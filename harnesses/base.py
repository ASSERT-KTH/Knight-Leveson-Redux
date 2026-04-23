"""
Abstract language harness: prompts, syntax check, compile, and execute candidates.
"""
from __future__ import annotations

import shutil
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass


class LanguageHarness(ABC):
    """Per-target-language integration for generation and evaluation."""

    name: str = "base"

    @property
    @abstractmethod
    def output_filename(self) -> str:
        """Expected primary artifact filename in the agent sandbox."""

    @abstractmethod
    def build_prompt(self, spec_path: str, output_path: str) -> str:
        """Full task prompt for the coding agent."""

    @abstractmethod
    def check_syntax(self, source_code: str, work_dir: Path | None = None) -> str:
        """Return 'ok' or a failure token like 'syntax_error'."""

    @abstractmethod
    def read_output(self, sandbox: Path) -> str:
        """Read generated source from sandbox after agent run."""

    def compile_to_binary(self, source_code: str, work_dir: Path) -> tuple[Path | None, str]:
        """
        For compiled languages: write sources and produce an executable path.

        Returns ``(path, "")`` on success. On failure returns ``(None, message)``
        with compiler/tool output when available (empty string only for Python).
        """
        return None, ""  # overridden by Pascal/Rust


def which_or_none(name: str) -> str | None:
    return shutil.which(name)


def run_cmd(
    cmd: list[str],
    cwd: Path | None = None,
    *,
    timeout: int = 600,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
    )
