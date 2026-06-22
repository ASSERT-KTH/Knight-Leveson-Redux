"""
Mock agent — deterministic fallback for pipeline validation.

Produces three variants with distinct fault profiles, without any API call.
The variants are deliberately imperfect to exercise the statistical pipeline.

Fault profiles
--------------
mock_A  (run_id % 3 == 0):
    Correct implementation — used as a "perfect" baseline.
    Failure rate ≈ 0%.

mock_B  (run_id % 3 == 1):
    Bug in LIC 5 quadrant assignment: treats (0,y) with y>0 as Q2 (wrong),
    and (x,0) with x>0 as Q4 (wrong). This violates the spec's priority rule.
    Creates systematic failures on inputs with boundary-quadrant points.

mock_C  (run_id % 3 == 2):
    Bug in LIC 2/9/14 circumscribed circle: always uses the circumscribed
    circle formula (ignores obtuse/right triangle case), so it under-estimates
    the enclosing circle radius for right/obtuse triangles.
    Creates failures when test cases involve obtuse triangles and RADIUS1
    is between the circumscribed and actual minimum enclosing circle radii.

These variants are NOT designed to simulate real agent behavior.
They exist solely to validate that the framework infrastructure (acceptance
screening, campaign execution, z-statistic, heatmap) runs correctly end-to-end.
"""
from __future__ import annotations

import tempfile
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agents.base import AgentBase, VersionRecord


# ---------------------------------------------------------------------------
# Variant source code templates
# ---------------------------------------------------------------------------

_HEADER = textwrap.dedent("""\
    from __future__ import annotations
    import json
    import math
    import sys

    PI = math.pi

    def realcompare(a: float, b: float) -> str:
        scale = max(abs(a), abs(b), 1.0)
        eps = 0.5e-5 * scale
        diff = a - b
        if diff > eps:
            return "GT"
        if diff < -eps:
            return "LT"
        return "EQ"

    def rc_lt(a, b): return realcompare(a, b) == "LT"
    def rc_gt(a, b): return realcompare(a, b) == "GT"
    def rc_eq(a, b): return realcompare(a, b) == "EQ"
    def rc_le(a, b): return realcompare(a, b) in ("LT", "EQ")
    def rc_ge(a, b): return realcompare(a, b) in ("GT", "EQ")

    def _dist(x1, y1, x2, y2):
        return math.sqrt((x2-x1)**2 + (y2-y1)**2)

    def _triangle_area(x1, y1, x2, y2, x3, y3):
        return abs((x2-x1)*(y3-y1) - (x3-x1)*(y2-y1)) / 2.0

    def _point_to_line_dist(px, py, x1, y1, x2, y2):
        dx, dy = x2-x1, y2-y1
        length = math.sqrt(dx*dx + dy*dy)
        if rc_eq(length, 0.0):
            return _dist(px, py, x1, y1)
        return abs(dx*(y1-py) - (x1-px)*dy) / length

    def _angle_at_vertex(x1, y1, vx, vy, x3, y3):
        if rc_eq(_dist(x1,y1,vx,vy), 0.0) or rc_eq(_dist(x3,y3,vx,vy), 0.0):
            return None
        ux, uy = x1-vx, y1-vy
        wx, wy = x3-vx, y3-vy
        cross_mag = math.sqrt((ux*ux+uy*uy)*(wx*wx+wy*wy))
        if rc_eq(cross_mag, 0.0):
            return None
        cos_a = max(-1.0, min(1.0, (ux*wx+uy*wy)/cross_mag))
        return math.acos(cos_a)
""")

# Correct circumscribed radius (used by mock_A)
_CIRCUM_CORRECT = textwrap.dedent("""\
    def _circumscribed_radius(x1, y1, x2, y2, x3, y3):
        a = _dist(x2,y2,x3,y3); b = _dist(x1,y1,x3,y3); c = _dist(x1,y1,x2,y2)
        area2 = abs((x2-x1)*(y3-y1) - (x3-x1)*(y2-y1))
        if rc_eq(area2, 0.0):
            return max(a,b,c)/2.0
        sides = sorted([a,b,c])
        if rc_ge(sides[2]*sides[2], sides[0]*sides[0]+sides[1]*sides[1]):
            return sides[2]/2.0
        return (a*b*c)/(4.0*(area2/2.0))
""")

# Buggy circumscribed radius: always uses circumscribed circle formula,
# ignoring the obtuse/right triangle case (mock_C fault)
_CIRCUM_BUGGY_C = textwrap.dedent("""\
    def _circumscribed_radius(x1, y1, x2, y2, x3, y3):
        a = _dist(x2,y2,x3,y3); b = _dist(x1,y1,x3,y3); c = _dist(x1,y1,x2,y2)
        area2 = abs((x2-x1)*(y3-y1) - (x3-x1)*(y2-y1))
        if rc_eq(area2, 0.0):
            return max(a,b,c)/2.0
        # BUG: always use circumscribed formula, no obtuse check
        return (a*b*c)/(4.0*(area2/2.0))
""")

