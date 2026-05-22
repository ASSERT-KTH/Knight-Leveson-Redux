"""
Runtime selection for candidate execution harnesses.

The normal pipeline uses the importable ``harnesses`` package.  Some experiments
keep a patched harness tree beside it, e.g. ``harnesses-realcompare``.  Because
those directories are not necessarily valid Python package names, this module can
load their harness modules directly from file paths and expose the same
``create_runner`` contract as ``harnesses.execution``.
"""
from __future__ import annotations

import importlib.util
import shutil
import tempfile
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Protocol

from harnesses.json_protocol import case_to_json_line, parse_output_line

_REASON_MAX_LEN = 12_000


class CandidateRunner(Protocol):
    def invoke(self, case: dict[str, Any]) -> tuple[list[bool], list[list[bool]], list[bool], bool]:
        ...

    def close(self) -> None:
        ...


CreateRunner = Callable[[str | None, str, Path | None], tuple[CandidateRunner | None, str]]


def realcompare_harness_root() -> Path:
    return Path(__file__).resolve().parents[1] / "harnesses-realcompare"


def resolve_harness_root(harness_root: str | None, realcompare_harness: bool) -> str | None:
    if realcompare_harness:
        if harness_root:
            raise ValueError("--harness-root and --realcompare-harness are mutually exclusive")
        return str(realcompare_harness_root())
    return harness_root


def create_runner_factory(harness_root: str | Path | None = None) -> CreateRunner:
    if harness_root is None:
        from harnesses.execution import create_runner

        return create_runner

    root = Path(harness_root).resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"harness root not found: {root}")

    python_harness = _load_module(root / "python_harness.py")
    pascal_harness = _load_module(root / "pascal_harness.py")
    rust_harness = _load_module(root / "rust_harness.py")

    harnesses = {
        "python": python_harness.PythonHarness(),
        "pascal": pascal_harness.PascalHarness(),
        "rust": rust_harness.RustHarness(),
    }

    def create_runner(
        language: str | None,
        source_code: str,
        tmp_parent: Path | None = None,
    ) -> tuple[CandidateRunner | None, str]:
        lang = (language or "python").lower()
        if lang not in harnesses:
            return None, f"unknown language: {language!r} (expected python|pascal|rust)"

        if lang == "python":
            mod = python_harness.load_decide_module(source_code)
            if mod is None:
                return None, "failed to load decide function"
            return _PythonRunner(python_harness, mod), ""

        parent = tmp_parent or Path(tempfile.mkdtemp(prefix=f"nvp_run_{lang}_"))
        parent.mkdir(parents=True, exist_ok=True)
        bin_path, compile_err = harnesses[lang].compile_to_binary(source_code, parent)
        if bin_path is None:
            if tmp_parent is None:
                shutil.rmtree(parent, ignore_errors=True)
            detail = compile_err.strip()
            if not detail:
                detail = f"failed to compile {lang} harness (no tool output; is fpc/cargo installed?)"
            return None, _truncate_reason(detail)

        if lang == "pascal":
            jr = pascal_harness.PascalJsonlinesRunner(bin_path)
        else:
            jr = rust_harness.RustJsonlinesRunner(bin_path)
        jr.start()
        return _JsonlinesRunner(jr), ""

    return create_runner


def _load_module(path: Path) -> ModuleType:
    if not path.is_file():
        raise FileNotFoundError(f"harness module not found: {path}")
    name = f"_nvp_harness_{path.parent.name.replace('-', '_')}_{path.stem}_{abs(hash(path))}"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"could not load harness module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _truncate_reason(msg: str) -> str:
    msg = msg.strip()
    if len(msg) <= _REASON_MAX_LEN:
        return msg
    return msg[: _REASON_MAX_LEN - 24] + "\n... (truncated)"


class _PythonRunner:
    def __init__(self, python_harness: ModuleType, mod: ModuleType) -> None:
        self._python_harness = python_harness
        self._mod = mod

    def invoke(self, case: dict[str, Any]) -> tuple[list[bool], list[list[bool]], list[bool], bool]:
        r = self._python_harness.call_decide(self._mod, case)
        return r[0], r[1], r[2], r[3]

    def close(self) -> None:
        pass


class _JsonlinesRunner:
    def __init__(self, inner: Any) -> None:
        self._inner = inner

    def invoke(self, case: dict[str, Any]) -> tuple[list[bool], list[list[bool]], list[bool], bool]:
        line = case_to_json_line(case)
        out = self._inner.call_one(line)
        return parse_output_line(out)

    def close(self) -> None:
        self._inner.close()
