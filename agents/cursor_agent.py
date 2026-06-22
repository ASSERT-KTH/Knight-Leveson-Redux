"""
Cursor agent adapter.

Invokes the `agent` CLI (Cursor headless CLI) in print mode.
Requires: Cursor CLI installed and CURSOR_API_KEY (or CURSOR_ACCESS_TOKEN) set.

Correct invocation (verified via `agent --help`):
  agent --print --force --trust --workspace <sandbox> --api-key <key> \
        --output-format json "<prompt>"

Notes:
  - --trust  is required to skip the workspace-trust prompt in headless mode.
  - --force  allows all tool calls without per-command approval.
  - --api-key can also come from CURSOR_API_KEY env var.
"""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any

from agents.base import AgentBase, AgentUnavailableError
from agents.trajectory import DEFAULT_TRAJECTORY_NOTE, parse_jsonl_events


class CursorAgent(AgentBase):
    name = "cursor"
    default_model = "cursor-default"

    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(config)
        self.timeout = self.config.get("timeout_seconds", 600)
        self.model = self.config.get("model", None)  # e.g. "gpt-5", "sonnet-4"

    def _invoke(self, sandbox: Path, prompt: str) -> tuple[str, str, str]:
        # Accept either name for the Cursor CLI binary
        cli = shutil.which("agent") or shutil.which("cursor")
        if not cli:
            raise AgentUnavailableError(
                "'agent' (or 'cursor') CLI not found in PATH. "
                "Install: curl https://cursor.com/install -fsS | bash"
            )

        # Accept CURSOR_API_KEY or CURSOR_ACCESS_TOKEN
        api_key = (
            os.environ.get("CURSOR_API_KEY") or
            os.environ.get("CURSOR_ACCESS_TOKEN")
        )
        if not api_key:
            raise AgentUnavailableError(
                "Neither CURSOR_API_KEY nor CURSOR_ACCESS_TOKEN is set. "
                "Set one of them: export CURSOR_API_KEY=<your-key>"
            )

        cmd = [
            cli,
            "--print",
            "--force",
            "--trust",
            "--workspace", str(sandbox),
            "--api-key", api_key,
            "--output-format", "json",
        ]
        if self.model:
            cmd += ["--model", self.model]
        cmd.append(prompt)

        try:
            result = self._run_cli(
                cmd, cwd=sandbox, timeout=self.timeout,
                env={"CURSOR_API_KEY": api_key},
            )
        except Exception as exc:
            raise AgentUnavailableError(f"agent CLI failed to launch: {exc}") from exc

        trajectory = parse_jsonl_events(result.stdout or "", stream="stdout") + parse_jsonl_events(result.stderr or "", stream="stderr")
        self._set_invocation_artifacts(
            trajectory=trajectory or None,
            raw_agent_stdout=result.stdout or "",
            raw_agent_stderr=result.stderr or "",
            trajectory_capture_note=DEFAULT_TRAJECTORY_NOTE,
        )

        if result.returncode != 0:
            snippet = (result.stderr or result.stdout or "")[:500]
            raise AgentUnavailableError(
                f"agent CLI exited {result.returncode}. Output: {snippet}"
            )

        model_name = self.model or self.default_model
        for line in (result.stdout or "").splitlines():
            try:
                data = json.loads(line)
                if isinstance(data, dict) and "model" in data:
                    model_name = data["model"]
                    break
            except (json.JSONDecodeError, AttributeError):
                continue

        source_code = self._read_output(sandbox)
        build_status = "ok" if source_code else "no_output"
        return source_code, model_name, build_status

    def _get_generation_config(self) -> dict:
        return {
            "agent": "cursor",
            "cli": shutil.which("agent") or shutil.which("cursor") or "agent",
            "model": self.model or "default",
            "force": True,
        }