# Correct quadrant (used by mock_A and mock_C)
_QUAD_CORRECT = textwrap.dedent("""\
    def _quadrant(px, py):
        if px >= 0 and py >= 0: return 1
        if px < 0 and py >= 0: return 2
        if px <= 0 and py < 0: return 3
        return 4
""")

# Buggy quadrant: wrong boundary handling (used only in mock_C, as an ADDITIONAL bug)
# Treats (0, y>0) as Q2 and (x>0, 0) as Q4 — violates priority rule
_QUAD_BUGGY_C2 = textwrap.dedent("""\
    def _quadrant(px, py):
        # BUG: wrong boundary handling — does not implement priority rule
        if px > 0 and py > 0: return 1
        if px <= 0 and py > 0: return 2   # (0,y>0) goes here instead of Q1
        if px < 0 and py <= 0: return 3
        if px >= 0 and py < 0: return 4   # (x>0, 0) goes here instead of Q1
        return 1  # origin
""")

_DECIDE_BODY = textwrap.dedent("""\

    def decide(numpoints, x, y, parameters, lcm, pum_diag):
        p = parameters

        def lic1():
            for i in range(numpoints-1):
                if rc_gt(_dist(x[i],y[i],x[i+1],y[i+1]), p['LENGTH1']): return True
            return False

        def lic2():
            for i in range(numpoints-2):
                r = _circumscribed_radius(x[i],y[i],x[i+1],y[i+1],x[i+2],y[i+2])
                if rc_gt(r, p['RADIUS1']): return True
            return False

        def lic3():
            eps = p['EPSILON']
            for i in range(numpoints-2):
                ang = _angle_at_vertex(x[i],y[i],x[i+1],y[i+1],x[i+2],y[i+2])
                if ang is None: continue
                if rc_lt(ang, PI-eps) or rc_gt(ang, PI+eps): return True
            return False

        def lic4():
            for i in range(numpoints-2):
                if rc_gt(_triangle_area(x[i],y[i],x[i+1],y[i+1],x[i+2],y[i+2]), p['AREA1']): return True
            return False

        def lic5():
            q_pts, quads = p['Q_PTS'], p['QUADS']
            for i in range(numpoints-q_pts+1):
                seen = set(_quadrant(x[i+j], y[i+j]) for j in range(q_pts))
                if len(seen) > quads: return True
            return False

        def lic6():
            for i in range(numpoints-1):
                if rc_lt(x[i+1]-x[i], 0.0): return True
            return False

        def lic7():
            if numpoints < 3: return False
            n_pts, dist = p['N_PTS'], p['DIST']
            for i in range(numpoints-n_pts+1):
                x1,y1=x[i],y[i]; x2,y2=x[i+n_pts-1],y[i+n_pts-1]
                coinc = rc_eq(_dist(x1,y1,x2,y2), 0.0)
                for k in range(1, n_pts-1):
                    d = _dist(x[i+k],y[i+k],x1,y1) if coinc else _point_to_line_dist(x[i+k],y[i+k],x1,y1,x2,y2)
                    if rc_gt(d, dist): return True
            return False

        def lic8():
            if numpoints < 3: return False
            k_pts = p['K_PTS']
            for i in range(numpoints-k_pts-1):
                if rc_gt(_dist(x[i],y[i],x[i+k_pts+1],y[i+k_pts+1]), p['LENGTH1']): return True
            return False

        def lic9():
            if numpoints < 5: return False
            a,b = p['A_PTS'], p['B_PTS']
            for i in range(numpoints-a-b-2):
                j,k = i+a+1, i+a+b+2
                if rc_gt(_circumscribed_radius(x[i],y[i],x[j],y[j],x[k],y[k]), p['RADIUS1']): return True
            return False

        def lic10():
            if numpoints < 5: return False
            c,d,eps = p['C_PTS'], p['D_PTS'], p['EPSILON']
            for i in range(numpoints-c-d-2):
                j,k = i+c+1, i+c+d+2
                ang = _angle_at_vertex(x[i],y[i],x[j],y[j],x[k],y[k])
                if ang is None: continue
                if rc_lt(ang, PI-eps) or rc_gt(ang, PI+eps): return True
            return False

        def lic11():
            if numpoints < 5: return False
            e,f = p['E_PTS'], p['F_PTS']
            for i in range(numpoints-e-f-2):
                j,k = i+e+1, i+e+f+2
                if rc_gt(_triangle_area(x[i],y[i],x[j],y[j],x[k],y[k]), p['AREA1']): return True
            return False

        def lic12():
            if numpoints < 3: return False
            g = p['G_PTS']
            for i in range(numpoints-g-1):
                if rc_lt(x[i+g+1]-x[i], 0.0): return True
            return False

        def lic13():
            if numpoints < 3: return False
            k,l1,l2 = p['K_PTS'], p['LENGTH1'], p['LENGTH2']
            c1,c2 = False,False
            for i in range(numpoints-k-1):
                d = _dist(x[i],y[i],x[i+k+1],y[i+k+1])
                if rc_gt(d,l1): c1=True
                if rc_lt(d,l2): c2=True
            return c1 and c2

        def lic14():
            if numpoints < 5: return False
            a,b,r1,r2 = p['A_PTS'], p['B_PTS'], p['RADIUS1'], p['RADIUS2']
            c1,c2 = False,False
            for i in range(numpoints-a-b-2):
                j,k = i+a+1, i+a+b+2
                r = _circumscribed_radius(x[i],y[i],x[j],y[j],x[k],y[k])
                if rc_gt(r,r1): c1=True
                if rc_le(r,r2): c2=True
            return c1 and c2

        def lic15():
            if numpoints < 5: return False
            e,f,a1,a2 = p['E_PTS'], p['F_PTS'], p['AREA1'], p['AREA2']
            c1,c2 = False,False
            for i in range(numpoints-e-f-2):
                j,k = i+e+1, i+e+f+2
                area = _triangle_area(x[i],y[i],x[j],y[j],x[k],y[k])
                if rc_gt(area,a1): c1=True
                if rc_lt(area,a2): c2=True
            return c1 and c2

        cmv = [lic1(),lic2(),lic3(),lic4(),lic5(),lic6(),lic7(),lic8(),
               lic9(),lic10(),lic11(),lic12(),lic13(),lic14(),lic15()]

        pum = [[False]*15 for _ in range(15)]
        for i in range(15):
            for j in range(15):
                if i == j:
                    pum[i][j] = pum_diag[i]
                else:
                    conn = lcm[i][j]
                    if conn == "NOTUSED": pum[i][j] = True
                    elif conn == "ANDD":  pum[i][j] = cmv[i] and cmv[j]
                    elif conn == "ORR":   pum[i][j] = cmv[i] or cmv[j]

        fuv = []
        for i in range(15):
            if not pum[i][i]:
                fuv.append(True)
            else:
                fuv.append(all(pum[i][j] for j in range(15)))

        return cmv, pum, fuv, all(fuv)
""")

