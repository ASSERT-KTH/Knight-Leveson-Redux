"""
Free Pascal (fpc) target: unit `lipdecide` with procedure DECIDE; JSON-lines binary.
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from harnesses.base import LanguageHarness, run_cmd, which_or_none

_PASCAL_DIR = Path(__file__).resolve().parent / "pascal"


PASCAL_TASK_PROMPT_TEMPLATE = """\
You are implementing the Launch Interceptor Program from Knight & Leveson (1986).

The file `spec.md` in your workspace is the verbatim specification (Pascal types,
globals, parameterless `DECIDE`, and `REALCOMPARE`). All LICs and logic are defined
only there.

Free Pascal delivery (this does not replace the spec):
- Write a unit named `lipdecide` in a single file named `lipdecide.pas`.
- The unit must `use` the shared unit `globals` (provided by the evaluation harness),
  which declares all K&L global variables and the `COMPTYPE` enumeration (`LT`, `EQ`,
  `GT`). Do not redeclare those globals.
- Implement `function REALCOMPARE(A, B: real): COMPTYPE;` in `lipdecide` with the same
  semantics as in the spec (six-significant-digit comparison). The harness does not
  supply `REALCOMPARE`; use your implementation everywhere the spec requires real
  comparisons inside the logic equivalent to `DECIDE`.
- Implement `procedure DECIDE;` that reads inputs from and writes outputs to the
  globals in `globals` (same contract as the original Pascal problem statement).
- Indices: Pascal arrays `X[i]`, `Y[i]` for `i = 1 .. NUMPOINTS` match the spec.

Engineering constraints:
- Target Free Pascal (`fpc`). Use only the standard RTL and FPC standard units that
  ship with `fpc` (no external packages).
- Do not include a `program` or `begin`/`end.` main block — only the unit.

The specification is in: {spec_path}

Write your implementation to: {output_path}
"""


class PascalHarness(LanguageHarness):
    name = "pascal"

    @property
    def output_filename(self) -> str:
        return "lipdecide.pas"

    def build_prompt(self, spec_path: str, output_path: str) -> str:
        return PASCAL_TASK_PROMPT_TEMPLATE.format(spec_path=spec_path, output_path=output_path)

    def check_syntax(self, source_code: str, work_dir: Path | None = None) -> str:
        if not which_or_none("fpc"):
            return "syntax_error"
        # Full parse check would duplicate a harness compile; acceptance/campaign compile again.
        if len(source_code.strip()) < 20:
            return "syntax_error"
        if "lipdecide" not in source_code.lower() and "procedure" not in source_code.lower():
            return "syntax_error"
        return "ok"

    def read_output(self, sandbox: Path) -> str:
        p = sandbox / "lipdecide.pas"
        if p.exists():
            return p.read_text(encoding="utf-8", errors="replace")
        for pas in sandbox.glob("*.pas"):
            t = pas.read_text(encoding="utf-8", errors="replace")
            if "procedure DECIDE" in t.upper() or "procedure decide" in t.lower():
                return t
        return ""

    def compile_to_binary(self, source_code: str, work_dir: Path) -> tuple[Path | None, str]:
        fpc = which_or_none("fpc")
        if not fpc:
            return None, "fpc not found on PATH"
        work_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(_PASCAL_DIR / "globals.pas", work_dir / "globals.pas")
        shutil.copy2(_PASCAL_DIR / "wire_json.pas", work_dir / "wire_json.pas")
        shutil.copy2(_PASCAL_DIR / "lip_harness.pas", work_dir / "lip_harness.pas")
        (work_dir / "lipdecide.pas").write_text(source_code, encoding="utf-8")
        exe = work_dir / ("lip_harness.exe" if os.name == "nt" else "lip_harness")
        r = run_cmd(
            [fpc, "-Mobjfpc", "-Sh", "-O2", f"-o{exe.name}", "lip_harness.pas"],
            cwd=work_dir,
            timeout=600,
        )
        if r.returncode != 0 or not exe.exists():
            parts = [p for p in (r.stderr or "", r.stdout or "") if p and p.strip()]
            msg = "\n".join(s.strip() for s in parts)
            if not msg:
                msg = f"fpc exited with code {r.returncode} (no compiler output)"
            return None, msg
        return exe, ""


class PascalJsonlinesRunner:
    """One subprocess; one JSON line in, one line out per call."""

    def __init__(self, exe: Path) -> None:
        self._exe = exe
        self._p: subprocess.Popen[str] | None = None

    def start(self) -> None:
        self._p = subprocess.Popen(
            [str(self._exe)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

    def call_one(self, line_in: str) -> str:
        if self._p is None or self._p.stdin is None or self._p.stdout is None:
            raise RuntimeError("Pascal runner not started")
        self._p.stdin.write(line_in if line_in.endswith("\n") else line_in + "\n")
        self._p.stdin.flush()
        out = self._p.stdout.readline()
        if out == "" and self._p.poll() is not None:
            err = (self._p.stderr.read() if self._p.stderr else "") or ""
            raise RuntimeError(f"Pascal harness exited (code={self._p.returncode}): {err[:500]}")
        return out

    def close(self) -> None:
        if self._p is None:
            return
        if self._p.stdin:
            try:
                self._p.stdin.close()
            except BrokenPipeError:
                pass
        try:
            self._p.wait(timeout=30)
        except subprocess.TimeoutExpired:
            self._p.kill()
        self._p = None
