#!/usr/bin/env python3
"""
Launch Interceptor Program (Knight & Leveson, 1986)

This module implements the DECIDE procedure for determining whether to launch
a weapons interceptor based on radar tracking data.

The main entry point is the decide() function, which can be called programmatically,
or the module can be run directly to read JSON from stdin and write JSON to stdout.
"""

import json
import sys
import math
from typing import List, Dict, Any, Tuple

PI = 3.1415926535

# ============================================================================
# REALCOMPARE IMPLEMENTATION
# ============================================================================

def realcompare(a: float, b: float) -> str:
    """
    Compare two real numbers with six significant digit precision.

    Returns:
        "LT" if a < b
        "EQ" if a == b (within tolerance)
        "GT" if a > b
    """
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


# ============================================================================
# HELPER GEOMETRY FUNCTIONS
# ============================================================================

def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate Euclidean distance between two points."""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def distance_point_to_line(px: float, py: float, x1: float, y1: float,
                          x2: float, y2: float) -> float:
    """
    Calculate perpendicular distance from point (px, py) to the line
    defined by points (x1, y1) and (x2, y2).

    If the two points are the same, return the distance from (px, py) to that point.
    """
    if realcompare(x1, x2) == "EQ" and realcompare(y1, y2) == "EQ":
        return distance(px, py, x1, y1)

    # Line: (x2-x1)*y - (y2-y1)*x + (y2-y1)*x1 - (x2-x1)*y1 = 0
    # Distance = |ax + by + c| / sqrt(a^2 + b^2)
    a = y2 - y1
    b = -(x2 - x1)
    c = (x2 - x1) * y1 - (y2 - y1) * x1

    denom = math.sqrt(a * a + b * b)
    if realcompare(denom, 0.0) == "EQ":
        return distance(px, py, x1, y1)

    return abs(a * px + b * py + c) / denom


def angle_between_three_points(x1: float, y1: float, x2: float, y2: float,
                               x3: float, y3: float) -> float:
    """
    Calculate the angle formed by three points, where (x2, y2) is the vertex.

    Returns the angle in radians. If either endpoint coincides with the vertex,
    returns None to indicate the angle is undefined.
    """
    # Vector from vertex to first point
    v1x = x1 - x2
    v1y = y1 - y2

    # Vector from vertex to third point
    v2x = x3 - x2
    v2y = y3 - y2

    # Check if either vector is zero (degenerate case)
    len1 = math.sqrt(v1x * v1x + v1y * v1y)
    len2 = math.sqrt(v2x * v2x + v2y * v2y)

    if realcompare(len1, 0.0) == "EQ" or realcompare(len2, 0.0) == "EQ":
        return None

    # Dot product and cross product
    dot = v1x * v2x + v1y * v2y
    cross = v1x * v2y - v1y * v2x

    # atan2 gives angle in [-pi, pi]
    angle = math.atan2(cross, dot)

    # Normalize to [0, 2*pi) if needed, or keep as is for absolute angle
    # We want the absolute angle, so use absolute value
    if angle < 0:
        angle = angle + 2 * PI

    return angle


def triangle_area(x1: float, y1: float, x2: float, y2: float,
                 x3: float, y3: float) -> float:
    """Calculate the area of a triangle given three points using cross product."""
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)


def smallest_circle_radius(x1: float, y1: float, x2: float, y2: float,
                          x3: float, y3: float) -> float:
    """
    Calculate the radius of the smallest circle containing all three points.

    Returns the radius of the smallest enclosing circle.
    """
    # Distance between all pairs
    d12 = distance(x1, y1, x2, y2)
    d23 = distance(x2, y2, x3, y3)
    d31 = distance(x3, y3, x1, y1)

    # Check if any two points are the same
    epsilon = 1e-10

    # Use circumradius for non-degenerate triangle
    area = triangle_area(x1, y1, x2, y2, x3, y3)

    if area < epsilon:
        # Points are collinear; smallest circle has diameter = longest edge
        return max(d12, d23, d31) / 2.0

    # Circumradius formula: R = (a*b*c) / (4*Area)
    circumradius = (d12 * d23 * d31) / (4.0 * area)
    return circumradius


def get_quadrant(x: float, y: float) -> int:
    """
    Determine which quadrant a point is in, with priority when on axes.

    Quadrant I: x >= 0, y >= 0
    Quadrant II: x < 0, y >= 0
    Quadrant III: x < 0, y < 0
    Quadrant IV: x >= 0, y < 0

    Returns 1, 2, 3, or 4.
    """
    if realcompare(x, 0.0) != "LT":  # x >= 0
        if realcompare(y, 0.0) != "LT":  # y >= 0
            return 1
        else:  # y < 0
            return 4
    else:  # x < 0
        if realcompare(y, 0.0) != "LT":  # y >= 0
            return 2
        else:  # y < 0
            return 3


# ============================================================================
# LIC IMPLEMENTATIONS
# ============================================================================

def lic_0(numpoints: int, x: List[float], y: List[float], params: Dict[str, Any]) -> bool:
    """
    LIC 0: Two consecutive data points are greater than LENGTH1 apart.
    """
    length1 = params['LENGTH1']

    for i in range(numpoints - 1):
        d = distance(x[i], y[i], x[i + 1], y[i + 1])
        if realcompare(d, length1) == "GT":
            return True

    return False


def lic_1(numpoints: int, x: List[float], y: List[float], params: Dict[str, Any]) -> bool:
    """
    LIC 1: Three consecutive data points cannot all be contained within
    a circle of radius RADIUS1.
    """
    radius1 = params['RADIUS1']

    for i in range(numpoints - 2):
        r = smallest_circle_radius(x[i], y[i], x[i + 1], y[i + 1], x[i + 2], y[i + 2])
        if realcompare(r, radius1) == "GT":
            return True

    return False


def lic_2(numpoints: int, x: List[float], y: List[float], params: Dict[str, Any]) -> bool:
    """
    LIC 2: Three consecutive data points form an angle such that:
    angle < (PI - EPSILON) or angle > (PI + EPSILON)
    """
    epsilon = params['EPSILON']

    for i in range(numpoints - 2):
        angle = angle_between_three_points(x[i], y[i], x[i + 1], y[i + 1],
                                          x[i + 2], y[i + 2])

        if angle is None:
            continue

        lower = PI - epsilon
        upper = PI + epsilon

        if realcompare(angle, lower) == "LT" or realcompare(angle, upper) == "GT":
            return True

    return False


def lic_3(numpoints: int, x: List[float], y: List[float], params: Dict[str, Any]) -> bool:
    """
    LIC 3: Three consecutive data points form a triangle with area > AREA1.
    """
    area1 = params['AREA1']

    for i in range(numpoints - 2):
        area = triangle_area(x[i], y[i], x[i + 1], y[i + 1], x[i + 2], y[i + 2])
        if realcompare(area, area1) == "GT":
            return True

    return False


def lic_4(numpoints: int, x: List[float], y: List[float], params: Dict[str, Any]) -> bool:
    """
    LIC 4: Q_PTS consecutive points lie in more than QUADS quadrants.
    """
    q_pts = params['Q_PTS']
    quads = params['QUADS']

    for i in range(numpoints - q_pts + 1):
        quadrants = set()
        for j in range(i, i + q_pts):
            quad = get_quadrant(x[j], y[j])
            quadrants.add(quad)

        if len(quadrants) > quads:
            return True

    return False


def lic_5(numpoints: int, x: List[float], y: List[float], params: Dict[str, Any]) -> bool:
    """
    LIC 5: Two consecutive data points where X[j] - X[i] < 0 (j = i+1).
    """
    for i in range(numpoints - 1):
        if realcompare(x[i + 1] - x[i], 0.0) == "LT":
            return True

    return False


def lic_6(numpoints: int, x: List[float], y: List[float], params: Dict[str, Any]) -> bool:
    """
    LIC 6: N_PTS consecutive points where at least one lies distance > DIST
    from the line joining first and last of the N_PTS points.
    """
    if numpoints < 3:
        return False

    n_pts = params['N_PTS']
    dist = params['DIST']

    for i in range(numpoints - n_pts + 1):
        x1, y1 = x[i], y[i]
        x2, y2 = x[i + n_pts - 1], y[i + n_pts - 1]

        for j in range(i, i + n_pts):
            d = distance_point_to_line(x[j], y[j], x1, y1, x2, y2)
            if realcompare(d, dist) == "GT":
                return True

    return False


def lic_7(numpoints: int, x: List[float], y: List[float], params: Dict[str, Any]) -> bool:
    """
    LIC 7: Two data points separated by exactly K_PTS intervening points
    are > LENGTH1 apart.
    """
    if numpoints < 3:
        return False

    k_pts = params['K_PTS']
    length1 = params['LENGTH1']

    for i in range(numpoints - k_pts - 1):
        j = i + k_pts + 1
        d = distance(x[i], y[i], x[j], y[j])
        if realcompare(d, length1) == "GT":
            return True

    return False


def lic_8(numpoints: int, x: List[float], y: List[float], params: Dict[str, Any]) -> bool:
    """
    LIC 8: Three data points separated by A_PTS and B_PTS intervening points
    cannot be contained in circle of radius RADIUS1.
    """
    if numpoints < 5:
        return False

    a_pts = params['A_PTS']
    b_pts = params['B_PTS']
    radius1 = params['RADIUS1']

    for i in range(numpoints - a_pts - b_pts - 2):
        j = i + a_pts + 1
        k = j + b_pts + 1

        r = smallest_circle_radius(x[i], y[i], x[j], y[j], x[k], y[k])
        if realcompare(r, radius1) == "GT":
            return True

    return False


def lic_9(numpoints: int, x: List[float], y: List[float], params: Dict[str, Any]) -> bool:
    """
    LIC 9: Three data points separated by C_PTS and D_PTS intervening points
    form an angle such that angle < (PI - EPSILON) or angle > (PI + EPSILON).
    """
    if numpoints < 5:
        return False

    c_pts = params['C_PTS']
    d_pts = params['D_PTS']
    epsilon = params['EPSILON']

    for i in range(numpoints - c_pts - d_pts - 2):
        j = i + c_pts + 1
        k = j + d_pts + 1

        angle = angle_between_three_points(x[i], y[i], x[j], y[j], x[k], y[k])

        if angle is None:
            continue

        lower = PI - epsilon
        upper = PI + epsilon

        if realcompare(angle, lower) == "LT" or realcompare(angle, upper) == "GT":
            return True

    return False


def lic_10(numpoints: int, x: List[float], y: List[float], params: Dict[str, Any]) -> bool:
    """
    LIC 10: Three data points separated by E_PTS and F_PTS intervening points
    form a triangle with area > AREA1.
    """
    if numpoints < 5:
        return False

    e_pts = params['E_PTS']
    f_pts = params['F_PTS']
    area1 = params['AREA1']

    for i in range(numpoints - e_pts - f_pts - 2):
        j = i + e_pts + 1
        k = j + f_pts + 1

        area = triangle_area(x[i], y[i], x[j], y[j], x[k], y[k])
        if realcompare(area, area1) == "GT":
            return True

    return False


def lic_11(numpoints: int, x: List[float], y: List[float], params: Dict[str, Any]) -> bool:
    """
    LIC 11: Two data points separated by G_PTS intervening points
    where X[j] - X[i] < 0.
    """
    if numpoints < 3:
        return False

    g_pts = params['G_PTS']

    for i in range(numpoints - g_pts - 1):
        j = i + g_pts + 1
        if realcompare(x[j] - x[i], 0.0) == "LT":
            return True

    return False


def lic_12(numpoints: int, x: List[float], y: List[float], params: Dict[str, Any]) -> bool:
    """
    LIC 12: Two parts:
    1. Two points separated by K_PTS intervening points with distance > LENGTH1.
    2. Two points separated by K_PTS intervening points with distance < LENGTH2.
    Both must be true.
    """
    if numpoints < 3:
        return False

    k_pts = params['K_PTS']
    length1 = params['LENGTH1']
    length2 = params['LENGTH2']

    # Check first condition: distance > LENGTH1
    cond1 = False
    for i in range(numpoints - k_pts - 1):
        j = i + k_pts + 1
        d = distance(x[i], y[i], x[j], y[j])
        if realcompare(d, length1) == "GT":
            cond1 = True
            break

    if not cond1:
        return False

    # Check second condition: distance < LENGTH2
    cond2 = False
    for i in range(numpoints - k_pts - 1):
        j = i + k_pts + 1
        d = distance(x[i], y[i], x[j], y[j])
        if realcompare(d, length2) == "LT":
            cond2 = True
            break

    return cond1 and cond2


def lic_13(numpoints: int, x: List[float], y: List[float], params: Dict[str, Any]) -> bool:
    """
    LIC 13: Three data points separated by A_PTS and B_PTS intervening points
    have two conditions:
    1. Cannot be contained in circle of radius RADIUS1.
    2. Can be contained in circle of radius RADIUS2.
    Both must be true.
    """
    if numpoints < 5:
        return False

    a_pts = params['A_PTS']
    b_pts = params['B_PTS']
    radius1 = params['RADIUS1']
    radius2 = params['RADIUS2']

    # Check first condition: cannot be contained in RADIUS1
    cond1 = False
    for i in range(numpoints - a_pts - b_pts - 2):
        j = i + a_pts + 1
        k = j + b_pts + 1

        r = smallest_circle_radius(x[i], y[i], x[j], y[j], x[k], y[k])
        if realcompare(r, radius1) == "GT":
            cond1 = True
            break

    if not cond1:
        return False

    # Check second condition: can be contained in RADIUS2
    cond2 = False
    for i in range(numpoints - a_pts - b_pts - 2):
        j = i + a_pts + 1
        k = j + b_pts + 1

        r = smallest_circle_radius(x[i], y[i], x[j], y[j], x[k], y[k])
        if realcompare(r, radius2) != "GT":  # r <= RADIUS2
            cond2 = True
            break

    return cond1 and cond2


def lic_14(numpoints: int, x: List[float], y: List[float], params: Dict[str, Any]) -> bool:
    """
    LIC 14: Three data points separated by E_PTS and F_PTS intervening points
    have two conditions:
    1. Area > AREA1.
    2. Area < AREA2.
    Both must be true.
    """
    if numpoints < 5:
        return False

    e_pts = params['E_PTS']
    f_pts = params['F_PTS']
    area1 = params['AREA1']
    area2 = params['AREA2']

    # Check first condition: area > AREA1
    cond1 = False
    for i in range(numpoints - e_pts - f_pts - 2):
        j = i + e_pts + 1
        k = j + f_pts + 1

        area = triangle_area(x[i], y[i], x[j], y[j], x[k], y[k])
        if realcompare(area, area1) == "GT":
            cond1 = True
            break

    if not cond1:
        return False

    # Check second condition: area < AREA2
    cond2 = False
    for i in range(numpoints - e_pts - f_pts - 2):
        j = i + e_pts + 1
        k = j + f_pts + 1

        area = triangle_area(x[i], y[i], x[j], y[j], x[k], y[k])
        if realcompare(area, area2) == "LT":
            cond2 = True
            break

    return cond1 and cond2


# ============================================================================
# MAIN DECIDE FUNCTION
# ============================================================================

def decide(numpoints: int, x: List[float], y: List[float],
          parameters: Dict[str, Any], lcm: List[List[str]],
          pum_diag: List[bool]) -> Tuple[List[bool], List[List[bool]], List[bool], bool]:
    """
    Main DECIDE procedure.

    Args:
        numpoints: Number of data points (2-100)
        x: X coordinates of data points
        y: Y coordinates of data points
        parameters: Dictionary of parameters
        lcm: 15x15 Logical Connector Matrix
        pum_diag: 15-element list of PUM diagonal values (input only)

    Returns:
        Tuple of (cmv, pum, fuv, launch) where:
        - cmv: List of 15 booleans (Conditions Met Vector)
        - pum: 15x15 list of booleans (Preliminary Unlocking Matrix)
        - fuv: List of 15 booleans (Final Unlocking Vector)
        - launch: Boolean launch decision
    """

    # Compute CMV (Conditions Met Vector)
    lic_functions = [
        lic_0, lic_1, lic_2, lic_3, lic_4,
        lic_5, lic_6, lic_7, lic_8, lic_9,
        lic_10, lic_11, lic_12, lic_13, lic_14
    ]

    cmv = [lic_func(numpoints, x, y, parameters) for lic_func in lic_functions]

    # Initialize PUM as 15x15 matrix
    pum = [[False] * 15 for _ in range(15)]

    # Set diagonal elements from input
    for i in range(15):
        pum[i][i] = pum_diag[i]

    # Compute off-diagonal elements using LCM
    for i in range(15):
        for j in range(15):
            if i == j:
                continue  # Skip diagonal

            connector = lcm[i][j]

            if connector == "NOTUSED":
                pum[i][j] = True
            elif connector == "ANDD":
                pum[i][j] = cmv[i] and cmv[j]
            elif connector == "ORR":
                pum[i][j] = cmv[i] or cmv[j]

    # Compute FUV (Final Unlocking Vector)
    fuv = [False] * 15
    for i in range(15):
        if not pum[i][i]:
            # Diagonal is false, so FUV[i] = true
            fuv[i] = True
        else:
            # Diagonal is true, check if all elements in row are true
            all_true = all(pum[i][j] for j in range(15))
            fuv[i] = all_true

    # Compute LAUNCH decision
    launch = all(fuv)

    return cmv, pum, fuv, launch


# ============================================================================
# JSON I/O INTERFACE
# ============================================================================

def main():
    """Read JSON from stdin, compute decision, write JSON to stdout."""
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Error parsing JSON: {e}\n")
        sys.exit(1)

    try:
        numpoints = input_data['numpoints']
        x = input_data['x']
        y = input_data['y']
        parameters = input_data['parameters']
        lcm = input_data['lcm']
        pum_diag = input_data['pum_diag']

        cmv, pum, fuv, launch = decide(numpoints, x, y, parameters, lcm, pum_diag)

        output = {
            'cmv': cmv,
            'pum': pum,
            'fuv': fuv,
            'launch': launch
        }

        json.dump(output, sys.stdout)
        sys.stdout.write('\n')
    except Exception as e:
        sys.stderr.write(f"Error processing input: {e}\n")
        sys.exit(1)


if __name__ == '__main__':
    main()
