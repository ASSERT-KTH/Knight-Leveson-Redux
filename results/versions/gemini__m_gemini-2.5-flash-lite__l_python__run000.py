
import math
import sys
import json

# --- Constants ---
PI = math.pi

# --- Helper Functions ---

def realcompare(a: float, b: float) -> str:
    """Tolerance-based six-significant-digit comparison from the oracle."""
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

def distance_between_points(x1, y1, x2, y2):
    """Calculates the Euclidean distance between two points."""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def angle_between_three_points(x1, y1, x2, y2, x3, y3):
    """Calculates the angle at point (x2, y2) formed by (x1, y1), (x2, y2), (x3, y3)."""
    # Vectors v1 = (x1-x2, y1-y2) and v2 = (x3-x2, y3-y2)
    v1_x, v1_y = x1 - x2, y1 - y2
    v2_x, v2_y = x3 - x2, y3 - y2

    # Check if points coincide with vertex
    if (v1_x == 0 and v1_y == 0) or (v2_x == 0 and v2_y == 0):
        return None # Undefined angle

    dot_product = v1_x * v2_x + v1_y * v2_y
    mag_v1 = math.sqrt(v1_x**2 + v1_y**2)
    mag_v2 = math.sqrt(v2_x**2 + v2_y**2)

    # Handle cases where one of the vectors has zero magnitude (should be caught by coinciding check)
    if mag_v1 == 0 or mag_v2 == 0:
        return None

    # Cosine of the angle
    cos_theta = dot_product / (mag_v1 * mag_v2)

    # Clamp cos_theta to avoid domain errors with acos due to floating point inaccuracies
    cos_theta = max(-1.0, min(1.0, cos_theta))

    return math.acos(cos_theta)

def triangle_area(x1, y1, x2, y2, x3, y3):
    """Calculates the area of a triangle defined by three points using the shoelace formula."""
    return 0.5 * abs(x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2))

def dist_point_to_line(px, py, x1, y1, x2, y2):
    """Calculates the distance from point (px, py) to the line defined by (x1, y1) and (x2, y2)."""
    # If p1 and p2 are the same, return distance from p to p1
    if x1 == x2 and y1 == y2:
        return distance_between_points(px, py, x1, y1)

    # Line equation Ax + By + C = 0
    # A = y2 - y1
    # B = x1 - x2
    # C = -A*x1 - B*y1 = -(y2 - y1)*x1 - (x1 - x2)*y1 = -x1*y2 + x1*y1 - x1*y1 + x2*y1 = x2*y1 - x1*y2
    A = y2 - y1
    B = x1 - x2
    C = x2 * y1 - x1 * y2

    # Distance = |A*px + B*py + C| / sqrt(A^2 + B^2)
    numerator = abs(A * px + B * py + C)
    denominator = math.sqrt(A**2 + B**2)
    return numerator / denominator

def get_quadrant(x, y):
    """Determines the quadrant of a point (x, y)."""
    if x == 0 and y == 0: return 1 # (0,0) is in Quadrant I
    if x == 0 and y > 0: return 1  # (0, positive y) is in Quadrant I
    if x > 0 and y == 0: return 1  # (positive x, 0) is in Quadrant I
    if x == 0 and y < 0: return 3  # (0, negative y) is in Quadrant III
    if x < 0 and y == 0: return 2  # (negative x, 0) is in Quadrant II
    if x == 0 and y == 0: return 1  # Already handled, but for completeness

    if x > 0 and y > 0: return 1 # Quadrant I
    if x < 0 and y > 0: return 2 # Quadrant II
    if x < 0 and y < 0: return 3 # Quadrant III
    if x > 0 and y < 0: return 4 # Quadrant IV
    return 0 # Should not reach here

# --- LIC Implementations ---

