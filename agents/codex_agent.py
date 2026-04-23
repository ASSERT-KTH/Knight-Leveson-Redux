"""
OpenAI Codex agent adapter.

Invokes the `codex exec` subcommand in non-interactive mode.
Requires: codex CLI installed and CODEX_API_KEY (or OPENAI_API_KEY) set.
Codex requires a git repository in the working directory.

Correct invocation (verified via `codex exec --help`):
  codex exec --dangerously-bypass-approvals-and-sandbox --ephemeral \
             -C <sandbox> "<prompt>"

Notes:
  - --full-auto uses bwrap sandboxing internally, which requires Linux namespaces
    that are typically not available in containers / CI (EPERM on loopback setup).
    Result: apply_patch always fails → no_output.
  - --dangerously-bypass-approvals-and-sandbox disables bwrap and all approval
    prompts, letting the agent write files directly. Safe because our /tmp sandbox
    is already isolated at the process level.
  - --ephemeral prevents codex from writing session files to ~/.codex/sessions/.
  - -C <dir> sets the workspace root so codex knows where to write.
  - --skip-git-repo-check allows running outside a git repo (still initialise one
    anyway since some codex internals prefer it).
  - --json emits JSONL events to stdout for progress visibility; last agent message
    usually contains summary but decide.py is written to disk.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from agents.base import AgentBase, AgentUnavailableError


class CodexAgent(AgentBase):
    name = "codex"
    default_model = "codex"

    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(config)
        self.timeout = self.config.get("timeout_seconds", 600)
        self.model = self.config.get("model", None)  # e.g. "o4-mini", "o3"

    def _make_sandbox(self, spec_path: Path) -> Path:
        """Codex prefers a git repo in the working directory."""
        sandbox = super()._make_sandbox(spec_path)
        for cmd in [
            ["git", "init", "-q"],
            ["git", "config", "user.email", "nvp@experiment.local"],
            ["git", "config", "user.name", "NVP Experiment"],
            ["git", "add", "."],
            ["git", "commit", "-m", "init", "-q", "--allow-empty"],
        ]:
            subprocess.run(cmd, cwd=str(sandbox), capture_output=True)
        return sandbox

    def _invoke(self, sandbox: Path, prompt: str) -> tuple[str, str, str]:
        if not shutil.which("codex"):
            raise AgentUnavailableError(
                "'codex' CLI not found in PATH. "
                "Install: npm install -g @openai/codex"
            )

        # Accept CODEX_API_KEY or OPENAI_API_KEY
        api_key = (
            os.environ.get("CODEX_API_KEY") or
            os.environ.get("OPENAI_API_KEY")
        )
        if not api_key:
            raise AgentUnavailableError(
                "Neither CODEX_API_KEY nor OPENAI_API_KEY is set. "
                "Set one: export OPENAI_API_KEY=sk-..."
            )

        cmd = [
            "codex", "exec",
            "--dangerously-bypass-approvals-and-sandbox",  # no bwrap; /tmp is externally isolated
            "--ephemeral",           # don't persist session files
            "--skip-git-repo-check", # tolerate missing/shallow git repos
            "-C", str(sandbox),      # set workspace root explicitly
            "--json",                # JSONL events to stdout
        ]
        if self.model:
            cmd += ["--model", self.model]
        cmd.append(prompt)

        env = {
            "CODEX_API_KEY": api_key,
            "OPENAI_API_KEY": api_key,
        }

        try:
            result = self._run_cli(cmd, cwd=sandbox, timeout=self.timeout, env=env)
        except Exception as exc:
            raise AgentUnavailableError(f"codex CLI failed to launch: {exc}") from exc

        if result.returncode != 0:
            snippet = (result.stderr or result.stdout or "")[:500]
            raise AgentUnavailableError(
                f"codex CLI exited {result.returncode}. Output: {snippet}"
            )

        # Parse model name from JSONL stream
        model_name = self.model or self.default_model
        for line in (result.stdout or "").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if isinstance(obj, dict) and "model" in obj:
                    model_name = obj["model"]
                    break
            except json.JSONDecodeError:
                continue

        source_code = self._read_output(sandbox)
        build_status = "ok" if source_code else "no_output"
        return source_code, model_name, build_status

    def _get_generation_config(self) -> dict:
        return {
            "agent": "codex",
            "cli": "codex",
            "mode": "exec --dangerously-bypass-approvals-and-sandbox",
            "model": self.model or "default",
            "ephemeral": True,
        }
