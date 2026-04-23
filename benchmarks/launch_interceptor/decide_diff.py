"""
Structured comparison of Launch Interceptor `decide` outputs (241 bits).

Used by the campaign fault log and for tests.
"""
from __future__ import annotations

from typing import Any


def diff_decide_outputs(
    expected: tuple[list[bool], list[list[bool]], list[bool], bool],
    actual: Any,
    *,
    detail: str = "summary",
) -> dict[str, Any]:
    """
    Compare oracle expected tuple to a candidate result.

    Parameters
    ----------
    expected
        (cmv, pum, fuv, launch) from the reference implementation.
    actual
        Candidate return value; may be malformed.
    detail
        ``summary`` — indices/cells where bits differ, plus launch flag.
        ``full`` — also include full expected and actual CMV, PUM, FUV, launch
        when shapes are valid.
    """
    exp_cmv, exp_pum, exp_fuv, exp_launch = expected
    out: dict[str, Any] = {
        "cmv_mismatch_indices": [],
        "pum_mismatch_cells": [],
        "fuv_mismatch_indices": [],
        "launch_mismatch": False,
        "malformed_actual": False,
    }

    if not isinstance(actual, tuple) or len(actual) != 4:
        out["malformed_actual"] = True
        return out

    act_cmv, act_pum, act_fuv, act_launch = actual

    try:
        for i in range(15):
            if list(exp_cmv)[i] != list(act_cmv)[i]:
                out["cmv_mismatch_indices"].append(i)
        for i in range(15):
            for j in range(15):
                if list(exp_pum[i])[j] != list(act_pum[i])[j]:
                    out["pum_mismatch_cells"].append([i, j])
        for i in range(15):
            if list(exp_fuv)[i] != list(act_fuv)[i]:
                out["fuv_mismatch_indices"].append(i)
        out["launch_mismatch"] = bool(exp_launch) != bool(act_launch)
    except (TypeError, ValueError, IndexError):
        out["malformed_actual"] = True
        return out

    if detail == "full" and not out["malformed_actual"]:
        out["expected_cmv"] = [bool(x) for x in exp_cmv]
        out["actual_cmv"] = [bool(x) for x in act_cmv]
        out["expected_pum"] = [[bool(x) for x in row] for row in exp_pum]
        out["actual_pum"] = [[bool(x) for x in row] for row in act_pum]
        out["expected_fuv"] = [bool(x) for x in exp_fuv]
        out["actual_fuv"] = [bool(x) for x in act_fuv]
        out["expected_launch"] = bool(exp_launch)
        out["actual_launch"] = bool(act_launch)

    return out


def campaign_inputs_only(case: dict[str, Any]) -> dict[str, Any]:
    """Strip oracle fields from a generator case for logging."""
    return {
        "numpoints": case["numpoints"],
        "x": case["x"],
        "y": case["y"],
        "parameters": case["parameters"],
        "lcm": case["lcm"],
        "pum_diag": case["pum_diag"],
    }


def recompute_pum_from_cmv(
    cmv: list[bool],
    lcm: list[list[str]],
    pum_diag: list[bool],
) -> list[list[bool]]:
    """PUM from CMV and LCM per Knight & Leveson (spec connector semantics)."""
    pum: list[list[bool]] = [[False] * 15 for _ in range(15)]
    for i in range(15):
        for j in range(15):
            if i == j:
                pum[i][j] = pum_diag[i]
            else:
                conn = lcm[i][j]
                if conn == "NOTUSED":
                    pum[i][j] = True
                elif conn == "ANDD":
                    pum[i][j] = cmv[i] and cmv[j]
                elif conn == "ORR":
                    pum[i][j] = cmv[i] or cmv[j]
                else:
                    raise ValueError(f"Unknown LCM connector: {conn!r}")
    return pum


def recompute_fuv_from_pum(pum: list[list[bool]]) -> list[bool]:
    """FUV from PUM per spec."""
    fuv: list[bool] = []
    for i in range(15):
        if not pum[i][i]:
            fuv.append(True)
        else:
            fuv.append(all(pum[i][j] for j in range(15)))
    return fuv