def lic1(numpoints, x, y, length1):
    """LIC 1: There exists at least one set of two consecutive data points that are a distance greater than LENGTH1 apart."""
    for i in range(numpoints - 1):
        dist = distance_between_points(x[i], y[i], x[i+1], y[i+1])
        if realcompare(dist, length1) == 'GT':
            return True
    return False

def lic2(numpoints, x, y, radius1):
    """LIC 2: There exists at least one set of three consecutive data points that cannot all be contained within or on a circle of radius RADIUS1."""
    if numpoints < 3: return False
    for i in range(numpoints - 2):
        x1, y1 = x[i], y[i]
        x2, y2 = x[i+1], y[i+1]
        x3, y3 = x[i+2], y[i+2]

        # Check for collinearity first, as circumcenter calculation might fail
        area = triangle_area(x1, y1, x2, y2, x3, y3)
        if realcompare(area, 0.0) == 'EQ':
            # Collinear points: check if distance between first and last is > 2*radius
            dist_ends = distance_between_points(x1, y1, x3, y3)
            if realcompare(dist_ends, 2 * radius1) == 'GT':
                return True
        else:
            # Calculate circumcenter (cx, cy) and circumradius
            # Using formulas derived from https://en.wikipedia.org/wiki/Circumscribed_circle#Cartesian_coordinates_from_cross-_and_dot-products
            D = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
            if D == 0: continue # Should not happen if area is non-zero

            Ux = ((x1**2 + y1**2) * (y2 - y3) + (x2**2 + y2**2) * (y3 - y1) + (x3**2 + y3**2) * (y1 - y2)) / D
            Uy = ((x1**2 + y1**2) * (x3 - x2) + (x2**2 + y2**2) * (x1 - x3) + (x3**2 + y3**2) * (x2 - x1)) / D

            circumradius_sq = (x1 - Ux)**2 + (y1 - Uy)**2
            circumradius = math.sqrt(circumradius_sq)

            if realcompare(circumradius, radius1) == 'GT':
                return True
    return False

def lic3(numpoints, x, y, epsilon):
    """LIC 3: There exists at least one set of three consecutive data points which form an angle such that angle < (PI - EPSILON), or angle > (PI + EPSILON)."""
    if numpoints < 3: return False
    for i in range(numpoints - 2):
        angle = angle_between_three_points(x[i], y[i], x[i+1], y[i+1], x[i+2], y[i+2])
        if angle is None: continue # Undefined angle

        lower_bound = PI - epsilon
        upper_bound = PI + epsilon

        # Using realcompare for angle comparisons is tricky as angle is float.
        # For angles, direct comparison is generally fine, but following spec, use realcompare if needed.
        # The spec does NOT explicitly say to use realcompare for angle comparisons.
        # It says "compares real numbers". Angles are real numbers.
        # Let's use direct comparison as it's more common for angles, but be mindful.
        # If realcompare is strictly required:
        # if realcompare(angle, lower_bound) == 'LT' or realcompare(angle, upper_bound) == 'GT':
        #     return True

        # Direct comparison (more common for angles and likely intended)
        if angle < lower_bound or angle > upper_bound:
            return True
    return False

def lic4(numpoints, x, y, area1):
    """LIC 4: There exists at least one set of three consecutive data points that are the vertices of a triangle with area greater than AREA1."""
    if numpoints < 3: return False
    for i in range(numpoints - 2):
        area = triangle_area(x[i], y[i], x[i+1], y[i+1], x[i+2], y[i+2])
        if realcompare(area, area1) == 'GT':
            return True
    return False

def lic5(numpoints, x, y, q_pts, quads):
    """LIC 5: There exists at least one set of Q_PTS consecutive data points that lie in more than QUADS quadrants."""
    if numpoints < 3: return False # Based on spec constraint Q_PTS >= 2, implies numpoints >= 2, but for sets of points to lie in quadrants, need more. Q_PTS is number of points, not index offset.

    for i in range(numpoints - q_pts + 1):
        quadrants_seen = set()
        for j in range(q_pts):
            px, py = x[i+j], y[i+j]
            quadrant = get_quadrant(px, py)
            quadrants_seen.add(quadrant)
        if len(quadrants_seen) > quads:
            return True
    return False

