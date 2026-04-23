"""
Rust target: `decide.rs` implements `decide(&DecideInput) -> DecideOutput`; JSON-lines binary.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from harnesses.base import LanguageHarness, run_cmd, which_or_none

_RUST_PROJECT = Path(__file__).resolve().parent / "rust"


RUST_TASK_PROMPT_TEMPLATE = """\
You are implementing the Launch Interceptor Program from Knight & Leveson (1986).

The file `spec.md` in your workspace is the verbatim specification. All LICs and logic
are defined only there.

## Rust delivery (evaluation harness)

Your code is linked as the `decide` module next to the harness `types.rs` and `main.rs`.
Submit **only** one file `decide.rs` implementing:

  `pub fn decide(input: &DecideInput) -> DecideOutput`

Import wire types with:

  `use crate::types::{{DecideInput, DecideOutput}};`

Do **not** declare `mod types;`, `mod main;`, or a `main` function. Do not add `Cargo.toml`
dependencies beyond what the harness already provides (serde for JSON types only).

## Types you must match exactly (same as `types.rs` in the harness)

`DecideInput` fields:
- `numpoints: usize` — number of points (2..100). Always index `input.x` / `input.y` with
  **usize** (e.g. `for i in 0..input.numpoints` then `input.x[i]`). If you have an `i32`
  index, cast: `input.x[i as usize]` (or use `usize` throughout).
- `x`, `y: Vec<f64>` — length `numpoints`, 0-based indices for point i+1 vs the Pascal spec.
- `parameters: Parameters` — see field names below (Rust **snake_case** only in source code).
- `lcm: Vec<Vec<String>>` — 15×15, symmetric; each off-diagonal entry is exactly one of
  `"NOTUSED"`, `"ORR"`, `"ANDD"`.
- `pum_diag: Vec<bool>` — length 15; diagonal PUM for LIC 1..15.

`Parameters` (access with `input.parameters.<field>`). Floating-point fields: `length1`,
`radius1`, `epsilon`, `area1`, `dist`, `length2`, `radius2`, `area2`. Integer/count fields
(all **usize**): `q_pts`, `quads`, `n_pts`, `k_pts`, `a_pts`, `b_pts`, `c_pts`, `d_pts`,
`e_pts`, `f_pts`, `g_pts`.

Wire JSON uses Pascal-style keys (`LENGTH1`, `Q_PTS`, …); serde maps them to these Rust
names. **Do not** use `LENGTH1`, `Q_PTS`, or other Pascal names as Rust identifiers — they
will not compile.

`DecideOutput` fields (lengths are mandatory):
- `cmv: Vec<bool>` — length 15
- `pum: Vec<Vec<bool>>` — 15 rows, each length 15
- `fuv: Vec<bool>` — length 15
- `launch: bool`

Build them with `vec![false; 15]`, nested `vec!`, or collect from iterators. If you compute
fixed arrays `[bool; 15]` and `[[bool; 15]; 15]`, either convert rows with `.to_vec()` or return
using the harness helper (import `DecideOutput` from `crate::types`):

  `DecideOutput::from_fixed(cmv, pum, fuv, launch)`

Do **not** return bare `[bool; 15]` where a `Vec<bool>` is required unless you convert.

## Real comparisons

Implement `realcompare(a: f64, b: f64) -> &'static str` returning exactly `"LT"`, `"EQ"`,
or `"GT"` per the six-significant-digit rule in `spec.md`. Use it everywhere the spec
requires real comparisons.

The specification is in: {spec_path}

Write your implementation to: {output_path}
"""


class RustHarness(LanguageHarness):
    name = "rust"

    @property
    def output_filename(self) -> str:
        return "decide.rs"

    def build_prompt(self, spec_path: str, output_path: str) -> str:
        return RUST_TASK_PROMPT_TEMPLATE.format(spec_path=spec_path, output_path=output_path)

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
        exe = work_dir / "target" / "release" / ("lip_harness.exe" if os.name == "nt" else "lip_harness")
        if r.returncode != 0 or not exe.exists():
            parts = [p for p in (r.stderr or "", r.stdout or "") if p and p.strip()]
            msg = "\n".join(s.strip() for s in parts)
            if not msg:
                msg = f"cargo build exited with code {r.returncode} (no output)"
            return None, msg
        return exe, ""

    @staticmethod
    def _materialize_project(work_dir: Path, decide_rs: str) -> None:
        """Copy harness sources and inject agent decide.rs."""
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
