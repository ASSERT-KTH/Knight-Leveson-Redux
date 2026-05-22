"""
Pipeline stage: oracle-free mini-campaign that records each version's
15-bit CMV vector on every test case.

Motivation
----------
For RQ4 in the no-oracle regime we want to compare versions on a *per-LIC
basis* without ever consulting a trusted reference.  This script re-runs
the test campaign over a small subset of the campaign generator
(``--n 10000`` by default), executes every admitted version on every
case, and saves the raw 15-bit CMV (Conditions Met Vector) outputs.

Two versions disagree on a test whenever their 15-bit CMV vectors
differ; per-bit disagreement is computed downstream as the bit-wise XOR
between the two stored vectors.  No oracle is consulted in this stage.

Output (.npz, default ``cmv_outputs.npz`` next to ``--accepted``):

    versions   : object array of version_id strings (length V)
    languages  : object array of languages aligned with ``versions``
    agents     : object array of agents aligned with ``versions``
    cmv_packed : uint16 array of shape (V, T) — bit b of cmv_packed[v,t]
                 is the CMV[b] output of version v on test t.
                 Tests on which the version raised / produced malformed
                 output are flagged in ``valid``.
    valid      : uint8 array of shape (V, T); 1 iff the version produced
                 a well-formed (cmv, pum, fuv, launch) tuple on test t.
    seed, n    : scalars for reproducibility.

Usage:
    python -m pipeline.run_campaign_lic \\
        --accepted results/main/accepted.json \\
        --output   results/main-spec-3/cmv_outputs.npz \\
        --n 10000
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# The compiled binary path used by RustJsonlinesRunner is relative to the
# version's work dir (``<work>/target/release/lip_harness``).  External
# tooling sometimes exports CARGO_TARGET_DIR (e.g. Cursor's sandbox cache)
# which would silently redirect cargo's output and leave the work dir
# empty.  Strip it so cargo writes into the expected place.
os.environ.pop("CARGO_TARGET_DIR", None)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np  # noqa: E402

from agents.base import VersionRecord  # noqa: E402
from benchmarks.launch_interceptor.generator import iter_campaign_cases  # noqa: E402
from pipeline.harness_runtime import create_runner_factory, resolve_harness_root  # noqa: E402


def _pack_cmv_bits(cmv: list[bool]) -> int:
    """Pack a 15-element boolean vector into a uint16 (bit b ↔ CMV[b])."""
    if len(cmv) != 15:
        raise ValueError(f"expected 15-bit CMV, got {len(cmv)}")
    bits = 0
    for b, val in enumerate(cmv):
        if val:
            bits |= 1 << b
    return bits


def _eval_cmv_one_version(
    version: dict, case: dict
) -> tuple[int, int]:
    """Return ``(cmv_packed, valid)`` for one version on one case."""
    if version["runner"] is None:
        return 0, 0
    try:
        cmv, _pum, _fuv, _launch = version["runner"].invoke(case)
        if not isinstance(cmv, (list, tuple)) or len(cmv) != 15:
            return 0, 0
        return _pack_cmv_bits(list(cmv)), 1
    except Exception:
        return 0, 0


def run(
    accepted_path: str,
    output_path: str,
    *,
    seed: int = 42,
    n: int = 10_000,
    harness_root: str | None = None,
    workers: int | None = None,
    only_languages: set[str] | None = None,
) -> None:
    runner_factory = create_runner_factory(harness_root)
    if harness_root:
        print(f"Using harness root: {Path(harness_root).resolve()}")

    accepted_data = json.loads(Path(accepted_path).read_text())
    admitted = [a for a in accepted_data.get("admitted", []) if a.get("passed")]
    if not admitted:
        print("ERROR: no admitted versions in", accepted_path, file=sys.stderr)
        sys.exit(1)
    if only_languages:
        admitted = [a for a in admitted if a.get("language") in only_languages]
        if not admitted:
            print("ERROR: language filter excluded everything", file=sys.stderr)
            sys.exit(1)

    if workers is None:
        import os
        workers = max(1, min(64, (os.cpu_count() or 8)))

    versions_dir = Path(accepted_path).parent / "versions"
    versions: list[dict] = []
    tmp_dirs: list[Path] = []
    for entry in admitted:
        fpath = versions_dir / entry["file"]
        record = VersionRecord.from_json(fpath)
        version_id = entry.get("version_id") or fpath.stem
        lang = entry.get("language") or getattr(record, "language", None) or "python"
        tmp = Path(tempfile.mkdtemp(prefix=f"nvp_lic_{version_id}_"))
        tmp_dirs.append(tmp)
        runner, rerr = runner_factory(record.language, record.source_code, tmp)
        versions.append({
            "version_id": version_id,
            "agent": entry["agent"],
            "language": lang,
            "runner": runner,
            "runner_err": rerr or "",
        })
        if runner is None:
            print(f"  skipping {version_id}: {rerr}", file=sys.stderr)

    V = len(versions)
    cmv_packed = np.zeros((V, n), dtype=np.uint16)
    valid = np.zeros((V, n), dtype=np.uint8)

    print(
        f"Running {n} tests × {V} versions = {n * V} evaluations "
        f"({workers} parallel worker(s) per test) ..."
    )
    progress_every = max(200, n // 50)
    start = time.time()
    try:
        with ThreadPoolExecutor(max_workers=min(workers, V)) as ex:
            for test_id, case in enumerate(iter_campaign_cases(seed=seed, n=n)):
                futures = [
                    ex.submit(_eval_cmv_one_version, v, case) for v in versions
                ]
                for vi, fut in enumerate(futures):
                    bits, ok = fut.result()
                    cmv_packed[vi, test_id] = bits
                    valid[vi, test_id] = ok
                if (test_id + 1) % progress_every == 0 or test_id + 1 == n:
                    elapsed = time.time() - start
                    rate = (test_id + 1) / max(elapsed, 1e-9)
                    eta = (n - (test_id + 1)) / max(rate, 1e-9)
                    print(
                        f"  {test_id + 1}/{n}  "
                        f"({rate:.1f} tests/s, ETA {eta:.0f}s)",
                        flush=True,
                    )
    finally:
        for v in versions:
            r = v.get("runner")
            if r is not None:
                try:
                    r.close()
                except Exception:
                    pass
        for td in tmp_dirs:
            shutil.rmtree(td, ignore_errors=True)

    out = Path(output_path).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    np.savez(
        out,
        versions=np.asarray([v["version_id"] for v in versions], dtype=object),
        languages=np.asarray([v["language"] for v in versions], dtype=object),
        agents=np.asarray([v["agent"] for v in versions], dtype=object),
        cmv_packed=cmv_packed,
        valid=valid,
        seed=np.int64(seed),
        n=np.int64(n),
    )
    print(f"\nWrote {out}")
    invalid = (valid == 0).sum(axis=1)
    if invalid.any():
        print("Versions with non-empty invalid counts (top 5):")
        order = np.argsort(-invalid)
        for vi in order[:5]:
            if invalid[vi] == 0:
                break
            print(f"  {versions[vi]['version_id']}: {int(invalid[vi])}/{n}")


def main() -> None:
    p = argparse.ArgumentParser(description="Mini-campaign saving 15-bit CMV outputs")
    p.add_argument("--accepted", required=True, help="accepted.json (run_acceptance output)")
    p.add_argument("--output", required=True, help="cmv_outputs.npz output path")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--n", type=int, default=10_000)
    p.add_argument("--workers", type=int, default=None)
    p.add_argument(
        "--harness-root",
        default=None,
        help=(
            "Alternate harness directory to use for runner creation, e.g. "
            "harnesses-realcompare. Defaults to the importable harnesses package."
        ),
    )
    p.add_argument(
        "--realcompare-harness",
        action="store_true",
        help="Use harnesses-realcompare (equivalent to --harness-root harnesses-realcompare).",
    )
    p.add_argument(
        "--language", action="append", default=None,
        help="If given, restrict to these languages (repeatable).",
    )
    args = p.parse_args()
    only = set(args.language) if args.language else None
    try:
        harness_root = resolve_harness_root(args.harness_root, args.realcompare_harness)
    except ValueError as exc:
        p.error(str(exc))
    run(
        args.accepted,
        args.output,
        seed=args.seed,
        n=args.n,
        harness_root=harness_root,
        workers=args.workers,
        only_languages=only,
    )


if __name__ == "__main__":
    main()