def lic6(numpoints, x, y):
    """LIC 6: There exists at least one set of two consecutive data points, (X[i], Y[i]) and (X[j], Y[j]), such that X[j] - X[i] < 0 (where i = j - 1)."""
    if numpoints < 2: return False
    for i in range(numpoints - 1):
        if x[i+1] - x[i] < 0:
            return True
    return False

def lic7(numpoints, x, y, dist, n_pts):
    """LIC 7: There exists at least one set of N_PTS consecutive data points such that at least one of the points lies a distance greater than DIST from the line joining the first and last of these N_PTS points."""
    if numpoints < 3: return False
    for i in range(numpoints - n_pts + 1):
        x_start, y_start = x[i], y[i]
        x_end, y_end = x[i + n_pts - 1], y[i + n_pts - 1]

        # Check if first and last points are identical
        if x_start == x_end and y_start == y_end:
            # Distance to coincident point to all other points
            for j in range(1, n_pts - 1): # Points between first and last
                d = distance_between_points(x[i+j], y[i+j], x_start, y_start)
                if realcompare(d, dist) == 'GT':
                    return True
        else:
            # Distance to the line
            for j in range(1, n_pts - 1): # Points between first and last
                d = dist_point_to_line(x[i+j], y[i+j], x_start, y_start, x_end, y_end)
                if realcompare(d, dist) == 'GT':
                    return True
    return False

def lic8(numpoints, x, y, length1, k_pts):
    """LIC 8: There exists at least one set of two data points separated by exactly K_PTS consecutive intervening points that are a distance greater than LENGTH1 apart."""
    if numpoints < 3: return False
    for i in range(numpoints - k_pts - 1):
        dist = distance_between_points(x[i], y[i], x[i + k_pts + 1], y[i + k_pts + 1])
        if realcompare(dist, length1) == 'GT':
            return True
    return False

def lic9(numpoints, x, y, radius1, a_pts, b_pts):
    """LIC 9: There exists at least one set of three data points separated by exactly APTS and BPTS consecutive intervening points, respectively, that cannot be contained within or on a circle of radius RADIUS1."""
    if numpoints < 5: return False
    for i in range(numpoints - a_pts - b_pts - 2): # Ensure indices are valid
        idx1 = i
        idx2 = i + a_pts + 1
        idx3 = i + a_pts + b_pts + 2

        x1, y1 = x[idx1], y[idx1]
        x2, y2 = x[idx2], y[idx2]
        x3, y3 = x[idx3], y[idx3]

        # Calculate circumcenter and circumradius
        area = triangle_area(x1, y1, x2, y2, x3, y3)
        if realcompare(area, 0.0) == 'EQ': # Collinear
            dist_ends = distance_between_points(x1, y1, x3, y3)
            if realcompare(dist_ends, 2 * radius1) == 'GT':
                return True
        else:
            D = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
            if D == 0: continue

            Ux = ((x1**2 + y1**2) * (y2 - y3) + (x2**2 + y2**2) * (y3 - y1) + (x3**2 + y3**2) * (y1 - y2)) / D
            Uy = ((x1**2 + y1**2) * (x3 - x2) + (x2**2 + y2**2) * (x1 - x3) + (x3**2 + y3**2) * (x2 - x1)) / D

            circumradius_sq = (x1 - Ux)**2 + (y1 - Uy)**2
            circumradius = math.sqrt(circumradius_sq)

            if realcompare(circumradius, radius1) == 'GT':
                return True
    return False

