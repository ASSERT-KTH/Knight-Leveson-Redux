"""
Pipeline stage 2: Acceptance screening.

For each generated version in --versions/:
  1. Check build status (must be "ok")
  2. Load or compile the candidate (Python in-process; Pascal/Rust JSON-lines binary)
  3. Run all acceptance test cases (pre-computed with oracle outputs)
  4. A version passes iff it produces correct output on every case

Writes admitted.json listing passing versions.
Writes exclusions.json listing rejected versions with reasons.

Usage:
    python -m pipeline.run_acceptance \\
        --versions results/pilot/versions/ \\
        --output results/pilot/accepted.json

    After changing compile harnesses (e.g. Rust ``types.rs``), re-check without regenerating:

        python -m pipeline.run_acceptance ... --revalidate-build
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agents.base import VersionRecord
from benchmarks.launch_interceptor.generator import generate_acceptance_cases
from harnesses.execution import create_runner

_ERR_CAP = 8000


def _compare_outputs(
    expected: tuple,
    actual: tuple,
) -> bool:
    """Return True if all 241 output bits match."""
    exp_cmv, exp_pum, exp_fuv, exp_launch = expected
    act_cmv, act_pum, act_fuv, act_launch = actual

    if list(act_cmv) != list(exp_cmv):
        return False
    for i in range(15):
        if list(act_pum[i]) != list(exp_pum[i]):
            return False
    if list(act_fuv) != list(exp_fuv):
        return False
    if bool(act_launch) != bool(exp_launch):
        return False
    return True


def _run_acceptance(
    record: VersionRecord,
    cases: list[dict],
    *,
    revalidate_build: bool = False,
) -> tuple[bool, str, int, int]:
    """
    Run acceptance tests on a version.

    Returns: (passed, reason, n_passed, n_total)

    ``revalidate_build``: if True, do not reject on cached ``build_status != "ok"`` when
    ``source_code`` is non-empty—compile/run again (e.g. after fixing the Rust harness).
    Updates ``record.build_status`` / ``record.error_message`` when revalidation runs.
    """
    blocked_by_status = record.build_status != "ok"
    if revalidate_build and (record.source_code or "").strip():
        blocked_by_status = False
    if blocked_by_status:
        return False, f"build_status={record.build_status}", 0, len(cases)

    tmp = Path(tempfile.mkdtemp(prefix="nvp_accept_"))
    runner = None
    try:
        runner, err = create_runner(record.language, record.source_code, tmp)
        if runner is None:
            if revalidate_build:
                record.build_status = "syntax_error"
                record.error_message = (err or "")[:_ERR_CAP]
            return False, err or "runner creation failed", 0, len(cases)
        if revalidate_build:
            record.build_status = "ok"
            record.error_message = ""

        n_passed = 0
        for i, case in enumerate(cases):
            try:
                result = runner.invoke(case)
                expected = (case["cmv"], case["pum"], case["fuv"], case["launch"])
                if not _compare_outputs(expected, result):
                    return False, f"wrong output on acceptance case {i}", n_passed, len(cases)
                n_passed += 1
            except Exception as exc:
                return False, f"exception on acceptance case {i}: {exc}", n_passed, len(cases)
        return True, "passed", n_passed, len(cases)
    finally:
        if runner is not None:
            try:
                runner.close()
            except Exception:
                pass
        shutil.rmtree(tmp, ignore_errors=True)


def run(
    versions_dir: str,
    output_path: str,
    seed: int = 42,
    acceptance_n: int = 200,
    *,
    revalidate_build: bool = False,
) -> None:
    versions_dir_path = Path(versions_dir)
    index_path = versions_dir_path / "index.json"

    if not index_path.exists():
        print(f"ERROR: {index_path} not found. Run generate_versions first.", file=sys.stderr)
        sys.exit(1)

    index = json.loads(index_path.read_text())
    print(f"Generating {acceptance_n} acceptance test cases (seed={seed + 1000})...")
    cases = generate_acceptance_cases(seed=seed, n=acceptance_n)
    print(f"Running acceptance screening on {len(index)} version(s)...\n")

    admitted: list[dict] = []
    excluded: list[dict] = []

    for entry in index:
        record = VersionRecord.from_json(versions_dir_path / entry["file"])
        passed, reason, n_ok, n_total = _run_acceptance(
            record, cases, revalidate_build=revalidate_build
        )

        lang = entry.get("language") or getattr(record, "language", None) or "python"
        result_entry = {
            "file": entry["file"],
            "version_id": entry.get("version_id", Path(entry["file"]).stem),
            "agent": entry["agent"],
            "run_id": entry["run_id"],
            "model": entry["model"],
            "language": lang,
            "build_status": record.build_status,
            "acceptance_cases_passed": n_ok,
            "acceptance_cases_total": n_total,
            "passed": passed,
            "reason": reason,
        }
        if "configured_model" in entry:
            result_entry["configured_model"] = entry["configured_model"]

        # Persist acceptance result back into the record
        record.acceptance_passed = passed
        record.to_json(versions_dir_path / entry["file"])

        status_str = "✓ ADMITTED" if passed else "✗ EXCLUDED"
        print(
            f"  {status_str}  {entry['agent']}/{lang}/run{entry['run_id']}  {reason}  ({n_ok}/{n_total} cases ok)"
        )

        if passed:
            admitted.append(result_entry)
        else:
            excluded.append(result_entry)

    output_path_p = Path(output_path)
    output_path_p.parent.mkdir(parents=True, exist_ok=True)

    result = {
        "admitted": admitted,
        "excluded": excluded,
        "seed": seed,
        "acceptance_n": acceptance_n,
        "n_admitted": len(admitted),
        "n_excluded": len(excluded),
    }
    output_path_p.write_text(json.dumps(result, indent=2))

    excl_path = output_path_p.parent / "exclusions.json"
    excl_path.write_text(json.dumps(excluded, indent=2))

    print(f"\nAdmitted: {len(admitted)}  Excluded: {len(excluded)}")
    print(f"Results: {output_path}")
    print(f"Exclusions: {excl_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run acceptance screening")
    parser.add_argument("--versions", required=True, help="Versions directory from generate_versions")
    parser.add_argument("--output", required=True, help="Output JSON file for admitted versions")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--acceptance-n", type=int, default=200)
    parser.add_argument(
        "--revalidate-build",
        action="store_true",
        help=(
            "Ignore cached build_status when source is present: compile again and refresh "
            "build_status (use after harness fixes without regenerating versions)"
        ),
    )
    args = parser.parse_args()
    run(
        args.versions,
        args.output,
        args.seed,
        args.acceptance_n,
        revalidate_build=args.revalidate_build,
    )


if __name__ == "__main__":
    main()
