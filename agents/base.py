"""
Base types and abstract interface for coding agent adapters.

Every real and mock agent adapter inherits from AgentBase and produces
VersionRecord instances.
"""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from harnesses import get_harness
from harnesses.prompt_context import provision_reference_files

# Backward-compatible alias (Python prompt body)
from harnesses.python_harness import PYTHON_TASK_PROMPT_TEMPLATE as TASK_PROMPT_TEMPLATE


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass
class VersionRecord:
    """Complete record of one agent-generated version."""
    agent_name: str                  # cursor | claude_code | codex | gemini | opencode | mock
    model_name: str                  # model identifier or "unknown"
    run_id: int                      # 0-indexed run number for this agent
    prompt: str                      # full prompt sent to the agent
    source_code: str                 # generated source ("" on failure)
    timestamp: str                   # ISO-8601 UTC
    generation_config: dict          # agent-specific settings logged verbatim
    acceptance_passed: bool | None   # None until acceptance stage runs
    build_status: str                # "ok"|"syntax_error"|"import_error"|"runtime_error"|"api_unavailable"|"no_output"
    sandbox_dir: str                 # path to isolated working directory
    artifact_file: str = ""
    trajectory_file: str = ""
    trajectory: list[dict[str, Any]] | None = None
    raw_agent_stdout: str = ""
    raw_agent_stderr: str = ""
    trajectory_capture_note: str = ""
    error_message: str = ""          # human-readable failure reason (empty on success)
    language: str = "python"         # python | pascal | rust

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "VersionRecord":
        # Forward-compat: drop unknown keys, supply defaults for new fields
        known = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore[attr-defined]
        filtered = {k: v for k, v in d.items() if k in known}
        if "language" not in filtered:
            filtered["language"] = "python"
        return cls(**filtered)

    def to_json(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), indent=2))

    @classmethod
    def from_json(cls, path: str | Path) -> "VersionRecord":
        return cls.from_dict(json.loads(Path(path).read_text()))


class AgentUnavailableError(RuntimeError):
    """Raised when an agent CLI or API key is not available."""


# ---------------------------------------------------------------------------
# Prompt helpers
# ---------------------------------------------------------------------------

def build_prompt(spec_path: str, output_path: str = "decide.py", *, language: str = "python") -> str:
    return get_harness(language).build_prompt(spec_path, output_path)


# ---------------------------------------------------------------------------
# Abstract base
# ---------------------------------------------------------------------------

class AgentBase(ABC):
    """Abstract base class for all coding agent adapters."""

    name: str = "base"
    default_model: str = "unknown"

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self._language: str = "python"
        self._invocation_artifacts: dict[str, Any] = {}

    def generate_version(
        self,
        spec_path: Path,
        run_id: int,
        *,
        language: str = "python",
    ) -> VersionRecord:
        """
        Generate one version by running the agent against spec_path.

        Creates a fresh sandbox directory, invokes the agent, collects
        the output file, and returns a VersionRecord.
        """
        self._language = language
        self._invocation_artifacts = {}
        harness = get_harness(language)
        out_name = harness.output_filename
        sandbox = self._make_sandbox(spec_path)
        provision_reference_files(sandbox, language)
        prompt = harness.build_prompt(
            spec_path=str(sandbox / "spec.md"),
            output_path=out_name,
        )
        timestamp = datetime.now(timezone.utc).isoformat()

        try:
            invoked = self._invoke(sandbox, prompt)
            if len(invoked) == 4:
                source_code, model_name, build_status, no_out_hint = invoked
            elif len(invoked) == 3:
                source_code, model_name, build_status = invoked
                no_out_hint = ""
            else:
                raise TypeError(f"_invoke must return 3 or 4 values, got {len(invoked)}")
        except AgentUnavailableError as exc:
            return VersionRecord(
                agent_name=self.name,
                model_name=self.default_model,
                run_id=run_id,
                prompt=prompt,
                source_code="",
                timestamp=timestamp,
                generation_config=self._get_generation_config(),
                trajectory=self._invocation_artifacts.get("trajectory"),
                raw_agent_stdout=self._invocation_artifacts.get("raw_agent_stdout", ""),
                raw_agent_stderr=self._invocation_artifacts.get("raw_agent_stderr", ""),
                trajectory_capture_note=self._invocation_artifacts.get("trajectory_capture_note", ""),
                acceptance_passed=None,
                build_status="api_unavailable",
                sandbox_dir=str(sandbox),
                error_message=str(exc),
                language=language,
            )

        if build_status == "ok":
            build_status, validation_detail = harness.validate_generation_result(sandbox, source_code)
            if validation_detail:
                no_out_hint = f"{no_out_hint}; {validation_detail}" if no_out_hint else validation_detail

        return VersionRecord(
            agent_name=self.name,
            model_name=model_name,
            run_id=run_id,
            prompt=prompt,
            source_code=source_code,
            timestamp=timestamp,
            generation_config=self._get_generation_config(),
            trajectory=self._invocation_artifacts.get("trajectory"),
            raw_agent_stdout=self._invocation_artifacts.get("raw_agent_stdout", ""),
            raw_agent_stderr=self._invocation_artifacts.get("raw_agent_stderr", ""),
            trajectory_capture_note=self._invocation_artifacts.get("trajectory_capture_note", ""),
            acceptance_passed=None,
            build_status=build_status,
            sandbox_dir=str(sandbox),
            error_message=no_out_hint if no_out_hint else "",
            language=language,
        )

    def _make_sandbox(self, spec_path: Path) -> Path:
        """Create a fresh isolated working directory with the spec."""
        sandbox = Path(tempfile.mkdtemp(prefix=f"nvp_{self.name}_"))
        (sandbox / "spec.md").write_text(spec_path.read_text())
        return sandbox

    @abstractmethod
    def _invoke(
        self,
        sandbox: Path,
        prompt: str,
    ) -> tuple[str, str, str] | tuple[str, str, str, str]:
        """
        Run the agent in sandbox.

        Return ``(source_code, model_name, build_status)`` or add an optional 4th
        string: human-readable diagnostic when ``build_status == "no_output"``.
        Raise AgentUnavailableError if CLI/API not available.
        """

    def _get_generation_config(self) -> dict:
        return dict(self.config)

    def _set_invocation_artifacts(
        self,
        *,
        trajectory: list[dict[str, Any]] | None = None,
        raw_agent_stdout: str = "",
        raw_agent_stderr: str = "",
        trajectory_capture_note: str = "",
    ) -> None:
        self._invocation_artifacts = {
            "trajectory": trajectory,
            "raw_agent_stdout": raw_agent_stdout,
            "raw_agent_stderr": raw_agent_stderr,
            "trajectory_capture_note": trajectory_capture_note,
        }

    def _read_output(self, sandbox: Path) -> str:
        """Read generated source from sandbox using the current language harness."""
        return get_harness(self._language).read_output(sandbox)

    @staticmethod
    def _run_cli(
        cmd: list[str],
        cwd: Path,
        timeout: int = 300,
        env: dict | None = None,
        stdin: str | None = None,
    ) -> subprocess.CompletedProcess:
        merged_env = {**os.environ, **(env or {})}
        return subprocess.run(
            cmd,
            cwd=str(cwd),
            input=stdin,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=merged_env,
        )
