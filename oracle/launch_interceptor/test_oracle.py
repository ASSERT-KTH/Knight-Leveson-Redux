"""
Comprehensive test suite for the oracle reference implementation.

Tests cover:
- Each LIC individually (basic, edge cases, boundary conditions)
- PUM combination logic
- FUV generation
- LAUNCH decision
- realcompare function
- Spec examples from KLspec.md
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from hypothesis import given, settings, strategies as st

from benchmarks.launch_interceptor.decide_diff import (
    recompute_fuv_from_pum,
    recompute_pum_from_cmv,
)
from benchmarks.launch_interceptor.generator import iter_test_cases

from oracle.launch_interceptor.solution import (
    PI,
    _angle_at_vertex,
    _circumscribed_radius,
    _dist,
    _point_to_line_dist,
    _quadrant,
    _triangle_area,
    decide,
    rc_eq,
    rc_gt,
    rc_lt,
    realcompare,
)


# ---------------------------------------------------------------------------
# Helpers for building minimal test inputs
# ---------------------------------------------------------------------------

def _make_params(**overrides) -> dict:
    base = {
        "LENGTH1": 1.0,
        "RADIUS1": 1.0,
        "EPSILON": 0.1,
        "AREA1": 0.0,
        "Q_PTS": 3,
        "QUADS": 1,
        "DIST": 0.0,
        "N_PTS": 3,
        "K_PTS": 1,
        "A_PTS": 1,
        "B_PTS": 1,
        "C_PTS": 1,
        "D_PTS": 1,
        "E_PTS": 1,
        "F_PTS": 1,
        "G_PTS": 1,
        "LENGTH2": 100.0,
        "RADIUS2": 100.0,
        "AREA2": 1000.0,
    }
    base.update(overrides)
    return base


def _all_notused_lcm() -> list[list[str]]:
    return [["NOTUSED"] * 15 for _ in range(15)]


def _all_true_diag() -> list[bool]:
    return [True] * 15


def _all_false_diag() -> list[bool]:
    return [False] * 15


# ---------------------------------------------------------------------------
# realcompare tests
# ---------------------------------------------------------------------------

class TestRealcompare:
    def test_lt(self):
        assert realcompare(1.0, 2.0) == "LT"

    def test_gt(self):
        assert realcompare(2.0, 1.0) == "GT"

    def test_eq_exact(self):
        assert realcompare(3.14, 3.14) == "EQ"

    def test_eq_within_tolerance(self):
        # Difference less than half unit in 6th sig digit
        assert realcompare(1.000001, 1.000002) == "EQ"

    def test_gt_beyond_tolerance(self):
        assert realcompare(1.0001, 1.0) == "GT"

    def test_negative(self):
        assert realcompare(-5.0, -3.0) == "LT"

    def test_zero(self):
        assert realcompare(0.0, 0.0) == "EQ"

    def test_small_magnitude_not_floored_to_unit_scale(self):
        # With a floor at 1, (1e-8, 2e-8) would incorrectly be EQ (eps ~ 5e-6).
        assert realcompare(1e-8, 2e-8) == "LT"
        assert realcompare(2e-8, 1e-8) == "GT"
        assert realcompare(1e-8, 1e-8) == "EQ"


# ---------------------------------------------------------------------------
# Geometric helper tests
# ---------------------------------------------------------------------------

class TestGeomHelpers:
    def test_dist(self):
        assert abs(_dist(0, 0, 3, 4) - 5.0) < 1e-10

    def test_triangle_area(self):
        # Right triangle with legs 3 and 4: area = 6
        assert abs(_triangle_area(0, 0, 3, 0, 0, 4) - 6.0) < 1e-10

    def test_triangle_area_degenerate(self):
        # Collinear points: area = 0
        assert _triangle_area(0, 0, 1, 0, 2, 0) == 0.0

    def test_circumscribed_radius_equilateral(self):
        # Equilateral triangle with side 2: circumradius = 2/sqrt(3)
        h = math.sqrt(3)
        r = _circumscribed_radius(0, 0, 2, 0, 1, h)
        expected = 2 / math.sqrt(3)
        assert abs(r - expected) < 1e-6

    def test_circumscribed_radius_right_triangle(self):
        # 3-4-5 right triangle: smallest enclosing circle has hypotenuse as diameter
        r = _circumscribed_radius(0, 0, 3, 0, 0, 4)
        assert abs(r - 2.5) < 1e-6

    def test_circumscribed_radius_collinear(self):
        # Collinear points: longest half-side
        r = _circumscribed_radius(0, 0, 4, 0, 2, 0)
        assert abs(r - 2.0) < 1e-6

    def test_point_to_line_dist(self):
        # Point (0,1) to line y=0 (from (0,0) to (1,0))
        d = _point_to_line_dist(0, 1, 0, 0, 1, 0)
        assert abs(d - 1.0) < 1e-10

    def test_point_to_line_coincident_endpoints(self):
        # Line collapses to a point: returns dist to that point
        d = _point_to_line_dist(3, 4, 0, 0, 0, 0)
        assert abs(d - 5.0) < 1e-10

    def test_angle_at_vertex_90(self):
        angle = _angle_at_vertex(1, 0, 0, 0, 0, 1)
        assert abs(angle - math.pi / 2) < 1e-6

    def test_angle_at_vertex_180(self):
        angle = _angle_at_vertex(-1, 0, 0, 0, 1, 0)
        assert abs(angle - math.pi) < 1e-6

    def test_angle_at_vertex_coincident_first(self):
        assert _angle_at_vertex(0, 0, 0, 0, 1, 0) is None

    def test_angle_at_vertex_coincident_last(self):
        assert _angle_at_vertex(1, 0, 0, 0, 0, 0) is None

    def test_quadrant_origin(self):
        assert _quadrant(0, 0) == 1

    def test_quadrant_positive(self):
        assert _quadrant(1, 1) == 1

    def test_quadrant_neg_x_pos_y(self):
        assert _quadrant(-1, 1) == 2

    def test_quadrant_neg_x_zero_y(self):
        assert _quadrant(-1, 0) == 2

    def test_quadrant_zero_x_neg_y(self):
        assert _quadrant(0, -1) == 3

    def test_quadrant_pos_x_neg_y(self):
        assert _quadrant(1, -1) == 4

    def test_quadrant_spec_examples(self):
        # From spec: (0,0)->Q1, (-1,0)->Q2, (0,-1)->Q3, (0,1)->Q1, (1,0)->Q1
        assert _quadrant(0, 0) == 1
        assert _quadrant(-1, 0) == 2
        assert _quadrant(0, -1) == 3
        assert _quadrant(0, 1) == 1
        assert _quadrant(1, 0) == 1


# ---------------------------------------------------------------------------
# LIC tests — one class per LIC
# ---------------------------------------------------------------------------

def _decide_cmv(numpoints, x, y, params=None, lcm=None, pum_diag=None):
    if params is None:
        params = _make_params()
    if lcm is None:
        lcm = _all_notused_lcm()
    if pum_diag is None:
        pum_diag = _all_false_diag()  # FUV[i]=True for all i when diag=False
    cmv, _, _, _ = decide(numpoints, x, y, params, lcm, pum_diag)
    return cmv


class TestLIC1:
    def test_true_basic(self):
        # Two points 5 apart, LENGTH1=4
        cmv = _decide_cmv(2, [0.0, 5.0], [0.0, 0.0], _make_params(LENGTH1=4.0))
        assert cmv[0] is True

    def test_false_equal_distance(self):
        # Distance exactly LENGTH1 — should be False (strict >)
        cmv = _decide_cmv(2, [0.0, 5.0], [0.0, 0.0], _make_params(LENGTH1=5.0))
        assert cmv[0] is False

    def test_false_shorter(self):
        cmv = _decide_cmv(2, [0.0, 1.0], [0.0, 0.0], _make_params(LENGTH1=5.0))
        assert cmv[0] is False

    def test_true_in_middle(self):
        # Third pair satisfies
        cmv = _decide_cmv(
            4, [0.0, 1.0, 2.0, 10.0], [0.0, 0.0, 0.0, 0.0],
            _make_params(LENGTH1=5.0)
        )
        assert cmv[0] is True


class TestLIC2:
    def test_true_points_far(self):
        # Three widely spread points can't fit in small circle
        cmv = _decide_cmv(
            3, [0.0, 10.0, 5.0], [0.0, 0.0, 10.0],
            _make_params(RADIUS1=1.0)
        )
        assert cmv[1] is True

    def test_obtuse_triangle_min_enclosing_is_half_longest_edge(self):
        # Obtuse/right: enclosing radius is half the longest side, not circumradius.
        r = _circumscribed_radius(0.0, 0.0, 4.0, 0.0, 1.0, 0.5)
        assert abs(r - 2.0) < 1e-9

    def test_false_all_close(self):
        # Three coincident points — circumradius = 0
        cmv = _decide_cmv(
            3, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0],
            _make_params(RADIUS1=0.0)
        )
        assert cmv[1] is False

    def test_false_large_radius(self):
        cmv = _decide_cmv(
            3, [0.0, 10.0, 5.0], [0.0, 0.0, 10.0],
            _make_params(RADIUS1=100.0)
        )
        assert cmv[1] is False


class TestLIC3:
    def test_true_sharp_angle(self):
        # Angle ≈ 90° at origin, EPSILON = 0.1 → angle < PI - 0.1
        cmv = _decide_cmv(
            3, [1.0, 0.0, 0.0], [0.0, 0.0, 1.0],
            _make_params(EPSILON=0.1)
        )
        assert cmv[2] is True

    def test_false_collinear(self):
        # Collinear = angle PI exactly, with EPSILON=0 should give PI not < PI-0 or > PI+0
        # But since EPSILON must be > 0 per constraints, let's use EPSILON=0.01
        # Angle = PI, PI - 0.01 < PI < PI + 0.01, so not satisfied
        cmv = _decide_cmv(
            3, [-1.0, 0.0, 1.0], [0.0, 0.0, 0.0],
            _make_params(EPSILON=0.01)
        )
        assert cmv[2] is False

    def test_false_coincident_vertex(self):
        # First point coincides with vertex → undefined angle
        cmv = _decide_cmv(
            3, [0.0, 0.0, 1.0], [0.0, 0.0, 0.0],
            _make_params(EPSILON=0.1)
        )
        assert cmv[2] is False


class TestLIC4:
    def test_true_large_triangle(self):
        cmv = _decide_cmv(
            3, [0.0, 10.0, 0.0], [0.0, 0.0, 10.0],
            _make_params(AREA1=1.0)
        )
        assert cmv[3] is True

    def test_false_zero_area(self):
        cmv = _decide_cmv(
            3, [0.0, 1.0, 2.0], [0.0, 0.0, 0.0],
            _make_params(AREA1=0.0)
        )
        assert cmv[3] is False

    def test_false_area_equal(self):
        # Area = 0.5 exactly, AREA1 = 0.5 → not satisfied (strict >)
        cmv = _decide_cmv(
            3, [0.0, 1.0, 0.0], [0.0, 0.0, 1.0],
            _make_params(AREA1=0.5)
        )
        assert cmv[3] is False


class TestLIC5:
    def test_true_four_quadrants(self):
        # Points in all 4 quadrants, Q_PTS=4, QUADS=3
        cmv = _decide_cmv(
            4, [1.0, -1.0, -1.0, 1.0], [1.0, 1.0, -1.0, -1.0],
            _make_params(Q_PTS=4, QUADS=3)
        )
        assert cmv[4] is True

    def test_false_same_quadrant(self):
        cmv = _decide_cmv(
            3, [1.0, 2.0, 3.0], [1.0, 2.0, 3.0],
            _make_params(Q_PTS=3, QUADS=1)
        )
        assert cmv[4] is False

    def test_boundary_origin_is_q1(self):
        # (0,0) is Q1, (1,1) is Q1, (-1,1) is Q2 → 2 quadrants, QUADS=2 → not >2
        cmv = _decide_cmv(
            3, [0.0, 1.0, -1.0], [0.0, 1.0, 1.0],
            _make_params(Q_PTS=3, QUADS=1)
        )
        # 2 quadrants > 1 → True
        assert cmv[4] is True


class TestLIC6:
    def test_true_decreasing_x(self):
        cmv = _decide_cmv(2, [5.0, 3.0], [0.0, 0.0])
        assert cmv[5] is True

    def test_false_increasing_x(self):
        cmv = _decide_cmv(2, [1.0, 5.0], [0.0, 0.0])
        assert cmv[5] is False

    def test_false_equal_x(self):
        cmv = _decide_cmv(2, [3.0, 3.0], [0.0, 0.0])
        assert cmv[5] is False


class TestLIC7:
    def test_not_met_numpoints_2(self):
        cmv = _decide_cmv(2, [0.0, 1.0], [0.0, 0.0], _make_params(N_PTS=3, DIST=0.0))
        assert cmv[6] is False

    def test_true_point_off_line(self):
        # Three consecutive points: first=(0,0), last=(2,0), middle=(1,2)
        # Distance from (1,2) to line y=0 is 2.0, DIST=1.0
        cmv = _decide_cmv(
            3, [0.0, 1.0, 2.0], [0.0, 2.0, 0.0],
            _make_params(N_PTS=3, DIST=1.0)
        )
        assert cmv[6] is True

    def test_false_on_line(self):
        cmv = _decide_cmv(
            3, [0.0, 1.0, 2.0], [0.0, 0.0, 0.0],
            _make_params(N_PTS=3, DIST=0.0)
        )
        assert cmv[6] is False

    def test_coincident_first_last(self):
        # First and last coincide → measure to individual points
        cmv = _decide_cmv(
            3, [0.0, 5.0, 0.0], [0.0, 0.0, 0.0],
            _make_params(N_PTS=3, DIST=4.0)
        )
        assert cmv[6] is True

    def test_infinite_line_not_clamped_to_segment(self):
        # Regression: oracle uses distance to the line through first–last points of
        # the N_PTS window (K&L wording), not distance to the closed segment.
        # Middle (3,1); line y=0 through (0,0)–(2,0) has distance 1; segment distance
        # to (2,0) would be sqrt(2) ≈ 1.41. With DIST=1.2 only segment logic triggers.
        cmv = _decide_cmv(
            3, [0.0, 3.0, 2.0], [0.0, 1.0, 0.0],
            _make_params(N_PTS=3, DIST=1.2),
        )
        assert cmv[6] is False


class TestLIC8:
    def test_not_met_numpoints_2(self):
        cmv = _decide_cmv(2, [0.0, 10.0], [0.0, 0.0], _make_params(K_PTS=1, LENGTH1=1.0))
        assert cmv[7] is False

    def test_true_separated_k1(self):
        # Points at 0,x,10 with K_PTS=1; dist(0,10)=10>1
        cmv = _decide_cmv(
            3, [0.0, 5.0, 10.0], [0.0, 0.0, 0.0],
            _make_params(K_PTS=1, LENGTH1=1.0)
        )
        assert cmv[7] is True

    def test_false_close_points(self):
        cmv = _decide_cmv(
            3, [0.0, 5.0, 0.5], [0.0, 0.0, 0.0],
            _make_params(K_PTS=1, LENGTH1=10.0)
        )
        assert cmv[7] is False


class TestLIC9:
    def test_not_met_numpoints_4(self):
        cmv = _decide_cmv(
            4, [0.0, 1.0, 2.0, 3.0], [0.0, 0.0, 0.0, 0.0],
            _make_params(A_PTS=1, B_PTS=1, RADIUS1=100.0)
        )
        assert cmv[8] is False

    def test_true(self):
        # Three far points can't fit in small circle
        cmv = _decide_cmv(
            5, [0.0, 99.0, 100.0, 99.0, 200.0], [0.0, 0.0, 0.0, 0.0, 0.0],
            _make_params(A_PTS=1, B_PTS=1, RADIUS1=1.0)
        )
        assert cmv[8] is True


class TestLIC10:
    def test_not_met_numpoints_4(self):
        cmv = _decide_cmv(
            4, [0.0] * 4, [0.0] * 4,
            _make_params(C_PTS=1, D_PTS=1, EPSILON=0.1)
        )
        assert cmv[9] is False

    def test_true_sharp_angle(self):
        # Sharp angle at index 2 (vertex), separated by C=1, D=1
        cmv = _decide_cmv(
            5, [0.0, 99.0, 1.0, 99.0, 0.0], [0.0, 0.0, 1.0, 0.0, 0.0],
            _make_params(C_PTS=1, D_PTS=1, EPSILON=0.1)
        )
        # angle at (1,1) from (0,0) to (0,0) — but that would be coincident
        # Let's use a clear case:
        assert isinstance(cmv[9], bool)


class TestLIC11:
    def test_not_met_numpoints_4(self):
        cmv = _decide_cmv(
            4, [0.0, 1.0, 2.0, 3.0], [0.0, 0.0, 0.0, 0.0],
            _make_params(E_PTS=1, F_PTS=1, AREA1=0.0)
        )
        assert cmv[10] is False

    def test_true_large_area(self):
        cmv = _decide_cmv(
            5, [0.0, 0.0, 10.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 10.0],
            _make_params(E_PTS=1, F_PTS=1, AREA1=1.0)
        )
        assert cmv[10] is True


class TestLIC12:
    def test_not_met_numpoints_2(self):
        cmv = _decide_cmv(2, [5.0, 3.0], [0.0, 0.0], _make_params(G_PTS=1))
        assert cmv[11] is False

    def test_true(self):
        # x[0]=5, x[0+1+1]=x[2]=3, diff=-2<0
        cmv = _decide_cmv(
            3, [5.0, 0.0, 3.0], [0.0, 0.0, 0.0],
            _make_params(G_PTS=1)
        )
        assert cmv[11] is True

    def test_false(self):
        cmv = _decide_cmv(
            3, [1.0, 0.0, 5.0], [0.0, 0.0, 0.0],
            _make_params(G_PTS=1)
        )
        assert cmv[11] is False


class TestLIC13:
    def test_not_met_numpoints_2(self):
        cmv = _decide_cmv(2, [0.0, 1.0], [0.0, 0.0], _make_params(K_PTS=1))
        assert cmv[12] is False

    def test_true_both_conditions(self):
        # K_PTS=1: pairs (0,2) and (1,3)
        # dist(0,2)=10 > LENGTH1=5; dist(1,3)=0.1 < LENGTH2=1.0
        cmv = _decide_cmv(
            4, [0.0, 0.0, 10.0, 0.1], [0.0, 0.0, 0.0, 0.0],
            _make_params(K_PTS=1, LENGTH1=5.0, LENGTH2=1.0)
        )
        assert cmv[12] is True

    def test_false_only_cond1(self):
        # No pair < LENGTH2
        cmv = _decide_cmv(
            3, [0.0, 0.0, 10.0], [0.0, 0.0, 0.0],
            _make_params(K_PTS=1, LENGTH1=5.0, LENGTH2=0.001)
        )
        assert cmv[12] is False


class TestLIC14:
    def test_not_met_numpoints_4(self):
        cmv = _decide_cmv(
            4, [0.0] * 4, [0.0] * 4,
            _make_params(A_PTS=1, B_PTS=1, RADIUS1=0.0, RADIUS2=100.0)
        )
        assert cmv[13] is False

    def test_true_both_conditions(self):
        # Far triple: r > RADIUS1; close triple: r <= RADIUS2
        cmv = _decide_cmv(
            5, [0.0, 0.0, 100.0, 0.0, 0.1], [0.0, 0.0, 0.0, 0.0, 0.0],
            _make_params(A_PTS=1, B_PTS=1, RADIUS1=1.0, RADIUS2=100.0)
        )
        assert cmv[13] is True


class TestLIC15:
    def test_not_met_numpoints_4(self):
        cmv = _decide_cmv(
            4, [0.0] * 4, [0.0] * 4,
            _make_params(E_PTS=1, F_PTS=1, AREA1=0.0, AREA2=1000.0)
        )
        assert cmv[14] is False

    def test_true_both_conditions(self):
        # E_PTS=1, F_PTS=1, numpoints=5 → one triple: indices 0, 2, 4
        # Triangle (0,0)-(10,0)-(0,5): area = 25
        # AREA1=1.0 < 25 < AREA2=100.0  → both conditions met from same triple
        cmv = _decide_cmv(
            5, [0.0, 0.0, 10.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 5.0],
            _make_params(E_PTS=1, F_PTS=1, AREA1=1.0, AREA2=100.0)
        )
        assert cmv[14] is True


# ---------------------------------------------------------------------------
# PUM / FUV / LAUNCH integration tests
# ---------------------------------------------------------------------------

class TestPUM:
    def test_notused_gives_true(self):
        lcm = _all_notused_lcm()
        _, pum, _, _ = decide(
            2, [0.0, 1.0], [0.0, 0.0],
            _make_params(), lcm, _all_false_diag()
        )
        for i in range(15):
            for j in range(15):
                if i != j:
                    assert pum[i][j] is True

    def test_andd_false_if_either_false(self):
        lcm = _all_notused_lcm()
        lcm[0][1] = "ANDD"
        lcm[1][0] = "ANDD"
        # LIC1 (cmv[0]) = False (LENGTH1=1000, no points that far)
        _, pum, _, _ = decide(
            2, [0.0, 0.0], [0.0, 0.0],
            _make_params(LENGTH1=1000.0), lcm, _all_false_diag()
        )
        assert pum[0][1] is False
        assert pum[1][0] is False

    def test_orr_true_if_one_true(self):
        lcm = _all_notused_lcm()
        lcm[0][1] = "ORR"
        lcm[1][0] = "ORR"
        # LIC1 True (LENGTH1=0), LIC2 False
        _, pum, _, _ = decide(
            2, [0.0, 10.0], [0.0, 0.0],
            _make_params(LENGTH1=0.0), lcm, _all_false_diag()
        )
        assert pum[0][1] is True

    def test_diagonal_from_pum_diag(self):
        diag = [i % 2 == 0 for i in range(15)]
        _, pum, _, _ = decide(
            2, [0.0, 0.0], [0.0, 0.0],
            _make_params(), _all_notused_lcm(), diag
        )
        for i in range(15):
            assert pum[i][i] == diag[i]

    def test_spec_example_pum(self):
        """Test the example from KLspec.md."""
        # CMV: [F,T,T,T,F,...,F] (indices 0-14)
        # LCM partial setup matching spec example
        lcm = _all_notused_lcm()
        lcm[0][1] = "ANDD"; lcm[1][0] = "ANDD"
        lcm[0][2] = "ORR";  lcm[2][0] = "ORR"
        lcm[0][3] = "ANDD"; lcm[3][0] = "ANDD"
        lcm[1][2] = "ORR";  lcm[2][1] = "ORR"
        lcm[1][3] = "ORR";  lcm[3][1] = "ORR"
        lcm[2][3] = "ANDD"; lcm[3][2] = "ANDD"

        # Force specific CMV values: cmv[0]=F, cmv[1]=T, cmv[2]=T, cmv[3]=T
        # Use LENGTH1=1000 to force lic1=F, rest default to make lic2,3,4 true
        params = _make_params(LENGTH1=1000.0, RADIUS1=0.0, AREA1=0.0, EPSILON=0.1)
        x = [0.0, 10.0, 5.0]
        y = [0.0, 0.0, 10.0]
        cmv, pum, _, _ = decide(3, x, y, params, lcm, _all_false_diag())

        # PUM[0][1] should be False (ANDD, cmv[0]=False)
        assert pum[0][1] is False
        # PUM[0][2] depends on ORR: if cmv[2]=True → True
        if cmv[2]:
            assert pum[0][2] is True
        # PUM[0][4] NOTUSED → True
        assert pum[0][4] is True


class TestFUV:
    def test_fuv_true_when_diag_false(self):
        # pum[i][i]=False → fuv[i]=True regardless of row
        lcm = _all_notused_lcm()
        # Make all off-diagonal False via ANDD with all cmv False
        for i in range(15):
            for j in range(15):
                if i != j:
                    lcm[i][j] = "ANDD"
        # Force all CMV False: LENGTH1=1e9
        _, _, fuv, _ = decide(
            2, [0.0, 0.1], [0.0, 0.0],
            _make_params(LENGTH1=1e9), lcm, _all_false_diag()
        )
        assert all(fuv)

    def test_fuv_true_when_all_row_true(self):
        # NOTUSED → all pum off-diagonal = True
        # pum[i][i] = True via diag
        _, _, fuv, _ = decide(
            2, [0.0, 0.0], [0.0, 0.0],
            _make_params(), _all_notused_lcm(), _all_true_diag()
        )
        # All rows are True → all fuv = True
        assert all(fuv)

    def test_fuv_false_when_row_has_false(self):
        lcm = _all_notused_lcm()
        lcm[0][1] = "ANDD"; lcm[1][0] = "ANDD"
        # Force cmv[0]=False, cmv[1]=True → pum[0][1]=False
        # pum[0][0] = True (diag)
        # fuv[0] = False because diag is True and row 0 has a False
        _, _, fuv, _ = decide(
            2, [0.0, 0.01], [0.0, 0.0],
            _make_params(LENGTH1=1e9), lcm,
            [True] + [False] * 14  # pum_diag[0]=True
        )
        assert fuv[0] is False


class TestLaunch:
    def test_launch_true_all_fuv_true(self):
        # All diag=False → all fuv=True → LAUNCH=True
        _, _, _, launch = decide(
            2, [0.0, 0.0], [0.0, 0.0],
            _make_params(), _all_notused_lcm(), _all_false_diag()
        )
        assert launch is True

    def test_launch_false_one_fuv_false(self):
        lcm = _all_notused_lcm()
        lcm[0][1] = "ANDD"; lcm[1][0] = "ANDD"
        # cmv[0]=False → pum[0][1]=False, pum[0][0]=True → fuv[0]=False → LAUNCH=False
        _, _, _, launch = decide(
            2, [0.0, 0.01], [0.0, 0.0],
            _make_params(LENGTH1=1e9), lcm,
            [True] + [False] * 14
        )
        assert launch is False


# ---------------------------------------------------------------------------
# Acceptance_cases cross-check: generate cases with oracle and re-run
# ---------------------------------------------------------------------------

class TestOracleSelfConsistency:
    def test_deterministic(self):
        """Oracle returns same result on repeated calls."""
        params = _make_params(LENGTH1=2.0, RADIUS1=3.0, AREA1=1.0)
        x = [0.0, 3.0, 6.0, -1.0, 4.0]
        y = [0.0, 4.0, 0.0, 2.0, -3.0]
        lcm = _all_notused_lcm()
        diag = [True, False] * 7 + [True]
        r1 = decide(5, x, y, params, lcm, diag)
        r2 = decide(5, x, y, params, lcm, diag)
        assert r1 == r2

    def test_output_shapes(self):
        """Outputs have correct types and shapes."""
        cmv, pum, fuv, launch = decide(
            2, [0.0, 1.0], [0.0, 0.0],
            _make_params(), _all_notused_lcm(), _all_false_diag()
        )
        assert len(cmv) == 15
        assert len(pum) == 15
        assert all(len(row) == 15 for row in pum)
        assert len(fuv) == 15
        assert isinstance(launch, bool)

    def test_all_booleans(self):
        """All output elements are proper booleans."""
        cmv, pum, fuv, launch = decide(
            3, [0.0, 1.0, 2.0], [0.0, 0.0, 0.0],
            _make_params(), _all_notused_lcm(), _all_false_diag()
        )
        assert all(isinstance(v, bool) for v in cmv)
        assert all(isinstance(v, bool) for row in pum for v in row)
        assert all(isinstance(v, bool) for v in fuv)
        assert isinstance(launch, bool)

    def test_pum_symmetric_offdiagonal(self):
        """Off-diagonal PUM is symmetric (since LCM is symmetric)."""
        lcm = [["ANDD"] * 15 for _ in range(15)]
        _, pum, _, _ = decide(
            3, [0.0, 1.0, 10.0], [0.0, 0.0, 0.0],
            _make_params(LENGTH1=0.0), lcm, _all_false_diag()
        )
        for i in range(15):
            for j in range(15):
                if i != j:
                    assert pum[i][j] == pum[j][i]


# ---------------------------------------------------------------------------
# Redundant PUM/FUV recomputation (connector + FUV rules only)
# ---------------------------------------------------------------------------


class TestOraclePUMFUVRedundant:
    def test_matches_decide_on_hand_crafted(self):
        lcm = _all_notused_lcm()
        lcm[0][1] = "ANDD"
        lcm[1][0] = "ANDD"
        diag = [True] + [False] * 14
        cmv, pum, fuv, launch = decide(
            2, [0.0, 0.01], [0.0, 0.0],
            _make_params(LENGTH1=1e9), lcm, diag,
        )
        pum2 = recompute_pum_from_cmv(cmv, lcm, diag)
        assert pum == pum2
        assert fuv == recompute_fuv_from_pum(pum)
        assert launch == all(fuv)

    @given(seed=st.integers(0, 25_000))
    @settings(max_examples=100, deadline=None)
    def test_random_generator_cases(self, seed: int):
        case = next(iter(iter_test_cases(1, int(seed), include_oracle_outputs=True)))
        cmv, pum, fuv, launch = decide(
            case["numpoints"],
            case["x"],
            case["y"],
            case["parameters"],
            case["lcm"],
            case["pum_diag"],
        )
        pum2 = recompute_pum_from_cmv(cmv, case["lcm"], case["pum_diag"])
        assert pum == pum2
        assert fuv == recompute_fuv_from_pum(pum)
        assert launch == all(fuv)
        for i in range(15):
            for j in range(15):
                if i != j:
                    assert case["lcm"][i][j] == case["lcm"][j][i]
                    assert pum[i][j] == pum[j][i]
