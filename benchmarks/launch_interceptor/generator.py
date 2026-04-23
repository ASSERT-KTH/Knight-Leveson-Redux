"""
Reproducible random test-case generator for the Launch Interceptor Program.

Each test case is a dict with the inputs to decide() and the oracle outputs.
Uses numpy.random.default_rng for reproducibility.
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path
from typing import Any, Iterator

import numpy as np

# Allow imports from repo root
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

PI = math.pi
CONNECTORS = ["NOTUSED", "ORR", "ANDD"]


def _random_parameters(rng: np.random.Generator, numpoints: int) -> dict[str, Any]:
    """Generate a random PARAMETERS record consistent with spec constraints."""
    length1 = float(rng.uniform(0, 20))
    radius1 = float(rng.uniform(0, 10))
    epsilon = float(rng.uniform(0, PI - 1e-9))
    area1 = float(rng.uniform(0, 50))
    q_pts = int(rng.integers(2, max(3, numpoints + 1)))
    quads = int(rng.integers(1, 4))
    dist = float(rng.uniform(0, 20))
    n_pts = int(rng.integers(3, max(4, numpoints + 1)))
    k_pts = int(rng.integers(1, max(2, numpoints - 1)))
    # A_PTS + B_PTS <= numpoints - 3 and both >= 1
    max_ab = max(2, numpoints - 3)
    a_pts = int(rng.integers(1, max(2, max_ab)))
    b_pts = int(rng.integers(1, max(2, max_ab - a_pts + 1)))
    c_pts = int(rng.integers(1, max(2, numpoints - 2)))
    d_pts = int(rng.integers(1, max(2, numpoints - 2 - c_pts + 1)))
    e_pts = int(rng.integers(1, max(2, numpoints - 2)))
    f_pts = int(rng.integers(1, max(2, numpoints - 2 - e_pts + 1)))
    g_pts = int(rng.integers(1, max(2, numpoints - 1)))
    length2 = float(rng.uniform(0, 20))
    radius2 = float(rng.uniform(0, 10))
    area2 = float(rng.uniform(0, 50))

    # Clamp to valid ranges
    k_pts = min(k_pts, numpoints - 2)
    g_pts = min(g_pts, numpoints - 2)
    a_pts = min(a_pts, max(1, numpoints - 3))
    b_pts = min(b_pts, max(1, numpoints - 3 - a_pts))
    c_pts = min(c_pts, max(1, numpoints - 3))
    d_pts = min(d_pts, max(1, numpoints - 3 - c_pts))
    e_pts = min(e_pts, max(1, numpoints - 3))
    f_pts = min(f_pts, max(1, numpoints - 3 - e_pts))
    q_pts = min(q_pts, numpoints)
    n_pts = min(n_pts, numpoints)

    return {
        "LENGTH1": length1,
        "RADIUS1": radius1,
        "EPSILON": epsilon,
        "AREA1": area1,
        "Q_PTS": q_pts,
        "QUADS": quads,
        "DIST": dist,
        "N_PTS": n_pts,
        "K_PTS": k_pts,
        "A_PTS": a_pts,
        "B_PTS": b_pts,
        "C_PTS": c_pts,
        "D_PTS": d_pts,
        "E_PTS": e_pts,
        "F_PTS": f_pts,
        "G_PTS": g_pts,
        "LENGTH2": length2,
        "RADIUS2": radius2,
        "AREA2": area2,
    }


def _random_lcm(rng: np.random.Generator) -> list[list[str]]:
    """Generate a random symmetric 15x15 LCM."""
    lcm: list[list[str]] = [["NOTUSED"] * 15 for _ in range(15)]
    for i in range(15):
        for j in range(i + 1, 15):
            val = CONNECTORS[int(rng.integers(0, 3))]
            lcm[i][j] = val
            lcm[j][i] = val
    return lcm


def _random_pum_diag(rng: np.random.Generator) -> list[bool]:
    """Generate random diagonal PUM elements."""
    return [bool(rng.integers(0, 2)) for _ in range(15)]


def iter_test_cases(
    n: int,
    seed: int,
    include_oracle_outputs: bool = False,
) -> Iterator[dict[str, Any]]:
    """
    Yield n reproducible random test cases.

    This is the memory-efficient primitive used by both acceptance and
    campaign generation. It avoids materializing very large case lists.
    """
    rng = np.random.default_rng(seed)

    oracle = None
    if include_oracle_outputs:
        from oracle.launch_interceptor.solution import decide as oracle_decide
        oracle = oracle_decide

    for _ in range(n):
        numpoints = int(rng.integers(2, 101))
        x = [float(v) for v in rng.uniform(-100, 100, size=numpoints)]
        y = [float(v) for v in rng.uniform(-100, 100, size=numpoints)]
        parameters = _random_parameters(rng, numpoints)
        lcm = _random_lcm(rng)
        pum_diag = _random_pum_diag(rng)

        case: dict[str, Any] = {
            "numpoints": numpoints,
            "x": x,
            "y": y,
            "parameters": parameters,
            "lcm": lcm,
            "pum_diag": pum_diag,
        }

        if oracle is not None:
            cmv, pum, fuv, launch = oracle(numpoints, x, y, parameters, lcm, pum_diag)
            case["cmv"] = cmv
            case["pum"] = pum
            case["fuv"] = fuv
            case["launch"] = launch

        yield case


def generate_test_cases(
    n: int,
    seed: int,
    include_oracle_outputs: bool = False,
) -> list[dict[str, Any]]:
    """
    Generate n reproducible random test cases as a list.

    Use `iter_test_cases()` for large campaigns to avoid OOM.
    """
    return list(iter_test_cases(n, seed, include_oracle_outputs))


def generate_acceptance_cases(seed: int, n: int = 50) -> list[dict[str, Any]]:
    """
    Generate acceptance test cases (with oracle outputs).
    Uses seed offset to keep acceptance cases distinct from campaign cases.
    """
    return generate_test_cases(n, seed=seed + 1000, include_oracle_outputs=True)


def generate_campaign_cases(seed: int, n: int = 1000) -> list[dict[str, Any]]:
    """
    Generate main campaign test cases (with oracle outputs).
    """
    return generate_test_cases(n, seed=seed, include_oracle_outputs=True)


def iter_campaign_cases(seed: int, n: int = 1000) -> Iterator[dict[str, Any]]:
    """Yield main campaign test cases (with oracle outputs)."""
    yield from iter_test_cases(n, seed=seed, include_oracle_outputs=True)


if __name__ == "__main__":
    import json
    import argparse

    parser = argparse.ArgumentParser(description="Generate LIP test cases")
    parser.add_argument("--n", type=int, default=10, help="Number of test cases")
    parser.add_argument("--seed", type=int, default=42, help="RNG seed")
    parser.add_argument("--mode", choices=["acceptance", "campaign", "raw"], default="raw")
    parser.add_argument("--output", type=str, default=None, help="Output JSON file")
    args = parser.parse_args()

    if args.mode == "acceptance":
        cases = generate_acceptance_cases(args.seed, args.n)
    elif args.mode == "campaign":
        cases = generate_campaign_cases(args.seed, args.n)
    else:
        cases = generate_test_cases(args.n, args.seed, include_oracle_outputs=True)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(cases, f, indent=2)
        print(f"Wrote {len(cases)} cases to {args.output}")
    else:
        print(json.dumps(cases[:2], indent=2))
        print(f"... ({len(cases)} total cases)")
