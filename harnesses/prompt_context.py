"""
Shared prompt context for agent version generation.
"""
from __future__ import annotations

import shutil
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parents[1]
_PROMPT_EXAMPLES_PATH = _REPO_ROOT / "benchmarks" / "launch_interceptor" / "prompt_examples.json"

REFERENCE_EXAMPLES_FILENAME = "prompt_examples.json"
_REFERENCE_REALCOMPARE_FILENAMES = {
    "python": "realcompare_reference.py",
    "pascal": "realcompare_reference.pas",
    "rust": "realcompare_reference.rs",
}

_PYTHON_REALCOMPARE_SNIPPET = '''\
def realcompare(a: float, b: float) -> str:
    """Tolerance-based six-significant-digit comparison from the oracle."""
    scale = max(abs(a), abs(b))
    if scale == 0.0:
        return "EQ"
    eps = 0.5e-5 * scale
    diff = a - b
    if diff > eps:
        return "GT"
    if diff < -eps:
        return "LT"
    return "EQ"
'''

_PASCAL_REALCOMPARE_SNIPPET = '''\
function REALCOMPARE(A, B: real): COMPTYPE;
var
  scale, eps, diff: real;
begin
  scale := Abs(A);
  if Abs(B) > scale then
    scale := Abs(B);
  if scale = 0.0 then
  begin
    REALCOMPARE := EQ;
    Exit;
  end;

  eps := 0.5e-5 * scale;
  diff := A - B;
  if diff > eps then
    REALCOMPARE := GT
  else if diff < -eps then
    REALCOMPARE := LT
  else
    REALCOMPARE := EQ;
end;
'''

_RUST_REALCOMPARE_SNIPPET = '''\
pub const LT: &str = "LT";
pub const EQ: &str = "EQ";
pub const GT: &str = "GT";

pub fn realcompare(a: f64, b: f64) -> &'static str {
    let scale = a.abs().max(b.abs());
    if scale == 0.0 {
        return "EQ";
    }
    let eps = 0.5e-5 * scale;
    let diff = a - b;
    if diff > eps {
        "GT"
    } else if diff < -eps {
        "LT"
    } else {
        "EQ"
    }
}
'''

_REALCOMPARE_BY_LANGUAGE = {
    "python": {
        "source_path": "harnesses-realcompare/python_harness.py",
        "filename": _REFERENCE_REALCOMPARE_FILENAMES["python"],
        "snippet": _PYTHON_REALCOMPARE_SNIPPET,
    },
    "pascal": {
        "source_path": "harnesses-realcompare/pascal/globals.pas",
        "filename": _REFERENCE_REALCOMPARE_FILENAMES["pascal"],
        "snippet": _PASCAL_REALCOMPARE_SNIPPET,
    },
    "rust": {
        "source_path": "harnesses-realcompare/rust/src/types.rs",
        "filename": _REFERENCE_REALCOMPARE_FILENAMES["rust"],
        "snippet": _RUST_REALCOMPARE_SNIPPET,
    },
}


def provision_reference_files(sandbox: Path, language: str) -> None:
    lang = language.lower().strip()
    sandbox.mkdir(parents=True, exist_ok=True)
    shutil.copy2(_PROMPT_EXAMPLES_PATH, sandbox / REFERENCE_EXAMPLES_FILENAME)
    info = _REALCOMPARE_BY_LANGUAGE[lang]
    (sandbox / info["filename"]).write_text(info["snippet"], encoding="utf-8")


def build_reference_context(language: str) -> str:
    lang = language.lower().strip()
    info = _REALCOMPARE_BY_LANGUAGE[lang]
    return (
        "Reference material is available in your workspace:\n"
        f"- Read `{REFERENCE_EXAMPLES_FILENAME}` for 15 oracle-backed correct input/output examples.\n"
        "- Each example contains the full input and the full expected output object "
        "(`cmv`, `pum`, `fuv`, `launch`).\n"
        f"- Read `{info['filename']}` for a working `realcompare` implementation derived from "
        f"`{info['source_path']}`. Treat that implementation as fixed reference behavior: do not modify its logic.\n"
    )
