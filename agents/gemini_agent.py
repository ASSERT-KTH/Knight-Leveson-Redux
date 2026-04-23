"""
Google Gemini CLI agent adapter.

Invokes `@google/gemini-cli` in headless mode (``gemini --prompt`` / ``-p``).
Requires: ``gemini`` on PATH (``npm install -g @google/gemini-cli``).

Authentication (non-interactive): export ``GEMINI_API_KEY`` (Google AI Studio),
put it in a repo-root ``.env`` (loaded automatically before each run), or set
``gemini_api_key`` in YAML (do not commit). If only ``GOOGLE_API_KEY`` is set
(some Google samples), it is forwarded to the CLI as ``GEMINI_API_KEY``.
Vertex / GCA: ``GOOGLE_GENAI_USE_VERTEXAI`` / ``GOOGLE_GENAI_USE_GCA``. OAuth:
``~/.gemini/settings.json``.

Reference: https://google-gemini.github.io/gemini-cli/docs/cli/headless.html

Typical invocation::

  gemini --prompt "<prompt>" --output-format json --approval-mode=yolo \\
         --include-directories <sandbox> [-m gemini-2.5-flash]

``--approval-mode=yolo`` auto-approves tool actions (do not combine with ``--yolo``;
current Gemini CLI rejects that pair).
"""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any

from agents.base import AgentBase, AgentUnavailableError


def _load_dotenv_for_gemini() -> None:
    """Load ``.env`` from repo root and cwd so IDE runs see keys (override=False)."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    repo_root = Path(__file__).resolve().parents[1]
    load_dotenv(repo_root / ".env", override=False)
    load_dotenv(Path.cwd() / ".env", override=False)


def _gemini_env_overrides(config_key: str | None) -> dict[str, str] | None:
    """
    Gemini CLI reads ``GEMINI_API_KEY``. Merge explicit config, or map
    ``GOOGLE_API_KEY`` when ``GEMINI_API_KEY`` is unset.
    """
    extra: dict[str, str] = {}
    if config_key and str(config_key).strip():
        extra["GEMINI_API_KEY"] = str(config_key).strip()
    elif not (os.environ.get("GEMINI_API_KEY") or "").strip():
        g = (os.environ.get("GOOGLE_API_KEY") or "").strip()
        if g:
            extra["GEMINI_API_KEY"] = g
    return extra or None


def _extract_gemini_response_dict(text: str) -> dict | None:
    """Parse JSON object from stdout (may be prefixed by CLI log lines)."""
    text = (text or "").strip()
    if not text:
        return None
    try:
        o = json.loads(text)
        return o if isinstance(o, dict) else None
    except json.JSONDecodeError:
        pass
    idx = text.find("\n{")
    if idx >= 0:
        try:
            o = json.loads(text[idx + 1 :].strip())
            return o if isinstance(o, dict) else None
        except json.JSONDecodeError:
            pass
    idx = text.find('{"')
    if idx >= 0:
        try:
            o = json.loads(text[idx:])
            return o if isinstance(o, dict) else None
        except json.JSONDecodeError:
            pass
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("{"):
            try:
                o = json.loads(s)
                return o if isinstance(o, dict) else None
            except json.JSONDecodeError:
                continue
    return None


def _gemini_cli_failure_message(returncode: int, stdout: str, stderr: str) -> str:
    blob = (stdout or "") + "\n" + (stderr or "")
    data = _extract_gemini_response_dict(blob)
    if data:
        err = data.get("error")
        if isinstance(err, dict) and err.get("message"):
            return f"gemini CLI exited {returncode}: {err['message'][:600]}"
    snippet = (stderr or stdout or "").strip()[:600]
    return f"gemini CLI exited {returncode}. Output: {snippet}"


def _model_from_gemini_json(obj: dict) -> str | None:
    stats = obj.get("stats")
    if not isinstance(stats, dict):
        return None
    models = stats.get("models")
    if not isinstance(models, dict) or not models:
        return None
    return next(iter(models.keys()), None)


class GeminiAgent(AgentBase):
    name = "gemini"
    default_model = "gemini"

    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(config)
        self.timeout = self.config.get("timeout_seconds", 600)
        self.model = self.config.get("model", None)  # e.g. "gemini-2.5-flash"
        self._gemini_api_key_from_config = self.config.get("gemini_api_key") or None

    def _invoke(self, sandbox: Path, prompt: str) -> tuple[str, str, str]:
        if not shutil.which("gemini"):
            raise AgentUnavailableError(
                "'gemini' CLI not found in PATH. "
                "Install: npm install -g @google/gemini-cli"
            )

        _load_dotenv_for_gemini()

        cmd = [
            "gemini",
            "--prompt",
            prompt,
            "--output-format",
            "json",
            "--approval-mode=yolo",
            "--include-directories",
            str(sandbox),
        ]
        if self.model:
            cmd += ["--model", self.model]

        cfg_key: str | None = None
        if self._gemini_api_key_from_config is not None:
            s = str(self._gemini_api_key_from_config).strip()
            if s:
                cfg_key = s
        env = _gemini_env_overrides(cfg_key)

        try:
            result = self._run_cli(cmd, cwd=sandbox, timeout=self.timeout, env=env)
        except Exception as exc:
            raise AgentUnavailableError(f"gemini CLI failed to launch: {exc}") from exc

        if result.returncode != 0:
            raise AgentUnavailableError(
                _gemini_cli_failure_message(
                    result.returncode,
                    result.stdout or "",
                    result.stderr or "",
                )
            )

        model_name = self.model or self.default_model
        data = _extract_gemini_response_dict(result.stdout or "")
        if data:
            err = data.get("error")
            if isinstance(err, dict) and err.get("message"):
                raise AgentUnavailableError(
                    f"gemini API error: {err.get('message', err)[:400]}"
                )
            m = _model_from_gemini_json(data)
            if m:
                model_name = m

        source_code = self._read_output(sandbox)
        build_status = "ok" if source_code else "no_output"
        return source_code, model_name, build_status

    def _get_generation_config(self) -> dict:
        out = {
            "agent": "gemini",
            "cli": "gemini",
            "model": self.model or "default",
            "headless": True,
            "approval_mode": "yolo",
        }
        if self._gemini_api_key_from_config and str(self._gemini_api_key_from_config).strip():
            out["gemini_api_key_from_config"] = True
        return out
