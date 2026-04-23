"""
Pipeline stage 3: Shared randomized test campaign.

Runs every admitted version on the same set of campaign test cases.
Records pass/fail per test per version.

Output: campaign.csv with columns:
    test_id, version_id, agent, run_id, language, passed, exception

Optional: fault_events.jsonl (``--fault-log`` or config ``fault_log``) with inputs
and structured bit-diff for each failure (``fault_log_detail``: summary or full).

Also writes versions_meta.json with version metadata.

Parallelism: within each test case, evaluations for different versions run concurrently
(``ThreadPoolExecutor``). Configure with ``campaign_workers`` in YAML or ``--workers N``.
CSV row order is unchanged (test-major, version order preserved). Fault JSONL is written
from the main thread only.

Usage:
    python -m pipeline.run_campaign \\
        --accepted results/pilot/accepted.json \\
        --config config/pilot.yaml \\
        --output results/pilot/campaign.csv \\
        [--fault-log results/pilot/fault_events.jsonl]
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agents.base import VersionRecord
from benchmarks.launch_interceptor.decide_diff import campaign_inputs_only, diff_decide_outputs
from benchmarks.launch_interceptor.generator import iter_campaign_cases
from harnesses.execution import create_runner


def _compare_outputs(expected: tuple, actual: tuple) -> bool:
    exp_cmv, exp_pum, exp_fuv, exp_launch = expected
    act_cmv, act_pum, act_fuv, act_launch = actual
    if list(act_cmv) != list(exp_cmv):
        return False
    for i in range(15):
        if list(act_pum[i]) != list(exp_pum[i]):
            return False
    if list(act_fuv) != list(exp_fuv):
        return False
    return bool(act_launch) == bool(exp_launch)


def _eval_one_version(
    v: dict,
    case: dict,
    expected: tuple,
) -> tuple[bool, str, tuple | None]:
    """
    Run one version on one case. Safe to call concurrently for **different** `v`
    (each runner is exclusive to its version).
    """
    exc_msg = ""
    passed = False
    result: tuple | None = None
    if v["runner"] is None:
        exc_msg = v.get("runner_err") or "runner not available"
        return passed, exc_msg, result
    try:
        result = v["runner"].invoke(case)
        passed = _compare_outputs(expected, result)
    except Exception as exc:
        exc_msg = str(exc)[:200]
    return passed, exc_msg, result


def run(
    accepted_path: str,
    config_path: str,
    output_path: str,
    *,
    fault_log: str | None = None,
    workers: int | None = None,
) -> None:
    config = yaml.safe_load(Path(config_path).read_text())
    seed = config.get("seed", 42)
    campaign_n = config.get("campaign_n", 1000)
    fault_log_detail = config.get("fault_log_detail", "summary")
    if fault_log_detail not in ("summary", "full"):
        fault_log_detail = "summary"

    fault_log_path = fault_log if fault_log is not None else config.get("fault_log")
    fault_log_p: Path | None = None
    if fault_log_path:
        fault_log_p = Path(fault_log_path)
        if not fault_log_p.is_absolute():
            fault_log_p = (Path.cwd() / fault_log_p).resolve()
        fault_log_p.parent.mkdir(parents=True, exist_ok=True)

    accepted_data = json.loads(Path(accepted_path).read_text())
    admitted = accepted_data.get("admitted", [])

    if not admitted:
        print("ERROR: No admitted versions. Run run_acceptance first.", file=sys.stderr)
        sys.exit(1)

    if workers is not None:
        campaign_workers = max(1, int(workers))
    else:
        raw = config.get("campaign_workers")
        if raw is None:
            # Reasonable default: use CPUs but cap to avoid huge pools on many-core boxes
            campaign_workers = max(1, min(64, (os.cpu_count() or 8)))
        else:
            campaign_workers = max(1, int(raw))

    versions_dir = Path(accepted_path).parent / "versions"
    versions: list[dict] = []
    tmp_dirs: list[Path] = []

    for entry in admitted:
        fpath = versions_dir / entry["file"]
        record = VersionRecord.from_json(fpath)
        version_id = entry.get("version_id") or fpath.stem
        lang = entry.get("language") or getattr(record, "language", None) or "python"
        tmp = Path(tempfile.mkdtemp(prefix=f"nvp_camp_{version_id}_"))
        tmp_dirs.append(tmp)
        runner, rerr = create_runner(record.language, record.source_code, tmp)
        versions.append({
            "version_id": version_id,
            "agent": entry["agent"],
            "run_id": entry["run_id"],
            "model": entry["model"],
            "language": lang,
            "runner": runner,
            "runner_err": rerr,
        })

    print(
        f"Running {campaign_n} tests × {len(versions)} versions = {campaign_n * len(versions)} evaluations "
        f"({campaign_workers} parallel worker(s) per test)..."
    )

    # Progress / flush: keep memory and OS buffers bounded on multi-million-row campaigns
    progress_every = max(1000, campaign_n // 200)
    flush_every_tests = max(50, campaign_n // 1000)

    output_path_p = Path(output_path)
    output_path_p.parent.mkdir(parents=True, exist_ok=True)
    summary: dict[str, dict[str, int]] = {
        v["version_id"]: {"total": 0, "passed_count": 0} for v in versions
    }

    fault_out = fault_log_p.open("w", encoding="utf-8") if fault_log_p else None
    try:
        with output_path_p.open("w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "test_id",
                    "version_id",
                    "agent",
                    "run_id",
                    "language",
                    "passed",
                    "exception",
                ],
            )
            writer.writeheader()

            for test_id, case in enumerate(iter_campaign_cases(seed=seed, n=campaign_n)):
                expected = (case["cmv"], case["pum"], case["fuv"], case["launch"])
                if campaign_workers <= 1:
                    outcomes = [_eval_one_version(v, case, expected) for v in versions]
                else:
                    pool = min(campaign_workers, len(versions))
                    with ThreadPoolExecutor(max_workers=pool) as ex:
                        futures = [ex.submit(_eval_one_version, v, case, expected) for v in versions]
                        outcomes = [fu.result() for fu in futures]

                for v, (passed, exc_msg, result) in zip(versions, outcomes):
                    writer.writerow({
                        "test_id": test_id,
                        "version_id": v["version_id"],
                        "agent": v["agent"],
                        "run_id": v["run_id"],
                        "language": v["language"],
                        "passed": passed,
                        "exception": exc_msg,
                    })
                    summary[v["version_id"]]["total"] += 1
                    summary[v["version_id"]]["passed_count"] += int(passed)

                    if fault_out and not passed:
                        if v["runner"] is None:
                            diff_payload: dict = {
                                "malformed_actual": True,
                                "note": exc_msg,
                            }
                        elif result is None:
                            diff_payload = {
                                "malformed_actual": True,
                                "note": "exception or invalid return before compare",
                            }
                        else:
                            diff_payload = diff_decide_outputs(
                                expected, result, detail=fault_log_detail
                            )
                        event = {
                            "test_id": test_id,
                            "version_id": v["version_id"],
                            "agent": v["agent"],
                            "run_id": v["run_id"],
                            "language": v["language"],
                            "inputs": campaign_inputs_only(case),
                            "exception": exc_msg,
                            "diff": diff_payload,
                            "fault_log_detail": fault_log_detail,
                        }
                        fault_out.write(json.dumps(event, separators=(",", ":")) + "\n")

                if (test_id + 1) % progress_every == 0 or test_id + 1 == campaign_n:
                    print(f"  {test_id + 1}/{campaign_n} tests done", flush=True)
                if (test_id + 1) % flush_every_tests == 0:
                    f.flush()
    finally:
        if fault_out is not None:
            fault_out.close()
        for v in versions:
            r = v.get("runner")
            if r is not None:
                try:
                    r.close()
                except Exception:
                    pass
        for td in tmp_dirs:
            shutil.rmtree(td, ignore_errors=True)

    meta = [
        {
            "version_id": vv["version_id"],
            "agent": vv["agent"],
            "run_id": vv["run_id"],
            "model": vv["model"],
            "language": vv["language"],
        }
        for vv in versions
    ]
    meta_path = output_path_p.parent / "versions_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2))

    print("\nPer-version failure rates:")
    for version_id, stats in summary.items():
        total = stats["total"]
        passed_count = stats["passed_count"]
        failure_rate = 1 - (passed_count / total if total else 0.0)
        print(
            f"  {version_id}: total={total} passed={passed_count} "
            f"failures={total - passed_count} failure_rate={failure_rate:.6f}"
        )
    print(f"\nCampaign CSV: {output_path}")
    print(f"Versions meta: {meta_path}")
    if fault_log_p is not None:
        print(f"Fault log (failures only): {fault_log_p}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run shared test campaign")
    parser.add_argument("--accepted", required=True, help="accepted.json from run_acceptance")
    parser.add_argument("--config", required=True, help="YAML config")
    parser.add_argument("--output", required=True, help="Output campaign CSV")
    parser.add_argument(
        "--fault-log",
        default=None,
        help="JSONL path for failing cases (inputs + diff). Overrides config fault_log if set.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=None,
        metavar="N",
        help=(
            "Parallel threads for evaluating versions within each test (default: config "
            "`campaign_workers` or min(64, CPU count)). Use 1 to force sequential."
        ),
    )
    args = parser.parse_args()
    run(args.accepted, args.config, args.output, fault_log=args.fault_log, workers=args.workers)


if __name__ == "__main__":
    main()
