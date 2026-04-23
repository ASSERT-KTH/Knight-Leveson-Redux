"""
Stable, filesystem-safe names for version artifacts.

Pattern:  {agent}__m_{model_slug}__l_{language}__run{NNN}.json

``runs`` in experiment config applies **per model** and **per language**; each
(model, language) pair gets run IDs ``0 .. runs-1``.
"""
from __future__ import annotations

import re
from typing import Any


def _normalize_model_for_agent(agent_name: str, model: str | None) -> str:
    """
    Normalize model names before slugging.

    For `claude_code`, drop OpenRouter-style provider prefixes such as
    `anthropic/`, `google/`, and `moonshot/` so filenames stay compact.
    """
    s = model if model is not None else "default"
    if not isinstance(s, str):
        s = str(s)
    s = s.strip() or "default"

    if agent_name == "claude_code" and "/" in s:
        provider, remainder = s.split("/", 1)
        if provider in {"anthropic", "google", "moonshot", "openai"} and remainder:
            s = remainder

    return s


def slug_model(model: str | None) -> str:
    """Turn a config model string into a single path segment (no slashes)."""
    s = model if model is not None else "default"
    if not isinstance(s, str):
        s = str(s)
    s = s.strip() or "default"
    s = s.replace("/", "__").replace("\\", "_")
    s = re.sub(r"[^a-zA-Z0-9._+-]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("._-") or "default"
    if len(s) > 64:
        s = s[:64].rstrip("._-") or "default"
    return s


def slug_language(language: str | None) -> str:
    s = (language or "python").strip().lower() or "python"
    s = re.sub(r"[^a-z0-9._+-]+", "_", s).strip("._-") or "python"
    return s[:16] if len(s) > 16 else s


def version_json_filename(
    agent_name: str,
    model_config: str | None,
    run_id: int,
    *,
    language: str = "python",
) -> str:
    normalized_model = _normalize_model_for_agent(agent_name, model_config)
    return (
        f"{agent_name}__m_{slug_model(normalized_model)}__l_{slug_language(language)}__run{run_id:03d}.json"
    )


def version_id_from_filename(filename: str) -> str:
    """Stem of the JSON file = version_id used in campaign CSV."""
    return filename.removesuffix(".json")


def models_from_agent_config(inner: dict[str, Any]) -> list[str | None]:
    """
    Models to generate for one agent block. ``runs`` (outside ``config``) is
    applied to **each** entry here.

    - ``config.models: [m1, m2, ...]`` or a single string
    - Legacy: ``config.model: m`` → ``[m]``
    - Neither → ``[None]`` (CLI / adapter default)
    """
    if not isinstance(inner, dict):
        inner = {}
    raw = inner.get("models")
    if raw is not None:
        if isinstance(raw, str):
            seq: list[Any] = [raw]
        elif isinstance(raw, list):
            seq = raw
        else:
            raise ValueError("config.models must be a string or a list")
        if len(seq) == 0:
            raise ValueError("config.models must not be an empty list")
        out: list[str | None] = []
        for item in seq:
            if item is None:
                out.append(None)
            else:
                s = str(item).strip()
                out.append(s if s else None)
        return out
    if "model" in inner:
        m = inner.get("model")
        if m is None:
            return [None]
        s = str(m).strip()
        return [s if s else None]
    return [None]
