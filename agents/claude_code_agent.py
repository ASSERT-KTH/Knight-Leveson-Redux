"""
Claude Code agent adapter.

Invokes the `claude` CLI in headless (-p/--print) mode.

Auth options (first non-empty value wins):
  1. Direct Anthropic:  ANTHROPIC_API_KEY=sk-ant-...
  2. OpenRouter:        OPENROUTER_API_KEY=sk-or-...
                        ANTHROPIC_BASE_URL=https://openrouter.ai/api
                        ANTHROPIC_AUTH_TOKEN=$OPENROUTER_API_KEY
  3. Generic alias:     CLAUDE_API_KEY=...

All ANTHROPIC_* env vars present in the environment are forwarded to the
subprocess unchanged, so any custom base URL / auth token configuration
that works for `claude -p "..."` in your shell will work here too.

Correct invocation (verified via `claude --help`):
  claude --print --dangerously-skip-permissions --no-session-persistence \
         --output-format json "<prompt>"
"""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any

from agents.base import AgentBase, AgentUnavailableError
from agents.trajectory import DEFAULT_TRAJECTORY_NOTE, parse_json_or_jsonl_output, parse_jsonl_events


# Env vars that carry Claude/Anthropic auth and routing config.
_AUTH_PASSTHROUGH = [
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_AUTH_TOKEN",
    "OPENROUTER_API_KEY",
    "CLAUDE_API_KEY",
]


def _resolve_auth() -> tuple[bool, dict[str, str]]:
    """
    Return (is_available, env_overrides).
    Auth is considered available when at least one non-empty key exists.
    Returns only the vars that are actually set so we don't clobber
    existing env with empty strings.
    """
    env: dict[str, str] = {}
    for var in _AUTH_PASSTHROUGH:
        val = os.environ.get(var)
        if val is not None:           # set (even if empty) → forward as-is
            env[var] = val

    available = bool(
        env.get("ANTHROPIC_API_KEY") or
        env.get("ANTHROPIC_AUTH_TOKEN") or
        env.get("OPENROUTER_API_KEY") or
        env.get("CLAUDE_API_KEY")
    )
    return available, env


class ClaudeCodeAgent(AgentBase):
    name = "claude_code"
    default_model = "claude"

    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(config)
        self.timeout = self.config.get("timeout_seconds", 600)
        self.model = self.config.get("model", None)  # e.g. "sonnet", "opus"

    def _invoke(self, sandbox: Path, prompt: str) -> tuple[str, str, str]:
        if not shutil.which("claude"):
            raise AgentUnavailableError(
                "'claude' CLI not found in PATH. "
                "Install Claude Code: https://code.claude.com"
            )

        available, auth_env = _resolve_auth()
        if not available:
            raise AgentUnavailableError(
                "No Claude auth found. Set one of: "
                "ANTHROPIC_API_KEY, ANTHROPIC_AUTH_TOKEN, OPENROUTER_API_KEY, or CLAUDE_API_KEY.\n"
                "For OpenRouter: export OPENROUTER_API_KEY=sk-or-... && "
                "export ANTHROPIC_BASE_URL=https://openrouter.ai/api && "
                "export ANTHROPIC_AUTH_TOKEN=$OPENROUTER_API_KEY"
            )

        # Prompt is passed via stdin to avoid --add-dir <directories...> consuming
        # the positional prompt argument (it accepts multiple values greedily).
        cmd = [
            "claude",
            "--print",
            "--dangerously-skip-permissions",
            "--no-session-persistence",
            "--output-format", "json",
            "--add-dir", str(sandbox),
        ]
        if self.model:
            cmd += ["--model", self.model]

        try:
            result = self._run_cli(
                cmd, cwd=sandbox, timeout=self.timeout, env=auth_env,
                stdin=prompt,
            )
        except Exception as exc:
            raise AgentUnavailableError(f"claude CLI failed to launch: {exc}") from exc

        trajectory = parse_json_or_jsonl_output(result.stdout or "", stream="stdout") + parse_jsonl_events(result.stderr or "", stream="stderr")
        self._set_invocation_artifacts(
            trajectory=trajectory or None,
            raw_agent_stdout=result.stdout or "",
            raw_agent_stderr=result.stderr or "",
            trajectory_capture_note=DEFAULT_TRAJECTORY_NOTE,
        )

        if result.returncode != 0:
            snippet = (result.stderr or result.stdout or "")[:500]
            raise AgentUnavailableError(
                f"claude CLI exited {result.returncode}. Output: {snippet}"
            )

        model_name = self.model or self.default_model
        if result.stdout:
            try:
                data = json.loads(result.stdout)
                if isinstance(data, dict) and data.get("model"):
                    model_name = data["model"]
            except (json.JSONDecodeError, AttributeError):
                pass

        source_code = self._read_output(sandbox)
        build_status = "ok" if source_code else "no_output"
        return source_code, model_name, build_status

    def _get_generation_config(self) -> dict:
        _, auth_env = _resolve_auth()
        return {
            "agent": "claude_code",
            "cli": "claude",
            "model": self.model or "default",
            "base_url": auth_env.get("ANTHROPIC_BASE_URL", "anthropic-direct"),
            "skip_permissions": True,
            "no_session_persistence": True,
        }
