"""
Python target: in-process exec of decide.py; same semantics as the oracle contract.
"""
from __future__ import annotations

import types
from pathlib import Path
from typing import Any

from harnesses.base import LanguageHarness
from harnesses.prompt_context import build_reference_context


PYTHON_TASK_PROMPT_TEMPLATE = """\
You are implementing the Launch Interceptor Program from Knight & Leveson (1986).

Your workspace initially contains only:
- `spec.md`
- `prompt_examples.json`
- `realcompare_reference.py`

The file `spec.md` is the verbatim specification. All functional requirements and
Launch Interceptor Conditions (LICs) are defined only there.

Python delivery:
- Your main deliverable is a standalone Python file at `{executable_path}`.
- That file must be runnable as `python {executable_path}`.
- On each run, it must read exactly one input JSON object from stdin and write exactly one
  output JSON object to stdout.
- It should also expose `decide(numpoints, x, y, parameters, lcm, pum_diag)` and be
  self-contained and importable with no side effects at import time.
- The input will be in JSON format, and each input object will have the same shape as an
  individual `input` object inside `prompt_examples.json`. How you parse or adapt that JSON
  is up to you.
- The logical inputs correspond to:
  - `numpoints`: int, 2..100
  - `x`, `y`: lists of floats of length `numpoints`
  - `parameters`: dict using Pascal-style keys (`LENGTH1`, `RADIUS1`, `EPSILON`, ...)
  - `lcm`: 15x15 list of `"NOTUSED"`, `"ORR"`, `"ANDD"`
  - `pum_diag`: length-15 list of bools
- The expected output must be emitted in JSON format, and each output object must have the
  same shape as an individual `expected` object inside `prompt_examples.json`.
- The logical output is JSON-equivalent to `(cmv, pum, fuv, launch)`.
- Implement `realcompare(a: float, b: float) -> str` with the specified semantics,
  using `realcompare_reference.py` as fixed reference behavior.
- Also write the primary source snapshot to `{output_path}` for archival and later
  evaluation by the pipeline.

Engineering constraints:
- Do not read any files other than the provided reference files.
- Do not modify `realcompare_reference.py`.
- Use only the Python standard library.

The specification is in: {spec_path}

{reference_context}

Write the archival source file to: {output_path}
Write the main standalone deliverable to: {executable_path}
"""


class PythonHarness(LanguageHarness):
    name = "python"

    @property
    def output_filename(self) -> str:
        return "decide.py"

    @property
    def primary_artifact_filename(self) -> str:
        return "decide.py"

    def build_prompt(self, spec_path: str, output_path: str) -> str:
        return PYTHON_TASK_PROMPT_TEMPLATE.format(
            spec_path=spec_path,
            output_path=output_path,
            executable_path=self.primary_artifact_filename,
            reference_context=build_reference_context(self.name),
        )

    def check_syntax(self, source_code: str, work_dir: Path | None = None) -> str:
        try:
            compile(source_code, "<generated>", "exec")
            return "ok"
        except SyntaxError:
            return "syntax_error"

    def read_output(self, sandbox: Path) -> str:
        candidate = sandbox / "decide.py"
        if candidate.exists():
            return candidate.read_text()
        for py_file in sandbox.glob("*.py"):
            text = py_file.read_text()
            if "def decide(" in text:
                return text
        return ""

    def validate_generation_result(self, sandbox: Path, source_code: str) -> tuple[str, str]:
        artifact = self.primary_artifact_path(sandbox)
        if artifact is None:
            return "no_output", f"primary artifact not found: {self.primary_artifact_filename}"
        status = self.check_syntax(artifact.read_text(encoding="utf-8", errors="replace"))
        if status != "ok":
            return status, "generated Python artifact failed syntax validation"
        return "ok", ""


def load_decide_module(source_code: str) -> types.ModuleType | None:
    mod = types.ModuleType("candidate")
    try:
        exec(compile(source_code, "<candidate>", "exec"), mod.__dict__)  # noqa: S102
    except Exception:
        return None
    return mod if hasattr(mod, "decide") else None


def call_decide(mod: types.ModuleType, case: dict[str, Any]) -> Any:
    return mod.decide(
        case["numpoints"],
        case["x"],
        case["y"],
        case["parameters"],
        case["lcm"],
        case["pum_diag"],
    )
