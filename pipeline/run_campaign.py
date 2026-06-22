"""
Pipeline stage 3: Shared randomized test campaign.

Runs every admitted version on the same set of campaign test cases.
Records pass/fail per test per version.

Output: campaign.csv with columns:
    test_id, version_id, agent, run_id, language, passed, exception

Optional: fault_events.jsonl (``--fault-log`` or config ``fault_log``) with inputs
and structured bit-diff for each failure (``fault_log_detail``: summary or full).

Also writes versions_meta.json with version metadata.

Parallelism: evaluations are scheduled across the full (test, version) space, but
CSV row order remains test-major with version order preserved. Configure with
``campaign_workers`` in YAML or ``--workers N``. Fault JSONL is written from the
main thread only.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import resource
import shutil
import subprocess
import sys
import tempfile
import threading
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from pathlib import Path
from typing import Any, Protocol

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agents.base import VersionRecord
from benchmarks.launch_interceptor.decide_diff import (
    PackedDecideOutput,
    campaign_inputs_only,
    diff_decide_outputs,
    pack_decide_output,
    packed_output_digest,
    unpack_decide_output,
)
from benchmarks.launch_interceptor.generator import iter_test_cases
from harnesses.json_protocol import case_to_json_line, parse_output_line
from pipeline.harness_runtime import resolve_harness_root
from pipeline.oracle_cache import OracleCache, load_or_build_oracle_cache

_CASE_TIMEOUT_SECONDS = 30.0
_NOFILE_TARGET = 8192
_NOFILE_RESERVED = 128
_FDS_PER_SUBPROCESS = 4
_invoke_semaphore: threading.Semaphore | None = None


def _nofile_soft_limit() -> int:
    try:
        soft, _hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        return int(soft)
    except (ValueError, OSError, AttributeError):
        return 1024


def _raise_nofile_soft_limit(min_desired: int = _NOFILE_TARGET) -> int:
    try:
        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        target = min(max(min_desired, soft), hard)
        if target > soft:
            resource.setrlimit(resource.RLIMIT_NOFILE, (target, hard))
            return target
        return soft
    except (ValueError, OSError, AttributeError):
        return _nofile_soft_limit()


def _cap_campaign_workers(requested: int) -> tuple[int, int, str | None]:
    """Cap worker count so concurrent subprocess pipes stay under RLIMIT_NOFILE."""
    nofile = _raise_nofile_soft_limit()
    max_by_fd = max(1, (nofile - _NOFILE_RESERVED) // _FDS_PER_SUBPROCESS)
    effective = min(requested, max_by_fd)
    warning = None
    if effective < requested:
        warning = (
            f"Reducing campaign_workers from {requested} to {effective} to avoid "
            f"'Too many open files' (RLIMIT_NOFILE={nofile}; reserve "
            f"{_NOFILE_RESERVED}, ~{_FDS_PER_SUBPROCESS} fds per concurrent subprocess). "
            f"Raise `ulimit -n` to allow more parallelism."
        )
    return effective, nofile, warning


class ArtifactRunner(Protocol):
    def invoke(self, case_bytes: bytes) -> tuple[list[bool], list[list[bool]], list[bool], bool]:
        ...

    def close(self) -> None:
        ...


def _minimal_subprocess_env() -> dict[str, str]:
    source = os.environ
    env = {
        "PATH": source.get("PATH", ""),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
    }
    for key in ("HOME", "TMPDIR", "LD_LIBRARY_PATH", "SYSTEMROOT", "WINDIR", "PATHEXT"):
        value = source.get(key)
        if value:
            env[key] = value
    return env


_SUBPROCESS_ENV = _minimal_subprocess_env()


def _packed_equals(expected: PackedDecideOutput, actual: PackedDecideOutput) -> bool:
    return (
        actual.cmv_bits == expected.cmv_bits
        and actual.pum_rows == expected.pum_rows
        and actual.fuv_bits == expected.fuv_bits
        and actual.launch_bit == expected.launch_bit
    )


def _artifact_command(language: str, artifact_path: Path) -> list[str]:
    if language == "python":
        return [sys.executable, "-S", "-B", "-u", str(artifact_path)]
    return [str(artifact_path)]


class OneShotArtifactRunner:
    def __init__(self, language: str, artifact_path: Path) -> None:
        self._language = language
        self._artifact_path = artifact_path
        self._cmd = _artifact_command(language, artifact_path)
        self._cwd = str(artifact_path.parent)
        self._env = _SUBPROCESS_ENV

    def invoke(self, case_bytes: bytes) -> tuple[list[bool], list[list[bool]], list[bool], bool]:
        sem = _invoke_semaphore
        if sem is not None:
            sem.acquire()
        try:
            result = subprocess.run(
                self._cmd,
                input=case_bytes,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                cwd=self._cwd,
                env=self._env,
                timeout=_CASE_TIMEOUT_SECONDS,
                text=False,
            )
            if result.returncode != 0:
                diag = subprocess.run(
                    self._cmd,
                    input=case_bytes,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=self._cwd,
                    env=self._env,
                    timeout=_CASE_TIMEOUT_SECONDS,
                    text=False,
                )
                stderr = (diag.stderr or b"").decode("utf-8", errors="replace").strip()[:1000]
                stdout = (diag.stdout or b"").decode("utf-8", errors="replace").strip()[:1000]
                raise RuntimeError(
                    f"artifact exited {result.returncode}; stdout={stdout!r}; stderr={stderr!r}"
                )
            return parse_output_line((result.stdout or b"").decode("utf-8", errors="replace"))
        finally:
            if sem is not None:
                sem.release()

    def close(self) -> None:
        return None


class MissingArtifactRunner:
    def __init__(self, error_message: str) -> None:
        self.error_message = error_message

    def invoke(self, case_bytes: bytes) -> tuple[list[bool], list[list[bool]], list[bool], bool]:
        del case_bytes
        raise RuntimeError(self.error_message)

    def close(self) -> None:
        return None


def _build_runner(language: str, artifact_path: Path | None, runner_err: str) -> ArtifactRunner:
    if artifact_path is None:
        return MissingArtifactRunner(runner_err or "artifact not available")
    return OneShotArtifactRunner(language, artifact_path)


def _compare_actual_to_expected(
    expected_packed: PackedDecideOutput,
    expected_digest: int,
    actual: tuple[list[bool], list[list[bool]], list[bool], bool],
) -> bool:
    packed_actual = pack_decide_output(actual)
    actual_digest = packed_output_digest(packed_actual)
    if actual_digest != expected_digest:
        return False
    return _packed_equals(expected_packed, packed_actual)


def _eval_one_version(
    version: dict[str, Any],
    case_bytes: bytes,
    expected_packed: PackedDecideOutput,
    expected_digest: int,
) -> tuple[bool, str, tuple[list[bool], list[list[bool]], list[bool], bool] | None]:
    exc_msg = ""
    result: tuple[list[bool], list[list[bool]], list[bool], bool] | None = None
    try:
        result = version["runner"].invoke(case_bytes)
        passed = _compare_actual_to_expected(expected_packed, expected_digest, result)
        return passed, exc_msg, result
    except Exception as exc:
        exc_msg = str(exc)[:200]
        return False, exc_msg, result


def _oracle_cache_dir(accepted_path: str, config: dict[str, Any], override: str | None) -> Path:
    if override:
        return Path(override).resolve()
    configured = config.get("campaign_oracle_cache_dir")
    if configured:
        return Path(configured).expanduser().resolve()
    return (Path(accepted_path).resolve().parent / "oracle_cache").resolve()


def _load_expected_cache(
    accepted_path: str,
    config: dict[str, Any],
    seed: int,
    campaign_n: int,
    oracle_cache_dir: str | None,
) -> OracleCache:
    cache_dir = _oracle_cache_dir(accepted_path, config, oracle_cache_dir)
    return load_or_build_oracle_cache(cache_dir, seed, campaign_n)


def _candidate_tmpfs_root() -> Path | None:
    root = Path("/dev/shm")
    if root.is_dir() and os.access(root, os.W_OK | os.X_OK):
        return root
    return None


def _stage_artifacts_to_tmpfs(
    versions_dir: Path,
    artifact_files: list[str],
) -> tuple[dict[str, Path], Path | None]:
    tmpfs_root = _candidate_tmpfs_root()
    if tmpfs_root is None or not artifact_files:
        return {}, None
    stage_root = Path(tempfile.mkdtemp(prefix=f"redux_campaign_{os.getpid()}_", dir=str(tmpfs_root)))
    staged: dict[str, Path] = {}
    try:
        for rel in sorted(set(artifact_files)):
            src = versions_dir / rel
            if not src.is_file():
                continue
            dst = stage_root / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            staged[rel] = dst
        return staged, stage_root
    except Exception:
        shutil.rmtree(stage_root, ignore_errors=True)
        return {}, None


def _precompile_python_artifacts(target_dir: Path, versions: list[dict[str, Any]]) -> None:
    if not any(v["language"] == "python" and v.get("artifact_path") is not None for v in versions):
        return
    try:
        subprocess.run(
            [sys.executable, "-m", "compileall", "-q", str(target_dir)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            text=False,
        )
    except Exception:
        pass


def _warm_native_artifacts(versions: list[dict[str, Any]], warm_case_bytes: bytes) -> None:
    for version in versions:
        if version["language"] == "python":
            continue
        try:
            version["runner"].invoke(warm_case_bytes)
        except Exception:
            pass


def _flush_completed_test(
    test_id: int,
    pending_entry: dict[str, Any],
    versions: list[dict[str, Any]],
    writer: csv.DictWriter,
    summary: dict[str, dict[str, int]],
    fault_out,
    fault_log_detail: str,
) -> None:
    expected_tuple = None
    for version, (passed, exc_msg, result) in zip(versions, pending_entry["outcomes"]):
        writer.writerow({
            "test_id": test_id,
            "version_id": version["version_id"],
            "agent": version["agent"],
            "run_id": version["run_id"],
            "language": version["language"],
            "passed": passed,
            "exception": exc_msg,
        })
        summary[version["version_id"]]["total"] += 1
        summary[version["version_id"]]["passed_count"] += int(passed)

        if fault_out and not passed:
            if result is None:
                diff_payload: dict[str, Any] = {
                    "malformed_actual": True,
                    "note": exc_msg or "exception or invalid return before compare",
                }
            else:
                if expected_tuple is None:
                    expected_tuple = unpack_decide_output(pending_entry["expected_packed"])
                diff_payload = diff_decide_outputs(
                    expected_tuple,
                    result,
                    detail=fault_log_detail,
                )
            event = {
                "test_id": test_id,
                "version_id": version["version_id"],
                "agent": version["agent"],
                "run_id": version["run_id"],
                "language": version["language"],
                "inputs": campaign_inputs_only(pending_entry["case"]),
                "exception": exc_msg,
                "diff": diff_payload,
                "fault_log_detail": fault_log_detail,
            }
            fault_out.write(json.dumps(event, separators=(",", ":")) + "\n")


def run(
    accepted_path: str,
    config_path: str,
    output_path: str,
    *,
    fault_log: str | None = None,
    harness_root: str | None = None,
    workers: int | None = None,
    oracle_cache_dir: str | None = None,
) -> None:
    config = yaml.safe_load(Path(config_path).read_text())
    if harness_root:
        print(f"Ignoring harness root for artifact-based campaign execution: {Path(harness_root).resolve()}")
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
        requested_workers = max(1, int(workers))
    else:
        raw = config.get("campaign_workers")
        if raw is None:
            requested_workers = max(1, min(64, (os.cpu_count() or 8)))
        else:
            requested_workers = max(1, int(raw))

    campaign_workers, nofile_soft, worker_cap_warning = _cap_campaign_workers(requested_workers)
    if worker_cap_warning:
        print(f"WARNING: {worker_cap_warning}", file=sys.stderr)

    oracle_cache = _load_expected_cache(accepted_path, config, seed, campaign_n, oracle_cache_dir)
    print(f"Using oracle cache: {oracle_cache.cache_path}")

    versions_dir = Path(accepted_path).parent / "versions"
    artifact_files: list[str] = []
    version_meta: list[dict[str, Any]] = []
    for entry in admitted:
        fpath = versions_dir / entry["file"]
        record = VersionRecord.from_json(fpath)
        artifact_rel = getattr(record, "artifact_file", "") or entry.get("artifact_file", "") or ""
        version_meta.append({
            "record": record,
            "entry": entry,
            "artifact_rel": artifact_rel,
        })
        if artifact_rel:
            artifact_files.append(artifact_rel)

    staged_artifacts, staged_root = _stage_artifacts_to_tmpfs(versions_dir, artifact_files)
    artifact_root_for_python = staged_root or versions_dir

    versions: list[dict[str, Any]] = []
    for item in version_meta:
        record = item["record"]
        entry = item["entry"]
        version_id = entry.get("version_id") or Path(entry["file"]).stem
        lang = entry.get("language") or getattr(record, "language", None) or "python"
        artifact_rel = item["artifact_rel"]
        artifact_path = None
        runner_err = ""
        if artifact_rel:
            artifact_path = staged_artifacts.get(artifact_rel) or (versions_dir / artifact_rel).resolve()
            if not artifact_path.is_file():
                runner_err = f"artifact missing: {artifact_rel}"
                artifact_path = None
        else:
            runner_err = "missing artifact_file"
        runner = _build_runner(lang, artifact_path, runner_err)
        versions.append({
            "version_id": version_id,
            "agent": entry["agent"],
            "run_id": entry["run_id"],
            "model": entry["model"],
            "language": lang,
            "artifact_path": artifact_path,
            "runner": runner,
        })

    _precompile_python_artifacts(artifact_root_for_python, versions)
    warm_case = next(iter_test_cases(1, seed=seed, include_oracle_outputs=False))
    warm_case_bytes = (case_to_json_line(warm_case) + "\n").encode("utf-8")
    _warm_native_artifacts(versions, warm_case_bytes)

    print(
        f"Running {campaign_n} tests × {len(versions)} versions = {campaign_n * len(versions)} evaluations "
        f"({campaign_workers} parallel worker(s) across test/version pairs, "
        f"RLIMIT_NOFILE={nofile_soft})..."
    )

    progress_every = max(1000, campaign_n // 200)
    flush_every_tests = max(50, campaign_n // 1000)

    output_path_p = Path(output_path)
    output_path_p.parent.mkdir(parents=True, exist_ok=True)
    summary: dict[str, dict[str, int]] = {
        v["version_id"]: {"total": 0, "passed_count": 0} for v in versions
    }

    fault_out = fault_log_p.open("w", encoding="utf-8") if fault_log_p else None
    executor: ThreadPoolExecutor | None = None
    global _invoke_semaphore
    if campaign_workers > 1:
        _invoke_semaphore = threading.Semaphore(campaign_workers)
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

            if campaign_workers <= 1:
                for test_id, case in enumerate(iter_test_cases(campaign_n, seed=seed, include_oracle_outputs=False)):
                    expected_cmv_bits, expected_pum_rows, expected_fuv_bits, expected_launch_bit, expected_digest = oracle_cache.expected_at(test_id)
                    expected_packed = PackedDecideOutput(
                        cmv_bits=expected_cmv_bits,
                        pum_rows=expected_pum_rows,
                        fuv_bits=expected_fuv_bits,
                        launch_bit=expected_launch_bit,
                    )
                    case_bytes = (case_to_json_line(case) + "\n").encode("utf-8")
                    outcomes = [
                        _eval_one_version(version, case_bytes, expected_packed, expected_digest)
                        for version in versions
                    ]
                    _flush_completed_test(
                        test_id,
                        {
                            "case": case,
                            "expected_packed": expected_packed,
                            "outcomes": outcomes,
                        },
                        versions,
                        writer,
                        summary,
                        fault_out,
                        fault_log_detail,
                    )
                    if (test_id + 1) % progress_every == 0 or test_id + 1 == campaign_n:
                        print(f"  {test_id + 1}/{campaign_n} tests done", flush=True)
                    if (test_id + 1) % flush_every_tests == 0:
                        f.flush()
            else:
                executor = ThreadPoolExecutor(max_workers=campaign_workers)
                # Keep in-flight work equal to worker count so each active subprocess
                # only holds stdin/stdout pipes and stays under RLIMIT_NOFILE.
                max_in_flight = campaign_workers
                case_iter = iter_test_cases(campaign_n, seed=seed, include_oracle_outputs=False)
                pending: dict[int, dict[str, Any]] = {}
                in_flight: dict[Future[tuple[bool, str, tuple[list[bool], list[list[bool]], list[bool], bool] | None]], tuple[int, int]] = {}
                submit_test_id = 0
                submit_version_index = 0
                next_flush_test_id = 0

                def _prepare_pending_test(test_id: int, case: dict[str, Any]) -> None:
                    expected_cmv_bits, expected_pum_rows, expected_fuv_bits, expected_launch_bit, expected_digest = oracle_cache.expected_at(test_id)
                    expected_packed = PackedDecideOutput(
                        cmv_bits=expected_cmv_bits,
                        pum_rows=expected_pum_rows,
                        fuv_bits=expected_fuv_bits,
                        launch_bit=expected_launch_bit,
                    )
                    pending[test_id] = {
                        "case": case,
                        "case_bytes": (case_to_json_line(case) + "\n").encode("utf-8"),
                        "expected_packed": expected_packed,
                        "expected_digest": expected_digest,
                        "outcomes": [None] * len(versions),
                        "remaining": len(versions),
                    }

                def submit_one() -> bool:
                    nonlocal submit_test_id, submit_version_index
                    if submit_test_id >= campaign_n:
                        return False
                    if len(in_flight) >= max_in_flight:
                        return False
                    test_id = submit_test_id
                    version_index = submit_version_index
                    if test_id not in pending:
                        _prepare_pending_test(test_id, next(case_iter))
                    entry = pending[test_id]
                    future = executor.submit(
                        _eval_one_version,
                        versions[version_index],
                        entry["case_bytes"],
                        entry["expected_packed"],
                        entry["expected_digest"],
                    )
                    in_flight[future] = (test_id, version_index)
                    submit_version_index += 1
                    if submit_version_index >= len(versions):
                        submit_test_id += 1
                        submit_version_index = 0
                    return True

                def fill_window() -> None:
                    while submit_one():
                        pass

                fill_window()
                while next_flush_test_id < campaign_n:
                    if not in_flight:
                        break
                    done, _ = wait(in_flight.keys(), return_when=FIRST_COMPLETED)
                    for future in done:
                        test_id, version_index = in_flight.pop(future)
                        entry = pending[test_id]
                        entry["outcomes"][version_index] = future.result()
                        entry["remaining"] -= 1
                    while next_flush_test_id in pending and pending[next_flush_test_id]["remaining"] == 0:
                        entry = pending.pop(next_flush_test_id)
                        _flush_completed_test(
                            next_flush_test_id,
                            entry,
                            versions,
                            writer,
                            summary,
                            fault_out,
                            fault_log_detail,
                        )
                        next_flush_test_id += 1
                        if next_flush_test_id % progress_every == 0 or next_flush_test_id == campaign_n:
                            print(f"  {next_flush_test_id}/{campaign_n} tests done", flush=True)
                        if next_flush_test_id % flush_every_tests == 0:
                            f.flush()
                    fill_window()
    finally:
        _invoke_semaphore = None
        if executor is not None:
            executor.shutdown(wait=True)
        if fault_out is not None:
            fault_out.close()
        for version in versions:
            try:
                version["runner"].close()
            except Exception:
                pass
        if staged_root is not None:
            shutil.rmtree(staged_root, ignore_errors=True)

    meta = [
        {
            "version_id": version["version_id"],
            "agent": version["agent"],
            "run_id": version["run_id"],
            "model": version["model"],
            "language": version["language"],
        }
        for version in versions
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
        "--harness-root",
        default=None,
        help=(
            "Ignored: campaign now executes archived artifacts directly rather than "
            "building runners from harness source."
        ),
    )
    parser.add_argument(
        "--realcompare-harness",
        action="store_true",
        help="Ignored: campaign now executes archived artifacts directly.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=None,
        metavar="N",
        help=(
            "Parallel threads for evaluating one-shot artifact invocations across the full "
            "(test, version) space. Use 1 to force sequential execution."
        ),
    )
    parser.add_argument(
        "--oracle-cache-dir",
        default=None,
        help="Optional directory for reusable packed oracle outputs. Defaults to `<results>/oracle_cache/`.",
    )
    args = parser.parse_args()
    try:
        harness_root = resolve_harness_root(args.harness_root, args.realcompare_harness)
    except ValueError as exc:
        parser.error(str(exc))
    run(
        args.accepted,
        args.config,
        args.output,
        fault_log=args.fault_log,
        harness_root=harness_root,
        workers=args.workers,
        oracle_cache_dir=args.oracle_cache_dir,
    )


if __name__ == "__main__":
    main()
