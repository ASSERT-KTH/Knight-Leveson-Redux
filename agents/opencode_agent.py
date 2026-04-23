"""
OpenCode agent adapter (https://opencode.ai).

Invokes ``opencode run`` in non-interactive mode with JSON output.
Requires: ``opencode`` on PATH (see https://opencode.ai/docs/cli/).

**OpenRouter**

Same as manual ``opencode run`` / TUI: use an OpenRouter model id
``openrouter/<vendor>/<model>``, **or** set ``openrouter: true`` so a bare
``anthropic/claude-sonnet-4.5`` is passed to the CLI as
``openrouter/anthropic/claude-sonnet-4.5`` (OpenCode’s OpenRouter route).

Credentials: prefer ``opencode auth login`` (``~/.local/share/opencode/auth.json``)
— no env var required. Optionally set ``OPENROUTER_API_KEY`` in the environment
or repo ``.env`` (loaded before each run), or ``openrouter_api_key`` in YAML.

Optional ``openrouter_sandbox_config: true`` writes a minimal sandbox
``opencode.json`` with ``{env:OPENROUTER_API_KEY}`` for CI-only setups; **off by
default** so global auth behaves like your tmp-dir / TUI workflow.

Typical invocation::

  opencode run --format json --dir <sandbox> [--model ...] [--agent build] <task_prompt.txt>

The task is written to ``task_prompt.txt`` in the sandbox and passed as the message path.
Do not follow ``-f spec.md`` with the inline prompt: ``--file`` is variadic and would treat
the prompt as another filepath.

Use config ``attach`` for a running ``opencode serve`` instance.
Use ``opencode_agent`` for the OpenCode agent profile (e.g. ``build``).
"""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any

from agents.base import AgentBase, AgentUnavailableError
from harnesses import get_harness


def _load_dotenv_for_opencode() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    repo_root = Path(__file__).resolve().parents[1]
    load_dotenv(repo_root / ".env", override=False)
    load_dotenv(Path.cwd() / ".env", override=False)


# Optional CI-style injection; default is off so ~/.config + auth.json match TUI/tmp usage.
_SANDBOX_OPENROUTER_CONFIG = """{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "openrouter": {
      "options": {
        "apiKey": "{env:OPENROUTER_API_KEY}"
      }
    }
  }
}
"""


def _model_from_opencode_line(obj: dict) -> str | None:
    if not isinstance(obj, dict):
        return None
    for key in ("model", "modelId", "model_id"):
        v = obj.get(key)
        if isinstance(v, str) and v.strip():
            return v.strip()
    sess = obj.get("session")
    if isinstance(sess, dict):
        for key in ("model", "modelId"):
            v = sess.get(key)
            if isinstance(v, str) and v.strip():
                return v.strip()
    return None


def _error_obj_to_message(err: Any) -> str | None:
    if err is None:
        return None
    if isinstance(err, str) and err.strip():
        return err.strip()
    if isinstance(err, dict):
        data = err.get("data")
        if isinstance(data, dict):
            m = data.get("message")
            if isinstance(m, str) and m.strip():
                return m.strip()
        m = err.get("message")
        if isinstance(m, str) and m.strip():
            return m.strip()
        name = err.get("name")
        if isinstance(name, str) and name.strip():
            return name.strip()
    return None


def _opencode_stream_errors(stdout: str, stderr: str) -> list[str]:
    """
    With ``--format json``, OpenCode may print JSONL including ``{"type":"error",...}``
    while still exiting 0. Collect human-readable error strings.
    """
    messages: list[str] = []
    blob = (stdout or "") + "\n" + (stderr or "")
    for line in blob.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(obj, dict):
            continue
        if obj.get("type") == "error":
            msg = _error_obj_to_message(obj.get("error"))
            if msg:
                messages.append(msg)
    return messages


def _parse_opencode_stdout(stdout: str, fallback: str) -> str:
    """Best-effort model id from JSON or JSONL stream."""
    text = stdout.strip()
    if not text:
        return fallback
    last_model = fallback
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            m = _model_from_opencode_line(data)
            return m or last_model
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    m = _model_from_opencode_line(item)
                    if m:
                        last_model = m
            return last_model
    except json.JSONDecodeError:
        pass
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            m = _model_from_opencode_line(obj)
            if m:
                last_model = m
        except json.JSONDecodeError:
            continue
    return last_model


def _no_output_diagnostic(
    sandbox: Path,
    stdout: str,
    stderr: str,
    *,
    expected_artifact: str,
    language: str,
) -> str:
    """Explain missing harness artifact when OpenCode exits 0."""
    try:
        rel = [str(p.relative_to(sandbox)) for p in sorted(sandbox.rglob("*")) if p.is_file()]
    except ValueError:
        rel = [str(p) for p in sorted(sandbox.rglob("*")) if p.is_file()]
    lines = [
        "OpenCode exited successfully but no harness output file was found "
        f"(expected `{expected_artifact}` for language={language!r} under {sandbox}).",
        "Use `--agent build` (default). For OpenRouter, set `openrouter: true` and a valid model id.",
    ]
    if language != "python":
        lines.append(
            "Non-Python runs depend on the model writing the exact filename in the task prompt "
            f"(e.g. `lipdecide.pas`). If the model only emits Python or chat, you still get no_output."
        )
    lines.append(
        f"Files in sandbox ({len(rel)}): {rel[:40]}{' …' if len(rel) > 40 else ''}",
    )
    out = (stdout or "").strip()
    if out:
        tail = out[-3500:] if len(out) > 3500 else out
        lines.append(f"stdout (tail if long):\n{tail}")
    err = (stderr or "").strip()
    if err:
        lines.append(f"stderr:\n{err[-2000:]}")
    return "\n".join(lines)


