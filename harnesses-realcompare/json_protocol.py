"""
JSON-lines wire format shared by Python orchestration and native harness binaries.

One input object per line (stdin); one output object per line (stdout).
"""
from __future__ import annotations

import json
from typing import Any


def case_to_json_line(case: dict[str, Any]) -> str:
    """Serialize campaign/acceptance case inputs (no oracle fields required)."""
    payload = {
        "numpoints": case["numpoints"],
        "x": case["x"],
        "y": case["y"],
        "parameters": case["parameters"],
        "lcm": case["lcm"],
        "pum_diag": case["pum_diag"],
    }
    return json.dumps(payload, separators=(",", ":"))


def parse_output_line(line: str) -> tuple[list[bool], list[list[bool]], list[bool], bool]:
    """Parse harness output JSON into the same shapes as Python decide()."""
    line = line.strip()
    if not line:
        raise ValueError("empty output line")
    obj = json.loads(line)
    cmv = [bool(x) for x in obj["cmv"]]
    pum = [[bool(x) for x in row] for row in obj["pum"]]
    fuv = [bool(x) for x in obj["fuv"]]
    launch = bool(obj["launch"])
    if len(cmv) != 15 or len(fuv) != 15 or len(pum) != 15:
        raise ValueError("wrong vector lengths")
    for row in pum:
        if len(row) != 15:
            raise ValueError("wrong PUM shape")
    return cmv, pum, fuv, launch
