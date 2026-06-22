"""
Rust target: archive source in `decide.rs`; agent also builds a standalone executable.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from harnesses.base import LanguageHarness, platform_executable_name, run_cmd, which_or_none
from harnesses.prompt_context import build_reference_context

_RUST_PROJECT = Path(__file__).resolve().parent / "rust"


RUST_TASK_PROMPT_TEMPLATE = """\
You are implementing the Launch Interceptor Program from Knight & Leveson (1986).

Your workspace initially contains only:
- `spec.md`
- `prompt_examples.json`
- `realcompare_reference.rs`

The file `spec.md` is the verbatim specification. All LICs and logic are defined only there.

Rust delivery:
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
- Use `realcompare_reference.rs` as fixed reference behavior for `realcompare`; do not
  modify its logic.
- Also write the primary Rust source snapshot to `{output_path}` for archival and later
  evaluation by the pipeline. The pipeline expects that file to contain the core Launch
  Interceptor logic in Rust.

Engineering constraints:
- Do not read any files other than the provided reference files.
- Do not modify `realcompare_reference.rs`.
- Use standard Rust tooling and libraries only.

The specification is in: {spec_path}

{reference_context}

Write the archival source file to: {output_path}
Write the main standalone deliverable to: {executable_path}
"""


class RustHarness(LanguageHarness):
    name = "rust"

    @property
    def output_filename(self) -> str:
        return "decide.rs"

    @property
    def primary_artifact_filename(self) -> str:
        return platform_executable_name("decide_bin")

    def build_prompt(self, spec_path: str, output_path: str) -> str:
        return RUST_TASK_PROMPT_TEMPLATE.format(
            spec_path=spec_path,
            output_path=output_path,
            executable_path=self.primary_artifact_filename,
            reference_context=build_reference_context(self.name),
        )

    def check_syntax(self, source_code: str, work_dir: Path | None = None) -> str:
        if which_or_none("cargo") is None:
            return "syntax_error"
        wd = work_dir
        cleanup = False
        if wd is None:
            wd = Path(tempfile.mkdtemp(prefix="lip_rs_syntax_"))
            cleanup = True
        try:
            self._materialize_project(wd, source_code)
            r = run_cmd(["cargo", "check", "--quiet"], cwd=wd, timeout=600)
            return "ok" if r.returncode == 0 else "syntax_error"
        finally:
            if cleanup:
                shutil.rmtree(wd, ignore_errors=True)

    def read_output(self, sandbox: Path) -> str:
        p = sandbox / "decide.rs"
        if p.exists():
            return p.read_text(encoding="utf-8", errors="replace")
        for rs in sandbox.glob("*.rs"):
            t = rs.read_text(encoding="utf-8", errors="replace")
            if "fn decide(" in t:
                return t
        return ""

    def compile_to_binary(self, source_code: str, work_dir: Path) -> tuple[Path | None, str]:
        if which_or_none("cargo") is None:
            return None, "cargo not found on PATH"
        work_dir.mkdir(parents=True, exist_ok=True)
        self._materialize_project(work_dir, source_code)
        r = run_cmd(["cargo", "build", "--release", "--quiet"], cwd=work_dir, timeout=900)
        exe = work_dir / "target" / "release" / platform_executable_name("lip_harness")
        if r.returncode != 0 or not exe.exists():
            parts = [p for p in (r.stderr or "", r.stdout or "") if p and p.strip()]
            msg = "\n".join(s.strip() for s in parts)
            if not msg:
                msg = f"cargo build exited with code {r.returncode} (no output)"
            return None, msg
        return exe, ""

    @staticmethod
    def _materialize_project(work_dir: Path, decide_rs: str) -> None:
        shutil.copy2(_RUST_PROJECT / "Cargo.toml", work_dir / "Cargo.toml")
        src = work_dir / "src"
        src.mkdir(parents=True, exist_ok=True)
        shutil.copy2(_RUST_PROJECT / "src" / "types.rs", src / "types.rs")
        shutil.copy2(_RUST_PROJECT / "src" / "main.rs", src / "main.rs")
        (src / "decide.rs").write_text(decide_rs, encoding="utf-8")


class RustJsonlinesRunner:
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
            raise RuntimeError("Rust runner not started")
        self._p.stdin.write(line_in if line_in.endswith("\n") else line_in + "\n")
        self._p.stdin.flush()
        out = self._p.stdout.readline()
        if out == "" and self._p.poll() is not None:
            err = (self._p.stderr.read() if self._p.stderr else "") or ""
            raise RuntimeError(f"Rust harness exited (code={self._p.returncode}): {err[:500]}")
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