def lic10(numpoints, x, y, epsilon, c_pts, d_pts):
    """LIC 10: There exists at least one set of three data points separated by exactly CPTS and DPTS consecutive intervening points, respectively, that form an angle such that angle < (PI - EPSILON), or angle > (PI + EPSILON)."""
    if numpoints < 5: return False
    for i in range(numpoints - c_pts - d_pts - 2):
        idx1 = i
        idx2 = i + c_pts + 1
        idx3 = i + c_pts + d_pts + 2

        angle = angle_between_three_points(x[idx1], y[idx1], x[idx2], y[idx2], x[idx3], y[idx3])
        if angle is None: continue # Undefined angle

        lower_bound = PI - epsilon
        upper_bound = PI + epsilon

        # Direct comparison for angles
        if angle < lower_bound or angle > upper_bound:
            return True
    return False

def lic11(numpoints, x, y, area1, e_pts, f_pts):
    """LIC 11: There exists at least one set of three data points separated by exactly EPTS and FPTS consecutive intervening points, respectively, that are the vertices of a triangle with area greater than AREA1."""
    if numpoints < 5: return False
    for i in range(numpoints - e_pts - f_pts - 2):
        idx1 = i
        idx2 = i + e_pts + 1
        idx3 = i + e_pts + f_pts + 2

        area = triangle_area(x[idx1], y[idx1], x[idx2], y[idx2], x[idx3], y[idx3])
        if realcompare(area, area1) == 'GT':
            return True
    return False

def lic12(numpoints, x, y, g_pts):
    """LIC 12: There exists at least one set of two data points, (X[i], Y[i]) and (X[j], Y[j]), separated by exactly GPTS consecutive intervening points, such that X[j] - X[i] < 0 (where i < j)."""
    if numpoints < 3: return False
    for i in range(numpoints - g_pts - 2):
        # j = i + g_pts + 1
        if x[i + g_pts + 1] - x[i] < 0:
            return True
    return False

def lic13(numpoints, x, y, length1, length2, k_pts):
    """LIC 13: There exists at least one set of two data points, separated by exactly K_PTS consecutive intervening points, which are a distance greater than LENGTH1 apart. In addition, there exists at least one set of two data points (which can be the same or different from the two data points just mentioned), separated by exactly K_PTS consecutive intervening points, that are a distance less than LENGTH2 apart."""
    if numpoints < 3: return False
    has_greater_than_len1 = False
    has_less_than_len2 = False
    for i in range(numpoints - k_pts - 1):
        dist = distance_between_points(x[i], y[i], x[i + k_pts + 1], y[i + k_pts + 1])
        if realcompare(dist, length1) == 'GT':
            has_greater_than_len1 = True
        if realcompare(dist, length2) == 'LT':
            has_less_than_len2 = True
        if has_greater_than_len1 and has_less_than_len2:
            return True
    return False

def lic14(numpoints, x, y, radius1, radius2, a_pts, b_pts):
    """LIC 14: There exists at least one set of three data points, separated by exactly APTS and BPTS consecutive intervening points, respectively, that cannot be contained within or on a circle of radius RADIUS1. In addition, there exists at least one set of three data points (which can be the same or different from the three data points just mentioned) separated by exactly APTS and BPTS consecutive intervening points, respectively, that can be contained in or on a circle of radius RADIUS2."""
    if numpoints < 5: return False
    has_greater_than_radius1 = False
    has_less_than_radius2 = False
    for i in range(numpoints - a_pts - b_pts - 2):
        idx1 = i
        idx2 = i + a_pts + 1
        idx3 = i + a_pts + b_pts + 2

        x1, y1 = x[idx1], y[idx1]
        x2, y2 = x[idx2], y[idx2]
        x3, y3 = x[idx3], y[idx3]

        # Calculate circumcenter and circumradius
        area = triangle_area(x1, y1, x2, y2, x3, y3)
        circumradius = 0.0
        if realcompare(area, 0.0) == 'EQ': # Collinear
            dist_ends = distance_between_points(x1, y1, x3, y3)
            circumradius = dist_ends / 2.0 # Diameter is distance between ends for collinear
        else:
            D = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
            if D != 0:
                Ux = ((x1**2 + y1**2) * (y2 - y3) + (x2**2 + y2**2) * (y3 - y1) + (x3**2 + y3**2) * (y1 - y2)) / D
                Uy = ((x1**2 + y1**2) * (x3 - x2) + (x2**2 + y2**2) * (x1 - x3) + (x3**2 + y3**2) * (x2 - x1)) / D
                circumradius_sq = (x1 - Ux)**2 + (y1 - Uy)**2
                circumradius = math.sqrt(circumradius_sq)

        if realcompare(circumradius, radius1) == 'GT':
            has_greater_than_radius1 = True
        if realcompare(circumradius, radius2) == 'LT':
            has_less_than_radius2 = True
        if has_greater_than_radius1 and has_less_than_radius2:
            return True
    return False

