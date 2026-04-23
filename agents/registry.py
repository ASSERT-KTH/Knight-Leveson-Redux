"""Agent registry — maps agent names to adapter classes."""
from __future__ import annotations

from agents.claude_code_agent import ClaudeCodeAgent
from agents.codex_agent import CodexAgent
from agents.cursor_agent import CursorAgent
from agents.gemini_agent import GeminiAgent
from agents.mock_agent import MockAgent
from agents.opencode_agent import OpenCodeAgent

REGISTRY: dict[str, type] = {
    "cursor": CursorAgent,
    "claude_code": ClaudeCodeAgent,
    "codex": CodexAgent,
    "gemini": GeminiAgent,
    "opencode": OpenCodeAgent,
    "mock": MockAgent,
}


def get_agent(name: str, config: dict | None = None):
    if name not in REGISTRY:
        raise ValueError(f"Unknown agent: {name!r}. Available: {list(REGISTRY)}")
    return REGISTRY[name](config)
