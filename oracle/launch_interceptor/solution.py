"""
Trusted oracle — reference implementation of the Launch Interceptor Program.

This is the "gold program" analogous to the one used in Knight & Leveson (1986).
It has been independently written and thoroughly tested.

Correctness rationale
---------------------
Each LIC is implemented directly from the spec with explicit handling of every
edge case described (coincident points, degenerate triangles, NUMPOINTS thresholds).
Real-number comparisons use realcompare() throughout.
The smallest enclosing circle uses the classic Welzl / circumscribed-circle
approach: for three points, check whether the circumscribed circle fits, or
whether the longest edge is a diameter.
"""
from __future__ import annotations

import math
from typing import Any

PI = math.pi


# ---------------------------------------------------------------------------
# Real-number comparison (6 significant digits, per spec)
# ---------------------------------------------------------------------------

def realcompare(a: float, b: float) -> str:
    """
    Compare two reals to 6 significant digits.
    Returns 'LT', 'EQ', or 'GT'.

    Uses the same linear tolerance as the Pascal REALCOMPARE in K&L
    (``eps := 0.5e-5 * scale`` after ``scale := max(abs(A), abs(B))``), but **without**
    flooring ``scale`` at 1: for |a|,|b| < 1 the tolerance scales with magnitude so
    small values are still compared at six-significant-digit resolution.
    """
    scale = max(abs(a), abs(b))
    if scale == 0.0:
        return "EQ"
    eps = 0.5e-5 * scale  # half a unit in the 6th significant digit at this scale
    diff = a - b
    if diff > eps:
        return "GT"
    if diff < -eps:
        return "LT"
    return "EQ"


def rc_lt(a: float, b: float) -> bool:
    return realcompare(a, b) == "LT"


def rc_gt(a: float, b: float) -> bool:
    return realcompare(a, b) == "GT"


def rc_eq(a: float, b: float) -> bool:
    return realcompare(a, b) == "EQ"


def rc_le(a: float, b: float) -> bool:
    return realcompare(a, b) in ("LT", "EQ")


def rc_ge(a: float, b: float) -> bool:
    return realcompare(a, b) in ("GT", "EQ")


# ---------------------------------------------------------------------------
# Geometric helpers
# ---------------------------------------------------------------------------

def _dist(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def _triangle_area(
    x1: float, y1: float,
    x2: float, y2: float,
    x3: float, y3: float,
) -> float:
    """Signed area * 2 of triangle; take abs / 2."""
    return abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) / 2.0


def _circumscribed_radius(
    x1: float, y1: float,
    x2: float, y2: float,
    x3: float, y3: float,
) -> float:
    """
    Radius of the smallest circle that encloses / passes through three points.

    Strategy:
    - If the triangle is obtuse (or degenerate/collinear), the smallest
      enclosing circle has the longest side as its diameter.
    - Otherwise (acute), use the circumscribed circle.
    """
    a = _dist(x2, y2, x3, y3)
    b = _dist(x1, y1, x3, y3)
    c = _dist(x1, y1, x2, y2)

    # Collinear / degenerate: longest edge / 2
    area2 = abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))
    if rc_eq(area2, 0.0):
        return max(a, b, c) / 2.0

    # Check if obtuse by comparing longest side² with sum of the other two²
    sides = sorted([a, b, c])
    s0, s1, s2 = sides  # s2 is longest
    if rc_ge(s2 * s2, s0 * s0 + s1 * s1):
        # Obtuse or right: diameter = longest side
        return s2 / 2.0

    # Acute: circumscribed radius = (a*b*c) / (4 * area)
    area = area2 / 2.0
    return (a * b * c) / (4.0 * area)


def _point_to_line_dist(
    px: float, py: float,
    x1: float, y1: float,
    x2: float, y2: float,
) -> float:
    """Perpendicular distance from point (px,py) to line through (x1,y1)-(x2,y2)."""
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx * dx + dy * dy)
    if rc_eq(length, 0.0):
        return _dist(px, py, x1, y1)
    return abs(dx * (y1 - py) - (x1 - px) * dy) / length


def _angle_at_vertex(
    x1: float, y1: float,
    vx: float, vy: float,
    x3: float, y3: float,
) -> float | None:
    """
    Angle at vertex (vx,vy) formed by rays to (x1,y1) and (x3,y3).
    Returns None if either (x1,y1) or (x3,y3) coincides with the vertex.
    """
    if rc_eq(_dist(x1, y1, vx, vy), 0.0) or rc_eq(_dist(x3, y3, vx, vy), 0.0):
        return None
    # Vectors from vertex
    ux, uy = x1 - vx, y1 - vy
    wx, wy = x3 - vx, y3 - vy
    dot = ux * wx + uy * wy
    cross_mag = math.sqrt((ux * ux + uy * uy) * (wx * wx + wy * wy))
    if rc_eq(cross_mag, 0.0):
        return None
    cos_a = max(-1.0, min(1.0, dot / cross_mag))
    return math.acos(cos_a)


