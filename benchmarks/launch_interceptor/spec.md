# Launch Interceptor Program — Python implementation reference (human / developer doc)

**Not used for agent generation.** Coding agents receive the verbatim K&L specification
(`benchmarks/launch_interceptor/spec_original.md`, configurable via `agent_spec_path` in YAML)
plus a short Python embedding described in `agents/base.py` (`TASK_PROMPT_TEMPLATE`).

The text below is a Python-oriented restatement of the same logic: types, `decide()` signature,
and LIC notes. Use it when reading or maintaining the oracle without parsing Pascal prose.

## Your Task

Implement the function `decide` in a file named `decide.py`. Do not implement any other public functions or classes beyond what is needed. Do not read from stdin or write to stdout/files. All logic must be self-contained.

## Function Signature

```python
from __future__ import annotations

def decide(
    numpoints: int,
    x: list[float],
    y: list[float],
    parameters: dict,
    lcm: list[list[str]],
    pum_diag: list[bool],
) -> tuple[list[bool], list[list[bool]], list[bool], bool]:
    """
    Evaluate the Launch Interceptor Conditions and compute the launch decision.

    Parameters
    ----------
    numpoints : int
        Number of planar data points. 2 <= numpoints <= 100.
    x : list[float]
        X-coordinates of data points. Length == numpoints.
    y : list[float]
        Y-coordinates of data points. Length == numpoints.
    parameters : dict
        Parameter record with the following keys (all floats unless noted):
            LENGTH1   - Length in LICs 1, 8, 13       (>= 0)
            RADIUS1   - Radius in LICs 2, 9, 14       (>= 0)
            EPSILON   - Deviation from PI in LICs 3, 10  (0 <= EPSILON < PI)
            AREA1     - Area in LICs 4, 11, 15         (>= 0)
            Q_PTS     - No. of consecutive points in LIC 5 (int, 2 <= Q_PTS <= numpoints)
            QUADS     - No. of quadrants in LIC 5      (int, 1 <= QUADS <= 3)
            DIST      - Distance in LIC 7              (>= 0)
            N_PTS     - No. of consecutive pts. in LIC 7 (int, 3 <= N_PTS <= numpoints)
            K_PTS     - No. of int. pts. in LICs 8, 13 (int, 1 <= K_PTS <= numpoints-2)
            A_PTS     - No. of int. pts. in LICs 9, 14  (int, >= 1)
            B_PTS     - No. of int. pts. in LICs 9, 14  (int, >= 1)
            C_PTS     - No. of int. pts. in LIC 10     (int, >= 1)
            D_PTS     - No. of int. pts. in LIC 10     (int, >= 1)
            E_PTS     - No. of int. pts. in LICs 11, 15 (int, >= 1)
            F_PTS     - No. of int. pts. in LICs 11, 15 (int, >= 1)
            G_PTS     - No. of int. pts. in LIC 12     (int, 1 <= G_PTS <= numpoints-2)
            LENGTH2   - Maximum length in LIC 13       (>= 0)
            RADIUS2   - Maximum radius in LIC 14       (>= 0)
            AREA2     - Maximum area in LIC 15         (>= 0)
    lcm : list[list[str]]
        15x15 Logical Connector Matrix. Each entry is one of:
            "NOTUSED" - PUM[i][j] = True
            "ANDD"    - PUM[i][j] = CMV[i] AND CMV[j]
            "ORR"     - PUM[i][j] = CMV[i] OR CMV[j]
        The matrix is symmetric. Diagonal entries are ignored (use pum_diag instead).
    pum_diag : list[bool]
        15 diagonal entries of the PUM. PUM[i][i] = pum_diag[i].

    Returns
    -------
    cmv : list[bool]
        15-element Conditions Met Vector. cmv[i] is True iff LIC (i+1) is met.
        (0-indexed: cmv[0] = LIC 1, cmv[14] = LIC 15)
    pum : list[list[bool]]
        15x15 Preliminary Unlocking Matrix.
        Off-diagonal: pum[i][j] computed from lcm[i][j] and cmv[i], cmv[j].
        Diagonal: pum[i][i] = pum_diag[i].
    fuv : list[bool]
        15-element Final Unlocking Vector.
        fuv[i] = True if pum[i][i] is False OR all pum[i][j] are True.
    launch : bool
        True if and only if all fuv[i] are True.
    """
    ...
```