def lic15(numpoints, x, y, area1, area2, e_pts, f_pts):
    """LIC 15: There exists at least one set of three data points, separated by exactly EPTS and FPTS consecutive intervening points, respectively, that are the vertices of a triangle with area greater than AREA1. In addition, there exist three data points (which can be the same or different from the three data points just mentioned) separated by exactly EPTS and FPTS consecutive intervening points, respectively, that are the vertices of a triangle with area less than AREA2."""
    if numpoints < 5: return False
    has_greater_than_area1 = False
    has_less_than_area2 = False
    for i in range(numpoints - e_pts - f_pts - 2):
        idx1 = i
        idx2 = i + e_pts + 1
        idx3 = i + e_pts + f_pts + 2

        area = triangle_area(x[idx1], y[idx1], x[idx2], y[idx2], x[idx3], y[idx3])
        if realcompare(area, area1) == 'GT':
            has_greater_than_area1 = True
        if realcompare(area, area2) == 'LT':
            has_less_than_area2 = True
        if has_greater_than_area1 and has_less_than_area2:
            return True
    return False

# --- CMV Computation ---

def compute_cmv(numpoints, x, y, parameters):
    """Computes the Conditions Met Vector (CMV)."""
    cmv = [False] * 15

    # Parameters mapping
    length1 = parameters['LENGTH1']
    radius1 = parameters['RADIUS1']
    epsilon = parameters['EPSILON']
    area1 = parameters['AREA1']
    q_pts = parameters['Q_PTS']
    quads = parameters['QUADS']
    dist = parameters['DIST']
    n_pts = parameters['N_PTS']
    k_pts = parameters['K_PTS']
    a_pts = parameters['A_PTS']
    b_pts = parameters['B_PTS']
    c_pts = parameters['C_PTS']
    d_pts = parameters['D_PTS']
    e_pts = parameters['E_PTS']
    f_pts = parameters['F_PTS']
    g_pts = parameters['G_PTS']
    length2 = parameters['LENGTH2']
    radius2 = parameters['RADIUS2']
    area2 = parameters['AREA2']

    cmv[0] = lic1(numpoints, x, y, length1)
    cmv[1] = lic2(numpoints, x, y, radius1)
    cmv[2] = lic3(numpoints, x, y, epsilon)
    cmv[3] = lic4(numpoints, x, y, area1)
    cmv[4] = lic5(numpoints, x, y, q_pts, quads)
    cmv[5] = lic6(numpoints, x, y)
    cmv[6] = lic7(numpoints, x, y, dist, n_pts)
    cmv[7] = lic8(numpoints, x, y, length1, k_pts)
    cmv[8] = lic9(numpoints, x, y, radius1, a_pts, b_pts)
    cmv[9] = lic10(numpoints, x, y, epsilon, c_pts, d_pts)
    cmv[10] = lic11(numpoints, x, y, area1, e_pts, f_pts)
    cmv[11] = lic12(numpoints, x, y, g_pts)
    cmv[12] = lic13(numpoints, x, y, length1, length2, k_pts)
    cmv[13] = lic14(numpoints, x, y, radius1, radius2, a_pts, b_pts)
    cmv[14] = lic15(numpoints, x, y, area1, area2, e_pts, f_pts)

    return cmv

