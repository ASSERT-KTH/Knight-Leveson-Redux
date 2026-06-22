"""
Pipeline stage 2: Acceptance screening.

For each generated version in --versions/:
  1. Check build status (must be "ok")
  2. Execute the archived artifact directly on JSON inputs
  3. Compare the artifact's JSON outputs against oracle outputs
  4. A version passes iff it produces correct output on every case

Writes admitted.json listing passing versions.
Writes exclusions.json listing rejected versions with reasons.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agents.base import VersionRecord
from harnesses import get_harness
from benchmarks.launch_interceptor.generator import generate_acceptance_cases
from harnesses.json_protocol import case_to_json_line

_CASE_TIMEOUT_SECONDS = 30


def _expected_output_object(case: dict[str, Any]) -> dict[str, Any]:
    return {
        "cmv": case["cmv"],
        "pum": case["pum"],
        "fuv": case["fuv"],
        "launch": case["launch"],
    }


def _parse_artifact_output(text: str) -> dict[str, Any]:
    text = (text or "").strip()
    if not text:
        raise ValueError("empty stdout")
    obj = json.loads(text)
    if not isinstance(obj, dict):
        raise ValueError("artifact output must be a JSON object")
    for key in ("cmv", "pum", "fuv", "launch"):
        if key not in obj:
            raise ValueError(f"artifact output missing key: {key}")
    cmv = [bool(x) for x in obj["cmv"]]
    pum = [[bool(x) for x in row] for row in obj["pum"]]
    fuv = [bool(x) for x in obj["fuv"]]
    launch = bool(obj["launch"])
    if len(cmv) != 15 or len(fuv) != 15 or len(pum) != 15:
        raise ValueError("wrong vector lengths")
    for row in pum:
        if len(row) != 15:
            raise ValueError("wrong PUM shape")
    return {
        "cmv": cmv,
        "pum": pum,
        "fuv": fuv,
        "launch": launch,
    }


def _compare_outputs(expected: dict[str, Any], actual: dict[str, Any]) -> bool:
    if list(actual["cmv"]) != list(expected["cmv"]):
        return False
    for i in range(15):
        if list(actual["pum"][i]) != list(expected["pum"][i]):
            return False
    return (
        list(actual["fuv"]) == list(expected["fuv"])
        and bool(actual["launch"]) == bool(expected["launch"])
    )


def _artifact_command(record: VersionRecord, artifact_path: Path) -> list[str]:
    if record.language == "python":
        return [sys.executable, str(artifact_path)]
    return [str(artifact_path)]


def _invoke_artifact(record: VersionRecord, artifact_path: Path, case: dict[str, Any]) -> dict[str, Any]:
    result = subprocess.run(
        _artifact_command(record, artifact_path),
        input=case_to_json_line(case) + "\n",
        capture_output=True,
        text=True,
        cwd=str(artifact_path.parent),
        timeout=_CASE_TIMEOUT_SECONDS,
    )
    if result.returncode != 0:
        stderr = (result.stderr or "").strip()[:1000]
        stdout = (result.stdout or "").strip()[:1000]
        raise RuntimeError(
            f"artifact exited {result.returncode}; stdout={stdout!r}; stderr={stderr!r}"
        )
    return _parse_artifact_output(result.stdout)


def _effective_build_status(record: VersionRecord, versions_dir: Path) -> tuple[str, str]:
    harness = get_harness(getattr(record, "language", None) or "python")
    artifact_rel = getattr(record, "artifact_file", "") or ""
    if artifact_rel:
        artifact_path = (versions_dir / artifact_rel).resolve()
        if artifact_path.is_file():
            status, detail = harness.validate_generation_result(Path(record.sandbox_dir), record.source_code)
            if status == "ok":
                return status, detail
            sandbox_artifact = harness.primary_artifact_path(Path(record.sandbox_dir))
            if sandbox_artifact and sandbox_artifact.resolve() == artifact_path.resolve():
                return status, detail
            if record.language == "python":
                status = harness.check_syntax(artifact_path.read_text(encoding="utf-8", errors="replace"))
                if status == "ok":
                    return "ok", ""
                return status, "archived Python artifact failed syntax validation"
            return "ok", ""
    return record.build_status, record.error_message or ""


def _run_acceptance(record: VersionRecord, versions_dir: Path, cases: list[dict]) -> tuple[bool, str, int, int]:
    effective_status, detail = _effective_build_status(record, versions_dir)
    record.build_status = effective_status
    record.error_message = "" if effective_status == "ok" else detail
    if effective_status != "ok":
        reason = f"build_status={effective_status}"
        if detail:
            reason = f"{reason}: {detail}"
        return False, reason, 0, len(cases)

    artifact_rel = getattr(record, "artifact_file", "") or ""
    if not artifact_rel:
        return False, "missing artifact_file", 0, len(cases)

    artifact_path = (versions_dir / artifact_rel).resolve()
    if not artifact_path.is_file():
        return False, f"artifact missing: {artifact_rel}", 0, len(cases)

    n_passed = 0
    for i, case in enumerate(cases):
        try:
            actual = _invoke_artifact(record, artifact_path, case)
            expected = _expected_output_object(case)
            if not _compare_outputs(expected, actual):
                return False, f"wrong output on acceptance case {i}", n_passed, len(cases)
            n_passed += 1
        except Exception as exc:
            return False, f"exception on acceptance case {i}: {exc}", n_passed, len(cases)
    return True, "passed", n_passed, len(cases)


def run(
    versions_dir: str,
    output_path: str,
    seed: int = 42,
    acceptance_n: int = 200,
    *,
    harness_root: str | None = None,
    revalidate_build: bool = False,
) -> None:
    del harness_root, revalidate_build

    versions_dir_path = Path(versions_dir)
    index_path = versions_dir_path / "index.json"

    if not index_path.exists():
        print(f"ERROR: {index_path} not found. Run generate_versions first.", file=sys.stderr)
        sys.exit(1)

    index = json.loads(index_path.read_text())
    version_seed_start = 2000
    print(
        f"Running acceptance screening on {len(index)} version(s) with unique per-version seeds "
        f"starting at {version_seed_start}...\n"
    )

    admitted: list[dict] = []
    excluded: list[dict] = []

    for version_offset, entry in enumerate(index):
        record = VersionRecord.from_json(versions_dir_path / entry["file"])
        version_seed = version_seed_start + version_offset
        cases = generate_acceptance_cases(seed=version_seed - 1000, n=acceptance_n)
        passed, reason, n_ok, n_total = _run_acceptance(record, versions_dir_path, cases)

        lang = entry.get("language") or getattr(record, "language", None) or "python"
        result_entry = {
            "file": entry["file"],
            "artifact_file": getattr(record, "artifact_file", "") or entry.get("artifact_file", ""),
            "trajectory_file": getattr(record, "trajectory_file", "") or entry.get("trajectory_file", ""),
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
        result_entry["acceptance_seed"] = version_seed

        record.acceptance_passed = passed
        record.to_json(versions_dir_path / entry["file"])

        status_str = "✓ ADMITTED" if passed else "✗ EXCLUDED"
        print(
            f"  {status_str}  {entry['agent']}/{lang}/run{entry['run_id']}  seed={version_seed}  {reason}  ({n_ok}/{n_total} cases ok)"
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
        "acceptance_seed_start": version_seed_start,
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
        "--harness-root",
        default=None,
        help="Ignored: artifact-based acceptance no longer uses harness-root execution.",
    )
    parser.add_argument(
        "--realcompare-harness",
        action="store_true",
        help="Ignored: artifact-based acceptance no longer uses alternate harness execution.",
    )
    parser.add_argument(
        "--revalidate-build",
        action="store_true",
        help="Ignored: acceptance now executes archived artifacts directly instead of recompiling source.",
    )
    args = parser.parse_args()
    run(
        args.versions,
        args.output,
        args.seed,
        args.acceptance_n,
        harness_root=args.harness_root,
        revalidate_build=args.revalidate_build,
    )


if __name__ == "__main__":
    main()