## Constants

```python
PI = 3.1415926535897932384626433832795
```

## Real Number Comparison

Whenever real numbers must be compared, use a fixed-precision comparison equivalent to the Pascal `REALCOMPARE` function, which compares with respect to the **six most significant digits**. Implement this as:

```python
def realcompare(a: float, b: float) -> str:
    """Returns 'LT', 'EQ', or 'GT' comparing a and b to 6 significant digits."""
```

Use this function for **all** real-number comparisons in the LIC computations (distances, areas, radii, angles, coordinates).

## Launch Interceptor Conditions (LICs)

All 15 LICs are evaluated for the set of `numpoints` points: `(x[0],y[0]), ..., (x[numpoints-1],y[numpoints-1])`.

`cmv[i]` is True iff LIC (i+1) is met (0-indexed).

### LIC 1 (cmv[0])
There exists at least one set of two consecutive data points that are a distance greater than `LENGTH1` apart.

Constraint: `LENGTH1 >= 0`

### LIC 2 (cmv[1])
There exists at least one set of three consecutive data points that cannot all be contained within or on a circle of radius `RADIUS1`.

Constraint: `RADIUS1 >= 0`

### LIC 3 (cmv[2])
There exists at least one set of three consecutive data points which form an angle such that:
- `angle < (PI - EPSILON)`, or
- `angle > (PI + EPSILON)`

The second of the three consecutive points is always the vertex of the angle. If either the first or last point coincides with the vertex, the angle is undefined and the LIC is **not** satisfied by those three points.

Constraint: `0 <= EPSILON < PI`

### LIC 4 (cmv[3])
There exists at least one set of three consecutive data points that are the vertices of a triangle with area greater than `AREA1`.

Constraint: `AREA1 >= 0`

### LIC 5 (cmv[4])
There exists at least one set of `Q_PTS` consecutive data points that lie in more than `QUADS` quadrants.

Quadrant assignment rules (priority order — first matching quadrant wins):
- Quadrant I:   x >= 0 and y >= 0
- Quadrant II:  x < 0 and y >= 0
- Quadrant III: x <= 0 and y < 0
- Quadrant IV:  x > 0 and y < 0

Examples: `(0,0)` → Q1, `(-1,0)` → Q2, `(0,-1)` → Q3, `(0,1)` → Q1, `(1,0)` → Q1.

Constraints: `2 <= Q_PTS <= numpoints`, `1 <= QUADS <= 3`

### LIC 6 (cmv[5])
There exists at least one set of two consecutive data points `(x[i], y[i])` and `(x[j], y[j])` such that `x[j] - x[i] < 0` (where `j = i + 1`).

### LIC 7 (cmv[6])
There exists at least one set of `N_PTS` consecutive data points such that at least one of the points lies a distance greater than `DIST` from the line joining the first and last of these `N_PTS` points.

If the first and last points of the `N_PTS` are identical, the distance is measured from the coincident point to each of the other points in the set.

The condition is **not met** when `numpoints < 3`.

Constraint: `3 <= N_PTS <= numpoints`, `DIST >= 0`

### LIC 8 (cmv[7])
There exists at least one set of two data points separated by exactly `K_PTS` consecutive intervening points that are a distance greater than `LENGTH1` apart.

That is, for some index i: distance between `(x[i], y[i])` and `(x[i+K_PTS+1], y[i+K_PTS+1])` > LENGTH1.

The condition is **not met** when `numpoints < 3`.

Constraint: `1 <= K_PTS <= numpoints - 2`

### LIC 9 (cmv[8])
There exists at least one set of three data points separated by exactly `A_PTS` and `B_PTS` consecutive intervening points, respectively, that cannot be contained within or on a circle of radius `RADIUS1`.

The three points are at indices i, i+A_PTS+1, i+A_PTS+B_PTS+2.

The condition is **not met** when `numpoints < 5`.

Constraints: `A_PTS >= 1`, `B_PTS >= 1`, `A_PTS + B_PTS <= numpoints - 3`

