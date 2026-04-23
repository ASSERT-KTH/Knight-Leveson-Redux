"""
Python target: in-process exec of decide.py; same semantics as the oracle contract.
"""
from __future__ import annotations

import types
from pathlib import Path
from typing import Any

from harnesses.base import LanguageHarness


PYTHON_TASK_PROMPT_TEMPLATE = """\
You are implementing the Launch Interceptor Program from Knight & Leveson (1986).

The file `spec.md` in your workspace is the verbatim specification: Pascal types,
global variables, the parameterless procedure `DECIDE`, and the `REALCOMPARE`
function contract. All functional requirements and Launch Interceptor Conditions
(LICs) are defined only there. Do not skip or reinterpret any part of it.

Python embedding (delivery only; this does not replace the spec):
- Implement a single function `decide` that is behaviorally equivalent to `DECIDE`.
- Inputs: `numpoints` (int, 2..100) corresponds to `NUMPOINTS`. `x` and `y` are
  Python lists of length `numpoints` with `x[i]`, `y[i]` as the coordinates of
  point i+1 in the spec (Pascal indices 1..NUMPOINTS → Python 0..numpoints-1).
- `parameters` is a Python dict whose keys are the field names of `PARAMETERS`
  in the spec (`LENGTH1`, `RADIUS1`, `EPSILON`, …) with the same types and
  constraints as in the Pascal record.
- `lcm` is a 15×15 list of strings, each entry one of `"NOTUSED"`, `"ORR"`, `"ANDD"`
  matching the `LCM` connector enum. The matrix is symmetric; diagonal entries
  are ignored for PUM off-diagonals (see spec).
- `pum_diag` is a length-15 list of bools: `pum_diag[i]` is the PUM diagonal
  element for LIC (i+1), i.e. the spec’s `PUM[i,i]` for i in 1..15.
- Return a 4-tuple `(cmv, pum, fuv, launch)`:
  - `cmv`: 15 bools, `cmv[i]` is CMV for LIC (i+1).
  - `pum`: 15×15 bools; off-diagonal from `LCM` and `CMV` per spec; diagonal
    `pum[i][i] == pum_diag[i]`.
  - `fuv`: 15 bools per the spec’s FUV rules.
  - `launch`: bool, the LAUNCH decision.
- The Pascal caller supplied `REALCOMPARE`. In Python there is no caller: define
  a helper `realcompare(a: float, b: float) -> str` that implements the same
  semantics, returning `"LT"`, `"EQ"`, or `"GT"` for the six-significant-digit
  comparison described in the spec. Use it everywhere the spec requires real
  comparisons inside the logic equivalent to `DECIDE`.

Engineering constraints:
- Write everything in one file named `decide.py`, self-contained and importable
  with no side effects at import time.
- Do not read from stdin, write to stdout/stderr, or read other files.
- Do not add any `if __name__ == "__main__"` block.
- Use only the Python standard library.

The specification is in: {spec_path}

Write your implementation to: {output_path}
"""


class PythonHarness(LanguageHarness):
    name = "python"

    @property
    def output_filename(self) -> str:
        return "decide.py"

    def build_prompt(self, spec_path: str, output_path: str) -> str:
        return PYTHON_TASK_PROMPT_TEMPLATE.format(spec_path=spec_path, output_path=output_path)

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
