"""
Free Pascal target: archive source in `lipdecide.pas`; agent also builds a standalone executable.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from harnesses.base import LanguageHarness, platform_executable_name, run_cmd, which_or_none
from harnesses.prompt_context import build_reference_context

_PASCAL_DIR = Path(__file__).resolve().parent / "pascal"


PASCAL_TASK_PROMPT_TEMPLATE = """\
You are implementing the Launch Interceptor Program from Knight & Leveson (1986).

Your workspace initially contains only:
- `spec.md`
- `prompt_examples.json`
- `realcompare_reference.pas`

The file `spec.md` is the verbatim specification. All LICs and logic are defined only there.

Pascal delivery:
- Your main deliverable is a compiled executable at `{executable_path}`.
- On each run, it must read exactly one input JSON object from stdin and write exactly one
  output JSON object to stdout.
- The input will be in JSON format, and each input object will have the same shape as an
  individual `input` object inside `prompt_examples.json`. How you parse that JSON and how
  you build the executable are up to you.
- The logical input schema matches the pipeline cases: `numpoints`, `x`, `y`, `parameters`,
  `lcm`, and `pum_diag`.
- The expected output must be emitted in JSON format, and each output object must have the
  same shape as an individual `expected` object inside `prompt_examples.json`.
- The logical output schema is JSON-equivalent to `(cmv, pum, fuv, launch)`.
- Use `realcompare_reference.pas` as fixed reference behavior for `REALCOMPARE`; do not
  modify its logic.
- Also write the primary Pascal source snapshot to `{output_path}` for archival and later
  evaluation by the pipeline. The pipeline expects that file to contain the core Launch
  Interceptor logic in Pascal.

Engineering constraints:
- Do not read any files other than the provided reference files.
- Do not modify `realcompare_reference.pas`.
- Use only standard Free Pascal/RTL facilities.

The specification is in: {spec_path}

{reference_context}

Write the archival source file to: {output_path}
Write the main standalone deliverable to: {executable_path}
"""


class PascalHarness(LanguageHarness):
    name = "pascal"

    @property
    def output_filename(self) -> str:
        return "lipdecide.pas"

    @property
    def primary_artifact_filename(self) -> str:
        return platform_executable_name("decide_bin")

    def build_prompt(self, spec_path: str, output_path: str) -> str:
        return PASCAL_TASK_PROMPT_TEMPLATE.format(
            spec_path=spec_path,
            output_path=output_path,
            executable_path=self.primary_artifact_filename,
            reference_context=build_reference_context(self.name),
        )

    def check_syntax(self, source_code: str, work_dir: Path | None = None) -> str:
        if not which_or_none("fpc"):
            return "syntax_error"
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
        exe = work_dir / platform_executable_name("lip_harness")
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