def _quadrant(px: float, py: float) -> int:
    """
    Quadrant by priority rule (spec LIC 5):
    Q1: x>=0 and y>=0  (includes both axes and origin)
    Q2: x<0  and y>=0
    Q3: x<=0 and y<0
    Q4: x>0  and y<0
    """
    if px >= 0 and py >= 0:
        return 1
    if px < 0 and py >= 0:
        return 2
    if px <= 0 and py < 0:
        return 3
    return 4


# ---------------------------------------------------------------------------
# Individual LIC implementations
# ---------------------------------------------------------------------------

def _lic1(x: list[float], y: list[float], numpoints: int, params: dict) -> bool:
    """LIC 1: two consecutive points > LENGTH1 apart."""
    l1 = params["LENGTH1"]
    for i in range(numpoints - 1):
        if rc_gt(_dist(x[i], y[i], x[i + 1], y[i + 1]), l1):
            return True
    return False


def _lic2(x: list[float], y: list[float], numpoints: int, params: dict) -> bool:
    """LIC 2: three consecutive points not all inside/on circle of RADIUS1."""
    r1 = params["RADIUS1"]
    for i in range(numpoints - 2):
        r = _circumscribed_radius(x[i], y[i], x[i + 1], y[i + 1], x[i + 2], y[i + 2])
        if rc_gt(r, r1):
            return True
    return False


def _lic3(x: list[float], y: list[float], numpoints: int, params: dict) -> bool:
    """LIC 3: three consecutive points form angle outside [PI-EPSILON, PI+EPSILON]."""
    eps = params["EPSILON"]
    for i in range(numpoints - 2):
        angle = _angle_at_vertex(x[i], y[i], x[i + 1], y[i + 1], x[i + 2], y[i + 2])
        if angle is None:
            continue
        if rc_lt(angle, PI - eps) or rc_gt(angle, PI + eps):
            return True
    return False


def _lic4(x: list[float], y: list[float], numpoints: int, params: dict) -> bool:
    """LIC 4: three consecutive points form triangle with area > AREA1."""
    a1 = params["AREA1"]
    for i in range(numpoints - 2):
        area = _triangle_area(x[i], y[i], x[i + 1], y[i + 1], x[i + 2], y[i + 2])
        if rc_gt(area, a1):
            return True
    return False


def _lic5(x: list[float], y: list[float], numpoints: int, params: dict) -> bool:
    """LIC 5: Q_PTS consecutive points in more than QUADS quadrants."""
    q_pts = params["Q_PTS"]
    quads = params["QUADS"]
    for i in range(numpoints - q_pts + 1):
        seen = set()
        for j in range(q_pts):
            seen.add(_quadrant(x[i + j], y[i + j]))
        if len(seen) > quads:
            return True
    return False


def _lic6(x: list[float], y: list[float], numpoints: int, params: dict) -> bool:
    """LIC 6: two consecutive points with x[j]-x[i] < 0."""
    for i in range(numpoints - 1):
        if rc_lt(x[i + 1] - x[i], 0.0):
            return True
    return False


def _lic7(x: list[float], y: list[float], numpoints: int, params: dict) -> bool:
    """LIC 7: N_PTS consecutive points with one point > DIST from first-last line."""
    if numpoints < 3:
        return False
    n_pts = params["N_PTS"]
    dist = params["DIST"]
    for i in range(numpoints - n_pts + 1):
        x1, y1 = x[i], y[i]
        x2, y2 = x[i + n_pts - 1], y[i + n_pts - 1]
        coincident = rc_eq(_dist(x1, y1, x2, y2), 0.0)
        for k in range(1, n_pts - 1):
            if coincident:
                d = _dist(x[i + k], y[i + k], x1, y1)
            else:
                d = _point_to_line_dist(x[i + k], y[i + k], x1, y1, x2, y2)
            if rc_gt(d, dist):
                return True
    return False


def _lic8(x: list[float], y: list[float], numpoints: int, params: dict) -> bool:
    """LIC 8: two points separated by K_PTS intervening points > LENGTH1 apart."""
    if numpoints < 3:
        return False
    k_pts = params["K_PTS"]
    l1 = params["LENGTH1"]
    for i in range(numpoints - k_pts - 1):
        j = i + k_pts + 1
        if rc_gt(_dist(x[i], y[i], x[j], y[j]), l1):
            return True
    return False


def _lic9(x: list[float], y: list[float], numpoints: int, params: dict) -> bool:
    """LIC 9: three points separated by A_PTS, B_PTS not in circle of RADIUS1."""
    if numpoints < 5:
        return False
    a_pts = params["A_PTS"]
    b_pts = params["B_PTS"]
    r1 = params["RADIUS1"]
    for i in range(numpoints - a_pts - b_pts - 2):
        j = i + a_pts + 1
        k = j + b_pts + 1
        r = _circumscribed_radius(x[i], y[i], x[j], y[j], x[k], y[k])
        if rc_gt(r, r1):
            return True
    return False


