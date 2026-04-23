"""
Create per-version runners for acceptance/campaign (Python in-process or JSON-lines binary).
"""
from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from types import ModuleType
from typing import Any, Protocol

from harnesses import get_harness
from harnesses.json_protocol import case_to_json_line, parse_output_line
from harnesses.pascal_harness import PascalJsonlinesRunner
from harnesses.python_harness import call_decide, load_decide_module
from harnesses.rust_harness import RustJsonlinesRunner

_REASON_MAX_LEN = 12_000


def _truncate_reason(msg: str) -> str:
    msg = msg.strip()
    if len(msg) <= _REASON_MAX_LEN:
        return msg
    return msg[: _REASON_MAX_LEN - 24] + "\n… (truncated)"


class CandidateRunner(Protocol):
    def invoke(self, case: dict[str, Any]) -> tuple[list[bool], list[list[bool]], list[bool], bool]:
        ...

    def close(self) -> None:
        ...


class _PythonRunner:
    def __init__(self, mod: ModuleType) -> None:
        self._mod = mod

    def invoke(self, case: dict[str, Any]) -> tuple[list[bool], list[list[bool]], list[bool], bool]:
        r = call_decide(self._mod, case)
        return r[0], r[1], r[2], r[3]

    def close(self) -> None:
        pass


class _JsonlinesRunner:
    def __init__(self, inner: PascalJsonlinesRunner | RustJsonlinesRunner) -> None:
        self._inner = inner

    def invoke(self, case: dict[str, Any]) -> tuple[list[bool], list[list[bool]], list[bool], bool]:
        line = case_to_json_line(case)
        out = self._inner.call_one(line)
        return parse_output_line(out)

    def close(self) -> None:
        self._inner.close()


def create_runner(
    language: str | None,
    source_code: str,
    tmp_parent: Path | None = None,
) -> tuple[CandidateRunner | None, str]:
    """
    Build a runner for one candidate (language + source).

    Returns (runner, error_message). runner is None on failure.
    """
    lang = (language or "python").lower()
    h = get_harness(lang)

    if lang == "python":
        mod = load_decide_module(source_code)
        if mod is None:
            return None, "failed to load decide function"
        return _PythonRunner(mod), ""

    parent = tmp_parent or Path(tempfile.mkdtemp(prefix=f"nvp_run_{lang}_"))
    parent.mkdir(parents=True, exist_ok=True)
    bin_path, compile_err = h.compile_to_binary(source_code, parent)
    if bin_path is None:
        if tmp_parent is None:
            shutil.rmtree(parent, ignore_errors=True)
        detail = compile_err.strip()
        if not detail:
            detail = f"failed to compile {lang} harness (no tool output; is fpc/cargo installed?)"
        return None, _truncate_reason(detail)

    if lang == "pascal":
        jr = PascalJsonlinesRunner(bin_path)
    else:
        jr = RustJsonlinesRunner(bin_path)
    jr.start()
    return _JsonlinesRunner(jr), ""