_CLI_FOOTER = textwrap.dedent("""\

    if __name__ == "__main__":
        payload = json.load(sys.stdin)
        cmv, pum, fuv, launch = decide(
            payload["numpoints"],
            payload["x"],
            payload["y"],
            payload["parameters"],
            payload["lcm"],
            payload["pum_diag"],
        )
        json.dump({"cmv": cmv, "pum": pum, "fuv": fuv, "launch": launch}, sys.stdout)
""")



def _build_source(circum_fn: str, quad_fn: str) -> str:
    return _HEADER + circum_fn + quad_fn + _DECIDE_BODY + _CLI_FOOTER


# Three variant source codes
# mock_B shares the circumscribed-circle bug with mock_C → correlated failures
# mock_C has BOTH bugs (circumscribed-circle + quadrant boundary) → slightly higher rate
MOCK_VARIANTS = {
    "mock_A": _build_source(_CIRCUM_CORRECT, _QUAD_CORRECT),
    "mock_B": _build_source(_CIRCUM_BUGGY_C, _QUAD_CORRECT),
    "mock_C": _build_source(_CIRCUM_BUGGY_C, _QUAD_BUGGY_C2),
}

MOCK_DESCRIPTIONS = {
    "mock_A": "Correct implementation (oracle-equivalent)",
    "mock_B": "Bug: LICs 2/9/14 circumscribed circle ignores obtuse/right-triangle case",
    "mock_C": "Bug: same circumscribed circle bug as B PLUS LIC-5 quadrant boundary rule violated",
}


class MockAgent(AgentBase):
    """
    Mock agent that produces one of three deterministic variants.

    Variant selection: run_id % 3
      0 → mock_A (correct)
      1 → mock_B (quadrant bug)
      2 → mock_C (circumscribed circle bug)
    """
    name = "mock"
    default_model = "mock"

    def _invoke(self, sandbox: Path, prompt: str) -> tuple[str, str, str]:
        # Never raises AgentUnavailableError — always available
        variant_key = f"mock_{['A', 'B', 'C'][self.config.get('run_id', 0) % 3]}"
        source = MOCK_VARIANTS[variant_key]
        (sandbox / "decide.py").write_text(source)
        return source, variant_key, "ok"

    def generate_version(
        self,
        spec_path: Path,
        run_id: int,
        *,
        language: str = "python",
    ) -> VersionRecord:
        self.config["run_id"] = run_id
        if language != "python":
            ts = datetime.now(timezone.utc).isoformat()
            return VersionRecord(
                agent_name=self.name,
                model_name="mock",
                run_id=run_id,
                prompt="",
                source_code="",
                timestamp=ts,
                generation_config=self._get_generation_config(),
                acceptance_passed=None,
                build_status="api_unavailable",
                sandbox_dir=str(Path(tempfile.mkdtemp(prefix="nvp_mock_skip_"))),
                error_message="mock agent supports Python only; use language: python for pipeline tests",
                language=language,
            )
        return super().generate_version(spec_path, run_id, language=language)

    def _get_generation_config(self) -> dict:
        run_id = self.config.get("run_id", 0)
        variant_key = f"mock_{['A', 'B', 'C'][run_id % 3]}"
        return {
            "agent": "mock",
            "variant": variant_key,
            "description": MOCK_DESCRIPTIONS[variant_key],
        }
