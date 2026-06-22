"""
Language harnesses for Python, Pascal (fpc), and Rust candidates.
"""
from __future__ import annotations

from harnesses.base import LanguageHarness
from harnesses.pascal_harness import PascalHarness
from harnesses.python_harness import PythonHarness
from harnesses.rust_harness import RustHarness

_REGISTRY: dict[str, LanguageHarness] = {
    "python": PythonHarness(),
    "pascal": PascalHarness(),
    "rust": RustHarness(),
}


def get_harness(language: str | None) -> LanguageHarness:
    key = (language or "python").lower().strip()
    if key not in _REGISTRY:
        raise ValueError(f"unknown language: {language!r} (expected python|pascal|rust)")
    return _REGISTRY[key]


def normalize_languages(raw: object | None) -> list[str]:
    """Config `languages:` list; default ``['python']`` for backward compatibility."""
    if raw is None:
        return ["python"]
    if isinstance(raw, str):
        return [raw.lower().strip()]
    if isinstance(raw, list):
        if len(raw) == 0:
            raise ValueError("languages must not be an empty list")
        out: list[str] = []
        for x in raw:
            s = str(x).lower().strip()
            if s not in _REGISTRY:
                raise ValueError(f"unknown language in list: {x!r}")
            out.append(s)
        return out
    raise ValueError("languages must be a string or a list of strings")


__all__ = [
    "LanguageHarness",
    "PascalHarness",
    "PythonHarness",
    "RustHarness",
    "get_harness",
    "normalize_languages",
]