class OpenCodeAgent(AgentBase):
    name = "opencode"
    default_model = "opencode"

    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(config)
        self.timeout = self.config.get("timeout_seconds", 600)
        self.model = self.config.get("model", None)
        self.attach = self.config.get("attach", None)
        # Default to "build" so `opencode run` uses a profile that edits/writes files.
        _oa = self.config.get("opencode_agent", None)
        self.opencode_agent = None if _oa is None else str(_oa).strip() or None
        if self.opencode_agent is None:
            self.opencode_agent = "build"
        self._openrouter_key_from_config = self.config.get("openrouter_api_key") or None

    def _use_openrouter(self) -> bool:
        if self.config.get("openrouter"):
            return True
        m = self.model
        return bool(m and str(m).startswith("openrouter/"))

    def _openrouter_sandbox_config(self) -> bool:
        return bool(self.config.get("openrouter_sandbox_config", False))

    def _effective_model(self) -> str | None:
        """Map anthropic/... → openrouter/anthropic/... when using OpenRouter."""
        if not self.model:
            return None
        ms = str(self.model).strip()
        if not self._use_openrouter():
            return ms
        if ms.startswith("openrouter/"):
            return ms
        if "/" in ms:
            return f"openrouter/{ms}"
        return ms

    def _openrouter_key(self) -> str | None:
        env_k = os.environ.get("OPENROUTER_API_KEY")
        if env_k and str(env_k).strip():
            return str(env_k).strip()
        if self._openrouter_key_from_config and str(self._openrouter_key_from_config).strip():
            return str(self._openrouter_key_from_config).strip()
        return None

    def _make_sandbox(self, spec_path: Path) -> Path:
        _load_dotenv_for_opencode()
        sandbox = super()._make_sandbox(spec_path)
        if (
            self._use_openrouter()
            and self._openrouter_sandbox_config()
            and self._openrouter_key()
        ):
            (sandbox / "opencode.json").write_text(
                _SANDBOX_OPENROUTER_CONFIG,
                encoding="utf-8",
            )
        return sandbox

    def _invoke(
        self,
        sandbox: Path,
        prompt: str,
    ) -> tuple[str, str, str] | tuple[str, str, str, str]:
        if not shutil.which("opencode"):
            raise AgentUnavailableError(
                "'opencode' CLI not found in PATH. "
                "Install: https://opencode.ai/docs/cli/"
            )

        _load_dotenv_for_opencode()

        if self._openrouter_sandbox_config() and not self._openrouter_key():
            raise AgentUnavailableError(
                "openrouter_sandbox_config is true but OPENROUTER_API_KEY (or "
                "openrouter_api_key in config) is not set. Needed for "
                "{env:OPENROUTER_API_KEY} in sandbox opencode.json."
            )

        eff_model = self._effective_model()
        sand = sandbox.resolve()

        # OpenCode's `-f` / `--file` is variadic: every token after `-f path` is treated as
        # another file until the next flag. Passing the inline prompt after `-f spec.md`
        # made the CLI try to open a "file" named the full prompt text → File not found.
        # Write the task to disk and pass that path as the message positional instead.
        task_path = sand / "task_prompt.txt"
        task_path.write_text(prompt, encoding="utf-8")

        cmd = [
            "opencode",
            "run",
            "--format",
            "json",
            "--dir",
            str(sand),
        ]
        if self.attach:
            cmd += ["--attach", str(self.attach)]
        if eff_model:
            cmd += ["--model", eff_model]
        cmd += ["--agent", str(self.opencode_agent)]
        # Message: path to prompt file (spec.md is already under --dir).
        cmd.append(str(task_path))

        env: dict[str, str] | None = None
        if self._openrouter_key_from_config:
            k = str(self._openrouter_key_from_config).strip()
            if k:
                env = {"OPENROUTER_API_KEY": k}

        try:
            result = self._run_cli(
                cmd, cwd=sandbox, timeout=self.timeout, env=env,
            )
        except Exception as exc:
            raise AgentUnavailableError(f"opencode CLI failed to launch: {exc}") from exc

        if result.returncode != 0:
            snippet = (result.stderr or result.stdout or "")[:500]
            raise AgentUnavailableError(
                f"opencode CLI exited {result.returncode}. Output: {snippet}"
            )

        stream_errs = _opencode_stream_errors(result.stdout or "", result.stderr or "")
        if stream_errs:
            raise AgentUnavailableError(
                "OpenCode JSON stream reported failure (process exited 0): "
                + "; ".join(stream_errs)
            )

        model_name = _parse_opencode_stdout(
            result.stdout or "",
            eff_model or self.model or self.default_model,
        )

        source_code = self._read_output(sandbox)
        build_status = "ok" if source_code else "no_output"
        if build_status == "no_output":
            lang = getattr(self, "_language", "python") or "python"
            expected = get_harness(lang).output_filename
            return (
                source_code,
                model_name,
                build_status,
                _no_output_diagnostic(
                    sandbox,
                    result.stdout or "",
                    result.stderr or "",
                    expected_artifact=expected,
                    language=lang,
                ),
            )
        return source_code, model_name, build_status

    def _get_generation_config(self) -> dict:
        out = {
            "agent": "opencode",
            "cli": "opencode",
            "model": self.model or "default",
            "model_passed_to_cli": self._effective_model() or self.model or "default",
            "attach": self.attach,
            "opencode_agent": self.opencode_agent,
            "opencode_agent_defaulted_to_build": self.config.get("opencode_agent") in (None, ""),
            "openrouter": self._use_openrouter(),
            "openrouter_sandbox_config": self._openrouter_sandbox_config(),
        }
        if self._openrouter_key_from_config and str(self._openrouter_key_from_config).strip():
            out["openrouter_api_key_from_config"] = True
        return out
