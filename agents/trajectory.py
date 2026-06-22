"""
Helpers for capturing agent CLI trajectories.
"""
from __future__ import annotations

import json
from typing import Any


DEFAULT_TRAJECTORY_NOTE = (
    "Captured provider-exposed CLI output and structured events when available. "
    "Private chain-of-thought reasoning is not available from these adapters."
)


def parse_jsonl_events(text: str, *, stream: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for idx, line in enumerate((text or "").splitlines()):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            payload = json.loads(stripped)
        except json.JSONDecodeError:
            events.append({
                "stream": stream,
                "index": idx,
                "format": "text",
                "text": line,
            })
            continue
        if isinstance(payload, dict):
            event = dict(payload)
            event.setdefault("stream", stream)
            event.setdefault("index", idx)
            events.append(event)
        else:
            events.append({
                "stream": stream,
                "index": idx,
                "format": "json",
                "payload": payload,
            })
    return events


def parse_json_or_jsonl_output(text: str, *, stream: str) -> list[dict[str, Any]]:
    blob = (text or "").strip()
    if not blob:
        return []
    try:
        payload = json.loads(blob)
    except json.JSONDecodeError:
        return parse_jsonl_events(text, stream=stream)

    if isinstance(payload, dict):
        event = dict(payload)
        event.setdefault("stream", stream)
        event.setdefault("index", 0)
        return [event]
    if isinstance(payload, list):
        events: list[dict[str, Any]] = []
        for idx, item in enumerate(payload):
            if isinstance(item, dict):
                event = dict(item)
                event.setdefault("stream", stream)
                event.setdefault("index", idx)
                events.append(event)
            else:
                events.append({
                    "stream": stream,
                    "index": idx,
                    "format": "json",
                    "payload": item,
                })
        return events
    return [{
        "stream": stream,
        "index": 0,
        "format": "json",
        "payload": payload,
    }]