### LIC 10 (cmv[9])
There exists at least one set of three data points separated by exactly `C_PTS` and `D_PTS` consecutive intervening points, respectively, that form an angle such that:
- `angle < (PI - EPSILON)`, or
- `angle > (PI + EPSILON)`

The second point of the set is always the vertex. If either the first or last point coincides with the vertex, the angle is undefined and the LIC is **not** satisfied by those three points.

The condition is **not met** when `numpoints < 5`.

Constraints: `C_PTS >= 1`, `D_PTS >= 1`, `C_PTS + D_PTS <= numpoints - 3`

### LIC 11 (cmv[10])
There exists at least one set of three data points separated by exactly `E_PTS` and `F_PTS` consecutive intervening points, respectively, that are the vertices of a triangle with area greater than `AREA1`.

The three points are at indices i, i+E_PTS+1, i+E_PTS+F_PTS+2.

The condition is **not met** when `numpoints < 5`.

Constraints: `E_PTS >= 1`, `F_PTS >= 1`, `E_PTS + F_PTS <= numpoints - 3`

### LIC 12 (cmv[11])
There exists at least one set of two data points `(x[i], y[i])` and `(x[j], y[j])` separated by exactly `G_PTS` consecutive intervening points, such that `x[j] - x[i] < 0` (where `i < j`).

That is, `j = i + G_PTS + 1` and `x[j] - x[i] < 0`.

The condition is **not met** when `numpoints < 3`.

Constraint: `1 <= G_PTS <= numpoints - 2`

### LIC 13 (cmv[12])
**Both** of the following must be true:
1. There exists at least one set of two data points separated by exactly `K_PTS` consecutive intervening points that are a distance **greater than** `LENGTH1` apart.
2. There exists at least one set of two data points (possibly different) separated by exactly `K_PTS` consecutive intervening points that are a distance **less than** `LENGTH2` apart.

The condition is **not met** when `numpoints < 3`.

Constraint: `LENGTH2 >= 0`

### LIC 14 (cmv[13])
**Both** of the following must be true:
1. There exists at least one set of three data points separated by exactly `A_PTS` and `B_PTS` consecutive intervening points, respectively, that cannot be contained within or on a circle of radius `RADIUS1`.
2. There exists at least one set of three data points (possibly different) separated by exactly `A_PTS` and `B_PTS` consecutive intervening points, respectively, that **can** be contained in or on a circle of radius `RADIUS2`.

The condition is **not met** when `numpoints < 5`.

Constraint: `RADIUS2 >= 0`

### LIC 15 (cmv[14])
**Both** of the following must be true:
1. There exists at least one set of three data points separated by exactly `E_PTS` and `F_PTS` consecutive intervening points, respectively, that are the vertices of a triangle with area **greater than** `AREA1`.
2. There exists at least one set of three data points (possibly different) separated by exactly `E_PTS` and `F_PTS` consecutive intervening points, respectively, that are the vertices of a triangle with area **less than** `AREA2`.

The condition is **not met** when `numpoints < 5`.

Constraint: `AREA2 >= 0`

## Combining LICs: PUM

The off-diagonal elements of PUM are computed from CMV and LCM:
- If `lcm[i][j] == "NOTUSED"`: `pum[i][j] = True`
- If `lcm[i][j] == "ANDD"`: `pum[i][j] = cmv[i] and cmv[j]`
- If `lcm[i][j] == "ORR"`: `pum[i][j] = cmv[i] or cmv[j]`

LCM is symmetric: `lcm[i][j] == lcm[j][i]`.

Diagonal: `pum[i][i] = pum_diag[i]`.

## Final Unlocking Vector (FUV)

`fuv[i] = True` if `pum[i][i] is False` OR all elements in `pum[i]` (the entire row i, including diagonal) are `True`.

## Launch Decision

`launch = all(fuv[i] for i in range(15))`

## Notes

- Do not include input validation. Assume all inputs are within the specified ranges.
- Use the `realcompare` function for all real-number comparisons.
- Indices are 0-based in Python (LIC 1 = cmv[0], LIC 15 = cmv[14]).
- The function must be deterministic and have no side effects.