def _lic10(x: list[float], y: list[float], numpoints: int, params: dict) -> bool:
    """LIC 10: three points separated by C_PTS, D_PTS with angle outside EPSILON band."""
    if numpoints < 5:
        return False
    c_pts = params["C_PTS"]
    d_pts = params["D_PTS"]
    eps = params["EPSILON"]
    for i in range(numpoints - c_pts - d_pts - 2):
        j = i + c_pts + 1
        k = j + d_pts + 1
        angle = _angle_at_vertex(x[i], y[i], x[j], y[j], x[k], y[k])
        if angle is None:
            continue
        if rc_lt(angle, PI - eps) or rc_gt(angle, PI + eps):
            return True
    return False


def _lic11(x: list[float], y: list[float], numpoints: int, params: dict) -> bool:
    """LIC 11: three points separated by E_PTS, F_PTS with area > AREA1."""
    if numpoints < 5:
        return False
    e_pts = params["E_PTS"]
    f_pts = params["F_PTS"]
    a1 = params["AREA1"]
    for i in range(numpoints - e_pts - f_pts - 2):
        j = i + e_pts + 1
        k = j + f_pts + 1
        area = _triangle_area(x[i], y[i], x[j], y[j], x[k], y[k])
        if rc_gt(area, a1):
            return True
    return False


def _lic12(x: list[float], y: list[float], numpoints: int, params: dict) -> bool:
    """LIC 12: two points separated by G_PTS with x[j]-x[i] < 0."""
    if numpoints < 3:
        return False
    g_pts = params["G_PTS"]
    for i in range(numpoints - g_pts - 1):
        j = i + g_pts + 1
        if rc_lt(x[j] - x[i], 0.0):
            return True
    return False


def _lic13(x: list[float], y: list[float], numpoints: int, params: dict) -> bool:
    """LIC 13: dual condition — K_PTS separation, >LENGTH1 AND <LENGTH2."""
    if numpoints < 3:
        return False
    k_pts = params["K_PTS"]
    l1 = params["LENGTH1"]
    l2 = params["LENGTH2"]
    cond1 = False
    cond2 = False
    for i in range(numpoints - k_pts - 1):
        j = i + k_pts + 1
        d = _dist(x[i], y[i], x[j], y[j])
        if rc_gt(d, l1):
            cond1 = True
        if rc_lt(d, l2):
            cond2 = True
    return cond1 and cond2


def _lic14(x: list[float], y: list[float], numpoints: int, params: dict) -> bool:
    """LIC 14: dual condition — A_PTS/B_PTS separation, >RADIUS1 AND <=RADIUS2."""
    if numpoints < 5:
        return False
    a_pts = params["A_PTS"]
    b_pts = params["B_PTS"]
    r1 = params["RADIUS1"]
    r2 = params["RADIUS2"]
    cond1 = False
    cond2 = False
    for i in range(numpoints - a_pts - b_pts - 2):
        j = i + a_pts + 1
        k = j + b_pts + 1
        r = _circumscribed_radius(x[i], y[i], x[j], y[j], x[k], y[k])
        if rc_gt(r, r1):
            cond1 = True
        if rc_le(r, r2):
            cond2 = True
    return cond1 and cond2


def _lic15(x: list[float], y: list[float], numpoints: int, params: dict) -> bool:
    """LIC 15: dual condition — E_PTS/F_PTS separation, >AREA1 AND <AREA2."""
    if numpoints < 5:
        return False
    e_pts = params["E_PTS"]
    f_pts = params["F_PTS"]
    a1 = params["AREA1"]
    a2 = params["AREA2"]
    cond1 = False
    cond2 = False
    for i in range(numpoints - e_pts - f_pts - 2):
        j = i + e_pts + 1
        k = j + f_pts + 1
        area = _triangle_area(x[i], y[i], x[j], y[j], x[k], y[k])
        if rc_gt(area, a1):
            cond1 = True
        if rc_lt(area, a2):
            cond2 = True
    return cond1 and cond2


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

_LIC_FUNCS = [
    _lic1, _lic2, _lic3, _lic4, _lic5,
    _lic6, _lic7, _lic8, _lic9, _lic10,
    _lic11, _lic12, _lic13, _lic14, _lic15,
]


def decide(
    numpoints: int,
    x: list[float],
    y: list[float],
    parameters: dict[str, Any],
    lcm: list[list[str]],
    pum_diag: list[bool],
) -> tuple[list[bool], list[list[bool]], list[bool], bool]:
    """
    Reference implementation of the Launch Interceptor Program DECIDE procedure.

    See benchmarks/launch_interceptor/spec_original.md (Knight & Leveson verbatim);
    benchmarks/launch_interceptor/spec.md is a Python-oriented human summary.
    """
    # --- CMV ---
    cmv = [fn(x, y, numpoints, parameters) for fn in _LIC_FUNCS]

    # --- PUM ---
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

    # --- FUV ---
    fuv: list[bool] = []
    for i in range(15):
        if not pum[i][i]:
            fuv.append(True)
        else:
            fuv.append(all(pum[i][j] for j in range(15)))

    # --- LAUNCH ---
    launch = all(fuv)

    return cmv, pum, fuv, launch
