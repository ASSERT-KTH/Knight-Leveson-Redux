"""
Structured comparison of Launch Interceptor `decide` outputs (241 bits).

Used by the campaign fault log and for tests.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class PackedDecideOutput:
    cmv_bits: int
    pum_rows: tuple[int, ...]
    fuv_bits: int
    launch_bit: int


def pack_bool_vector(values: list[bool] | tuple[bool, ...], *, width: int = 15) -> int:
    if len(values) != width:
        raise ValueError(f"expected {width} booleans, got {len(values)}")
    bits = 0
    for idx, value in enumerate(values):
        if bool(value):
            bits |= 1 << idx
    return bits


def unpack_bool_vector(bits: int, *, width: int = 15) -> list[bool]:
    return [bool((bits >> idx) & 1) for idx in range(width)]


def pack_pum_rows(pum: list[list[bool]] | tuple[list[bool], ...], *, width: int = 15) -> tuple[int, ...]:
    if len(pum) != width:
        raise ValueError(f"expected {width} PUM rows, got {len(pum)}")
    return tuple(pack_bool_vector(list(row), width=width) for row in pum)


def unpack_pum_rows(rows: tuple[int, ...] | list[int], *, width: int = 15) -> list[list[bool]]:
    if len(rows) != width:
        raise ValueError(f"expected {width} packed PUM rows, got {len(rows)}")
    return [unpack_bool_vector(int(row), width=width) for row in rows]


def pack_decide_output(
    output: tuple[list[bool], list[list[bool]], list[bool], bool],
) -> PackedDecideOutput:
    cmv, pum, fuv, launch = output
    return PackedDecideOutput(
        cmv_bits=pack_bool_vector(list(cmv)),
        pum_rows=pack_pum_rows(list(pum)),
        fuv_bits=pack_bool_vector(list(fuv)),
        launch_bit=int(bool(launch)),
    )


def unpack_decide_output(
    packed: PackedDecideOutput,
) -> tuple[list[bool], list[list[bool]], list[bool], bool]:
    return (
        unpack_bool_vector(packed.cmv_bits),
        unpack_pum_rows(packed.pum_rows),
        unpack_bool_vector(packed.fuv_bits),
        bool(packed.launch_bit),
    )


def pack_case_expected_output(case: dict[str, Any]) -> PackedDecideOutput:
    return pack_decide_output((case["cmv"], case["pum"], case["fuv"], case["launch"]))


def packed_output_digest(packed: PackedDecideOutput) -> int:
    h = hashlib.blake2b(digest_size=8)
    h.update(int(packed.cmv_bits).to_bytes(2, "little", signed=False))
    for row_bits in packed.pum_rows:
        h.update(int(row_bits).to_bytes(2, "little", signed=False))
    h.update(int(packed.fuv_bits).to_bytes(2, "little", signed=False))
    h.update(int(packed.launch_bit).to_bytes(1, "little", signed=False))
    return int.from_bytes(h.digest(), "little", signed=False)


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