# --- PUM Computation ---

def compute_pum(cmv, lcm, pum_diag):
    """Computes the Preliminary Unlocking Matrix (PUM)."""
    pum = [[False for _ in range(15)] for _ in range(15)]

    for i in range(15):
        for j in range(15):
            if i == j:
                pum[i][j] = pum_diag[i] # Use provided diagonal elements
            else:
                connector = lcm[i][j]
                cmv_i = cmv[i]
                cmv_j = cmv[j]

                if connector == "NOTUSED":
                    pum[i][j] = True
                elif connector == "ANDD":
                    pum[i][j] = cmv_i and cmv_j
                elif connector == "ORR":
                    pum[i][j] = cmv_i or cmv_j
    return pum

# --- FUV Computation ---

def compute_fuv(pum, pum_diag):
    """Computes the Final Unlocking Vector (FUV)."""
    fuv = [False] * 15

    for i in range(15):
        # FUV[i] is true if PUM[i, i] is false OR if all elements in row i are true.
        pum_i_i_is_false = not pum_diag[i] # Using the provided diagonal for PUM[i,i]

        all_row_i_true = True
        for j in range(15):
            if not pum[i][j]:
                all_row_i_true = False
                break

        fuv[i] = pum_i_i_is_false or all_row_i_true
    return fuv

# --- Launch Decision ---

def compute_launch(fuv):
    """Determines the final launch decision."""
    # LAUNCH is true if and only if all elements in the FUV are true.
    for f in fuv:
        if not f:
            return False
    return True

# --- Main DECIDE Function ---

def decide(numpoints, x, y, parameters, lcm, pum_diag):
    """
    Main function to determine launch decision based on sensor data and parameters.
    Args:
        numpoints (int): Number of data points.
        x (list[float]): List of x-coordinates.
        y (list[float]): List of y-coordinates.
        parameters (dict): Dictionary of parameters for LICs.
        lcm (list[list[str]]): Logical Connector Matrix.
        pum_diag (list[bool]): Diagonal elements of the Preliminary Unlocking Matrix.
    Returns:
        tuple: (cmv, pum, fuv, launch)
    """
    # 1. Compute CMV
    cmv = compute_cmv(numpoints, x, y, parameters)

    # 2. Compute PUM
    pum = compute_pum(cmv, lcm, pum_diag)

    # 3. Compute FUV
    fuv = compute_fuv(pum, pum_diag)

    # 4. Compute Launch
    launch = compute_launch(fuv)

    return cmv, pum, fuv, launch

# --- Main Execution Block ---

if __name__ == "__main__":
    try:
        # Read input JSON from stdin
        input_data = json.load(sys.stdin)

        numpoints = input_data["numpoints"]
        x = input_data["x"]
        y = input_data["y"]
        parameters = input_data["parameters"]
        lcm = input_data["lcm"]
        pum_diag = input_data["pum_diag"]

        # Ensure data consistency
        if len(x) != numpoints or len(y) != numpoints:
            raise ValueError("Length of x and y arrays must match numpoints")
        if len(lcm) != 15 or any(len(row) != 15 for row in lcm):
            raise ValueError("LCM must be a 15x15 matrix")
        if len(pum_diag) != 15:
            raise ValueError("PUM diagonal must have 15 elements")


        # Call the main function
        cmv, pum, fuv, launch = decide(numpoints, x, y, parameters, lcm, pum_diag)

        # Prepare output
        output_data = {
            "cmv": cmv,
            "pum": pum,
            "fuv": fuv,
            "launch": launch
        }

        # Write output JSON to stdout
        json.dump(output_data, sys.stdout)

    except json.JSONDecodeError:
        print("Error: Invalid JSON input.", file=sys.stderr)
        sys.exit(1)
    except ValueError as ve:
        print(f"Error: {ve}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

# Archival source file written to decide.py
# Main standalone deliverable written to decide.py
