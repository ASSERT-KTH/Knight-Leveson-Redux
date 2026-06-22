
import json
import math
import sys

# Global constant PI
PI = 3.1415926535

# Comparison function from realcompare_reference.py
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

# Helper function to calculate distance between two points
def dist_sq(x1, y1, x2, y2):
    return (x2 - x1)**2 + (y2 - y1)**2

def dist(x1, y1, x2, y2):
    return math.sqrt(dist_sq(x1, y1, x2, y2))

# Helper function to calculate the area of a triangle
def triangle_area(x1, y1, x2, y2, x3, y3):
    return 0.5 * abs(x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2))

# Helper function to determine quadrant
def get_quadrant(x_coord, y_coord):
    if x_coord >= 0 and y_coord >= 0:
        return 1
    elif x_coord < 0 and y_coord >= 0:
        return 2
    elif x_coord < 0 and y_coord < 0:
        return 3
    else:  # x_coord >= 0 and y_coord < 0
        return 4

# LIC functions - will be filled in
def lic0(x, y, numpoints, parameters):
    return False

def lic1(x, y, numpoints, parameters):
    return False

def lic2(x, y, numpoints, parameters):
    return False

def lic3(x, y, numpoints, parameters):
    return False

def lic4(x, y, numpoints, parameters):
    return False

def lic5(x, y, numpoints, parameters):
    return False

def lic6(x, y, numpoints, parameters):
    return False

def lic7(x, y, numpoints, parameters):
    return False

def lic8(x, y, numpoints, parameters):
    return False

def lic9(x, y, numpoints, parameters):
    return False

def lic10(x, y, numpoints, parameters):
    return False

def lic11(x, y, numpoints, parameters):
    return False

def lic12(x, y, numpoints, parameters):
    return False

def lic13(x, y, numpoints, parameters):
    return False

def lic14(x, y, numpoints, parameters):
    return False

def lic(x_coords, y_coords, numpoints, parameters):
    """
    Evaluates all Launch Interceptor Conditions (LICs) and returns the Conditions Met Vector (CMV).
    """
    cmv = [False] * 15

    # LIC 0: There exists at least one set of two consecutive data points that are a distance greater than LENGTH1 apart.
    # Constraints: (0 <= LENGTH1)
    if numpoints >= 2:
        for i in range(numpoints - 1):
            distance = dist(x_coords[i], y_coords[i], x_coords[i+1], y_coords[i+1])
            if realcompare(distance, parameters["LENGTH1"]) == "GT":
                cmv[0] = True
                break

    # LIC 1: There exists at least one set of three consecutive data points that cannot all be contained within or on a circle of radius RADIUS1.
    # Constraints: (0 <= RADIUS1)
    if numpoints >= 3:
        for i in range(numpoints - 2):
            x1, y1 = x_coords[i], y_coords[i]
            x2, y2 = x_coords[i+1], y_coords[i+1]
            x3, y3 = x_coords[i+2], y_coords[i+2]

            # Case 1: Two points are identical
            if (realcompare(x1, x2) == "EQ" and realcompare(y1, y2) == "EQ") or 
               (realcompare(x1, x3) == "EQ" and realcompare(y1, y3) == "EQ") or 
               (realcompare(x2, x3) == "EQ" and realcompare(y2, y3) == "EQ"):
                # If two points are identical, the radius of the circumcircle is 0 (if collinear) or infinite (if not collinear).
                # We need to check if the third point is outside a circle of RADIUS1 centered at the two identical points
                # OR if the three points form a line and the radius1 is small enough.
                # A simpler approach: if all three points are identical, then radius is 0.
                # If two points are identical, then the minimum circumradius is half the distance to the third point.
                if (realcompare(x1, x2) == "EQ" and realcompare(y1, y2) == "EQ" and realcompare(x2, x3) == "EQ" and realcompare(y2, y3) == "EQ"):
                    # All three points are identical, radius is 0
                    if realcompare(parameters["RADIUS1"], 0.0) == "LT":
                        cmv[1] = True
                        break
                elif realcompare(x1, x2) == "EQ" and realcompare(y1, y2) == "EQ":
                    # P1 and P2 are identical
                    if realcompare(dist(x1, y1, x3, y3) / 2.0, parameters["RADIUS1"]) == "GT":
                        cmv[1] = True
                        break
                elif realcompare(x1, x3) == "EQ" and realcompare(y1, y3) == "EQ":
                    # P1 and P3 are identical
                    if realcompare(dist(x1, y1, x2, y2) / 2.0, parameters["RADIUS1"]) == "GT":
                        cmv[1] = True
                        break
                elif realcompare(x2, x3) == "EQ" and realcompare(y2, y3) == "EQ":
                    # P2 and P3 are identical
                    if realcompare(dist(x1, y1, x2, y2) / 2.0, parameters["RADIUS1"]) == "GT":
                        cmv[1] = True
                        break
            else:
                # Case 2: All three points are distinct
                a = dist(x1, y1, x2, y2)
                b = dist(x2, y2, x3, y3)
                c = dist(x3, y3, x1, y1)

                if realcompare(a, 0.0) == "EQ" or realcompare(b, 0.0) == "EQ" or realcompare(c, 0.0) == "EQ":
                    # Handle cases where points are distinct but collinear (or very close)
                    # If points are collinear, circumradius is infinite unless all points are identical (handled above)
                    # or two points are identical (also handled above)
                    # For distinct collinear points, they cannot be contained in a circle of finite radius.
                    if (realcompare(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2), 0.0) == "EQ"): # Collinear points
                         # If three distinct points are collinear, they cannot be contained in any finite circle, so any finite radius1 will fail
                        cmv[1] = True
                        break
                    else:
                        # Non-collinear, but numerically close to collinear. Let's calculate for circumradius.
                        # This might be tricky, use a robust check for collinearity if possible.
                        # For now, rely on triangle area for collinearity check
                        pass # proceed with general circumradius calculation
                
                area = triangle_area(x1, y1, x2, y2, x3, y3)
                if realcompare(area, 0.0) == "EQ":
                    # Points are collinear. If points are distinct and collinear, they cannot be contained in a finite circle.
                    cmv[1] = True
                    break

                circumradius = (a * b * c) / (4.0 * area)

                if realcompare(circumradius, parameters["RADIUS1"]) == "GT":
                    cmv[1] = True
                    break

    # LIC 2: There exists at least one set of three consecutive data points which form an angle such that:
    # - angle < (PI - EPSILON), or
    # - angle > (PI + EPSILON)
    # The second of the three consecutive points is always the vertex of the angle. If either the first point
    # or the last point (or both) coincides with the vertex, the angle is undefined and the LIC is not satisfied by those three points.
    # Constraints: (0 <= EPSILON < PI)
    if numpoints >= 3:
        for i in range(numpoints - 2):
            x1, y1 = x_coords[i], y_coords[i]
            x2, y2 = x_coords[i+1], y_coords[i+1] # Vertex
            x3, y3 = x_coords[i+2], y_coords[i+2]

            # Check for coincident points with the vertex
            if (realcompare(x1, x2) == "EQ" and realcompare(y1, y2) == "EQ") or 
               (realcompare(x3, x2) == "EQ" and realcompare(y3, y2) == "EQ"):
                continue # Angle is undefined, LIC not satisfied by these points

            # Vectors from vertex
            vec1_x, vec1_y = x1 - x2, y1 - y2
            vec2_x, vec2_y = x3 - x2, y3 - y2

            dot_product = vec1_x * vec2_x + vec1_y * vec2_y
            magnitude1 = math.sqrt(vec1_x**2 + vec1_y**2)
            magnitude2 = math.sqrt(vec2_x**2 + vec2_y**2)

            if realcompare(magnitude1, 0.0) == "EQ" or realcompare(magnitude2, 0.0) == "EQ":
                continue # Should not happen if non-coincident check is correct, but for safety

            # Calculate angle using dot product formula: cos(theta) = (A . B) / (|A| |B|)
            # Clamp value to avoid domain errors in acos due to floating point inaccuracies
            cos_angle = dot_product / (magnitude1 * magnitude2)
            cos_angle = max(-1.0, min(1.0, cos_angle)) # Clamp to [-1, 1]
            angle = math.acos(cos_angle)

            if realcompare(angle, PI - parameters["EPSILON"]) == "LT" or 
               realcompare(angle, PI + parameters["EPSILON"]) == "GT":
                cmv[2] = True
                break

    # LIC 3: There exists at least one set of three consecutive data points that are the vertices of a triangle with area greater than AREA1.
    # Constraints: (0 <= AREA1)
    if numpoints >= 3:
        for i in range(numpoints - 2):
            x1, y1 = x_coords[i], y_coords[i]
            x2, y2 = x_coords[i+1], y_coords[i+1]
            x3, y3 = x_coords[i+2], y_coords[i+2]

            area = triangle_area(x1, y1, x2, y2, x3, y3)
            if realcompare(area, parameters["AREA1"]) == "GT":
                cmv[3] = True
                break

    # LIC 4: There exists at least one set of Q_PTS consecutive data points that lie in more than QUADS quadrants.
    # Where there is ambiguity as to which quadrant contains a given point, priority of decision will be by quadrant number, i.e., I, II, III, IV.
    # For example, the data point (0,0) is in quadrant I, the point (-1,0) is in quadrant II, the point (0,-1) is in quadrant III,
    # the point (0,1) is in quadrant I, and the point (1,0) is in quadrant I.
    # Constraints: (2 <= Q_PTS <= NUMPOINTS), (1 <= QUADS <= 3)
    if numpoints >= parameters["Q_PTS"] and 2 <= parameters["Q_PTS"] <= numpoints and 1 <= parameters["QUADS"] <= 3:
        for i in range(numpoints - parameters["Q_PTS"] + 1):
            quadrants_found = set()
            for j in range(parameters["Q_PTS"]):
                quadrants_found.add(get_quadrant(x_coords[i+j], y_coords[i+j]))
            if len(quadrants_found) > parameters["QUADS"]:
                cmv[4] = True
                break

    # LIC 5: There exists at least one set of two consecutive data points, (X[i], Y[i]) and (X[j], Y[j]), such that X[j] - X[i] < 0 (where i = j - 1).
    if numpoints >= 2:
        for i in range(numpoints - 1):
            if realcompare(x_coords[i+1] - x_coords[i], 0.0) == "LT":
                cmv[5] = True
                break

    # LIC 6: There exists at least one set of N_PTS consecutive data points such that at least one of the points lies a distance greater than DIST from the line joining the first and last of these N_PTS points.
    # If the first and last points of these N_PTS are identical, then the calculated distance to compare with DIST will be the distance from the coincident point to all other points of the N_PTS consecutive points.
    # The condition is not met when NUMPOINTS < 3.
    # Constraints: (3 <= N_PTS <= NUMPOINTS), (0 <= DIST)
    if numpoints >= 3 and 3 <= parameters["N_PTS"] <= numpoints and realcompare(parameters["DIST"], 0.0) != "LT":
        for i in range(numpoints - parameters["N_PTS"] + 1):
            start_idx = i
            end_idx = i + parameters["N_PTS"] - 1

            x_start, y_start = x_coords[start_idx], y_coords[start_idx]
            x_end, y_end = x_coords[end_idx], y_coords[end_idx]

            found_lic = False
            if realcompare(x_start, x_end) == "EQ" and realcompare(y_start, y_end) == "EQ":
                # First and last points are identical
                for j in range(start_idx + 1, end_idx):
                    current_dist = dist(x_start, y_start, x_coords[j], y_coords[j])
                    if realcompare(current_dist, parameters["DIST"]) == "GT":
                        found_lic = True
                        break
            else:
                # First and last points are distinct
                # Line equation: Ax + By + C = 0
                A = y_end - y_start
                B = x_start - x_end
                C = x_end * y_start - y_end * x_start
                
                denominator = math.sqrt(A**2 + B**2)
                
                if realcompare(denominator, 0.0) == "EQ": # Should not happen if points are distinct
                    # If start and end points are distinct but denominator is 0, they are the same point (error in check logic above)
                    # Or, more likely, numerical instability. Treat as if they were identical.
                    for j in range(start_idx + 1, end_idx):
                        current_dist = dist(x_start, y_start, x_coords[j], y_coords[j])
                        if realcompare(current_dist, parameters["DIST"]) == "GT":
                            found_lic = True
                            break
                else:
                    for j in range(start_idx + 1, end_idx):
                        # Distance from a point (x0, y0) to a line Ax + By + C = 0
                        current_dist = abs(A * x_coords[j] + B * y_coords[j] + C) / denominator
                        if realcompare(current_dist, parameters["DIST"]) == "GT":
                            found_lic = True
                            break
            if found_lic:
                cmv[6] = True
                break

    # LIC 7: There exists at least one set of two data points separated by exactly K_PTS consecutive intervening points that are a distance greater than the length, LENGTH1, apart.
    # The condition is not met when NUMPOINTS < 3.
    # Constraints: (1 <= K_PTS <= NUMPOINTS - 2)
    if numpoints >= 3 and 1 <= parameters["K_PTS"] <= numpoints - 2:
        for i in range(numpoints - parameters["K_PTS"] - 1):
            j = i + parameters["K_PTS"] + 1
            distance = dist(x_coords[i], y_coords[i], x_coords[j], y_coords[j])
            if realcompare(distance, parameters["LENGTH1"]) == "GT":
                cmv[7] = True
                break
    
    # LIC 8: There exists at least one set of three data points separated by exactly A_PTS and B_PTS consecutive intervening points, respectively, that cannot be contained within or on a circle of radius RADIUS1.
    # The condition is not met when NUMPOINTS < 5.
    # Constraints: (1 <= A_PTS), (1 <= B_PTS), A_PTS + B_PTS <= NUMPOINTS - 3
    if numpoints >= 5 and 
        1 <= parameters["A_PTS"] and 
        1 <= parameters["B_PTS"] and 
        parameters["A_PTS"] + parameters["B_PTS"] <= numpoints - 3:
        for i in range(numpoints - (parameters["A_PTS"] + parameters["B_PTS"] + 2)):
            j = i + parameters["A_PTS"] + 1
            k = j + parameters["B_PTS"] + 1

            x1, y1 = x_coords[i], y_coords[i]
            x2, y2 = x_coords[j], y_coords[j]
            x3, y3 = x_coords[k], y_coords[k]

            # Re-using LIC1 logic for circumcircle check
            # Case 1: Two points are identical
            if (realcompare(x1, x2) == "EQ" and realcompare(y1, y2) == "EQ") or 
               (realcompare(x1, x3) == "EQ" and realcompare(y1, y3) == "EQ") or 
               (realcompare(x2, x3) == "EQ" and realcompare(y2, y3) == "EQ"):
                if (realcompare(x1, x2) == "EQ" and realcompare(y1, y2) == "EQ" and realcompare(x2, x3) == "EQ" and realcompare(y2, y3) == "EQ"):
                    if realcompare(parameters["RADIUS1"], 0.0) == "LT":
                        cmv[8] = True
                        break
                elif realcompare(x1, x2) == "EQ" and realcompare(y1, y2) == "EQ":
                    if realcompare(dist(x1, y1, x3, y3) / 2.0, parameters["RADIUS1"]) == "GT":
                        cmv[8] = True
                        break
                elif realcompare(x1, x3) == "EQ" and realcompare(y1, y3) == "EQ":
                    if realcompare(dist(x1, y1, x2, y2) / 2.0, parameters["RADIUS1"]) == "GT":
                        cmv[8] = True
                        break
                elif realcompare(x2, x3) == "EQ" and realcompare(y2, y3) == "EQ":
                    if realcompare(dist(x1, y1, x2, y2) / 2.0, parameters["RADIUS1"]) == "GT":
                        cmv[8] = True
                        break
            else:
                a = dist(x1, y1, x2, y2)
                b = dist(x2, y2, x3, y3)
                c = dist(x3, y3, x1, y1)

                area = triangle_area(x1, y1, x2, y2, x3, y3)
                if realcompare(area, 0.0) == "EQ":
                    cmv[8] = True
                    break

                circumradius = (a * b * c) / (4.0 * area)

                if realcompare(circumradius, parameters["RADIUS1"]) == "GT":
                    cmv[8] = True
                    break

    # LIC 9: There exists at least one set of three data points separated by exactly C_PTS and D_PTS consecutive intervening points, respectively, that form an angle such that:
    # - angle < (PI - EPSILON), or
    # - angle > (PI + EPSILON)
    # The second point of the set of three points is always the vertex of the angle. If either the first point
    # or the last point (or both) coincide with the vertex, the angle is undefined and the LIC is not satisfied by those three points.
    # The condition is not met when NUMPOINTS < 5.
    # Constraints: (1 <= C_PTS), (1 <= D_PTS), C_PTS + D_PTS <= NUMPOINTS - 3
    if numpoints >= 5 and 
        1 <= parameters["C_PTS"] and 
        1 <= parameters["D_PTS"] and 
        parameters["C_PTS"] + parameters["D_PTS"] <= numpoints - 3:
        for i in range(numpoints - (parameters["C_PTS"] + parameters["D_PTS"] + 2)):
            j = i + parameters["C_PTS"] + 1
            k = j + parameters["D_PTS"] + 1

            x1, y1 = x_coords[i], y_coords[i]
            x2, y2 = x_coords[j], y_coords[j] # Vertex
            x3, y3 = x_coords[k], y_coords[k]

            # Check for coincident points with the vertex
            if (realcompare(x1, x2) == "EQ" and realcompare(y1, y2) == "EQ") or 
               (realcompare(x3, x2) == "EQ" and realcompare(y3, y2) == "EQ"):
                continue # Angle is undefined, LIC not satisfied by these points

            vec1_x, vec1_y = x1 - x2, y1 - y2
            vec2_x, vec2_y = x3 - x2, y3 - y2

            dot_product = vec1_x * vec2_x + vec1_y * vec2_y
            magnitude1 = math.sqrt(vec1_x**2 + vec1_y**2)
            magnitude2 = math.sqrt(vec2_x**2 + vec2_y**2)

            if realcompare(magnitude1, 0.0) == "EQ" or realcompare(magnitude2, 0.0) == "EQ":
                continue

            cos_angle = dot_product / (magnitude1 * magnitude2)
            cos_angle = max(-1.0, min(1.0, cos_angle))
            angle = math.acos(cos_angle)

            if realcompare(angle, PI - parameters["EPSILON"]) == "LT" or 
               realcompare(angle, PI + parameters["EPSILON"]) == "GT":
                cmv[9] = True
                break

    # LIC 10: There exists at least one set of three data points separated by exactly E_PTS and F_PTS consecutive intervening points, respectively, that are the vertices of a triangle with area greater than AREA1.
    # The condition is not met when NUMPOINTS < 5.
    # Constraints: (1 <= E_PTS), (1 <= F_PTS), E_PTS + F_PTS <= NUMPOINTS - 3
    if numpoints >= 5 and 
        1 <= parameters["E_PTS"] and 
        1 <= parameters["F_PTS"] and 
        parameters["E_PTS"] + parameters["F_PTS"] <= numpoints - 3:
        for i in range(numpoints - (parameters["E_PTS"] + parameters["F_PTS"] + 2)):
            j = i + parameters["E_PTS"] + 1
            k = j + parameters["F_PTS"] + 1

            x1, y1 = x_coords[i], y_coords[i]
            x2, y2 = x_coords[j], y_coords[j]
            x3, y3 = x_coords[k], y_coords[k]

            area = triangle_area(x1, y1, x2, y2, x3, y3)
            if realcompare(area, parameters["AREA1"]) == "GT":
                cmv[10] = True
                break

    # LIC 11: There exists at least one set of two data points, (X[i], Y[i]) and (X[j], Y[j]), separated by exactly G_PTS consecutive intervening points, such that X[j] - X[i] < 0 (where i < j).
    # The condition is not met when NUMPOINTS < 3.
    # Constraints: (1 <= G_PTS <= NUMPOINTS - 2)
    if numpoints >= 3 and 1 <= parameters["G_PTS"] <= numpoints - 2:
        for i in range(numpoints - parameters["G_PTS"] - 1):
            j = i + parameters["G_PTS"] + 1
            if realcompare(x_coords[j] - x_coords[i], 0.0) == "LT":
                cmv[11] = True
                break

    # LIC 12: There exists at least one set of two data points, separated by exactly K_PTS consecutive intervening points, which are a distance greater than the length, LENGTH1, apart.
    # In addition, there exists at least one set of two data points (which can be the same or different from the two data points just mentioned), separated by exactly K_PTS consecutive intervening points, that are a distance less than the length, LENGTH2, apart.
    # Both parts must be true for the LIC to be true. The condition is not met when NUMPOINTS < 3.
    # Constraints: (0 <= LENGTH2)
    if numpoints >= 3 and 1 <= parameters["K_PTS"] <= numpoints - 2 and realcompare(parameters["LENGTH2"], 0.0) != "LT":
        condition1_met = False
        for i in range(numpoints - parameters["K_PTS"] - 1):
            j = i + parameters["K_PTS"] + 1
            distance = dist(x_coords[i], y_coords[i], x_coords[j], y_coords[j])
            if realcompare(distance, parameters["LENGTH1"]) == "GT":
                condition1_met = True
                break
        
        condition2_met = False
        for i in range(numpoints - parameters["K_PTS"] - 1):
            j = i + parameters["K_PTS"] + 1
            distance = dist(x_coords[i], y_coords[i], x_coords[j], y_coords[j])
            if realcompare(distance, parameters["LENGTH2"]) == "LT":
                condition2_met = True
                break
        
        if condition1_met and condition2_met:
            cmv[12] = True


    # LIC 13: There exists at least one set of three data points, separated by exactly A_PTS and B_PTS consecutive intervening points, respectively, that cannot be contained within or on a circle of radius RADIUS1.
    # In addition, there exists at least one set of three data points (which can be the same or different from the three data points just mentioned) separated by exactly A_PTS and B_PTS consecutive intervening points, respectively, that can be contained in or on a circle of radius RADIUS2.
    # Both parts must be true for the LIC to be true. The condition is not met when NUMPOINTS < 5.
    # Constraints: (0 <= RADIUS2)
    if numpoints >= 5 and 
        1 <= parameters["A_PTS"] and 
        1 <= parameters["B_PTS"] and 
        parameters["A_PTS"] + parameters["B_PTS"] <= numpoints - 3 and 
        realcompare(parameters["RADIUS2"], 0.0) != "LT":
        
        condition1_met = False
        for i in range(numpoints - (parameters["A_PTS"] + parameters["B_PTS"] + 2)):
            j = i + parameters["A_PTS"] + 1
            k = j + parameters["B_PTS"] + 1

            x1, y1 = x_coords[i], y_coords[i]
            x2, y2 = x_coords[j], y_coords[j]
            x3, y3 = x_coords[k], y_coords[k]

            circumradius = float('inf') # Default to infinite for collinear or identical points
            
            if (realcompare(x1, x2) == "EQ" and realcompare(y1, y2) == "EQ") or 
               (realcompare(x1, x3) == "EQ" and realcompare(y1, y3) == "EQ") or 
               (realcompare(x2, x3) == "EQ" and realcompare(y2, y3) == "EQ"):
                if (realcompare(x1, x2) == "EQ" and realcompare(y1, y2) == "EQ" and realcompare(x2, x3) == "EQ" and realcompare(y2, y3) == "EQ"):
                    circumradius = 0.0
                elif realcompare(x1, x2) == "EQ" and realcompare(y1, y2) == "EQ":
                    circumradius = dist(x1, y1, x3, y3) / 2.0
                elif realcompare(x1, x3) == "EQ" and realcompare(y1, y3) == "EQ":
                    circumradius = dist(x1, y1, x2, y2) / 2.0
                elif realcompare(x2, x3) == "EQ" and realcompare(y2, y3) == "EQ":
                    circumradius = dist(x1, y1, x2, y2) / 2.0
            else:
                a = dist(x1, y1, x2, y2)
                b = dist(x2, y2, x3, y3)
                c = dist(x3, y3, x1, y1)
                area = triangle_area(x1, y1, x2, y2, x3, y3)
                if realcompare(area, 0.0) != "EQ":
                    circumradius = (a * b * c) / (4.0 * area)

            if realcompare(circumradius, parameters["RADIUS1"]) == "GT":
                condition1_met = True
                break

        condition2_met = False
        for i in range(numpoints - (parameters["A_PTS"] + parameters["B_PTS"] + 2)):
            j = i + parameters["A_PTS"] + 1
            k = j + parameters["B_PTS"] + 1

            x1, y1 = x_coords[i], y_coords[i]
            x2, y2 = x_coords[j], y_coords[j]
            x3, y3 = x_coords[k], y_coords[k]
            
            circumradius = float('inf')
            
            if (realcompare(x1, x2) == "EQ" and realcompare(y1, y2) == "EQ") or 
               (realcompare(x1, x3) == "EQ" and realcompare(y1, y3) == "EQ") or 
               (realcompare(x2, x3) == "EQ" and realcompare(y2, y3) == "EQ"):
                if (realcompare(x1, x2) == "EQ" and realcompare(y1, y2) == "EQ" and realcompare(x2, x3) == "EQ" and realcompare(y2, y3) == "EQ"):
                    circumradius = 0.0
                elif realcompare(x1, x2) == "EQ" and realcompare(y1, y2) == "EQ":
                    circumradius = dist(x1, y1, x3, y3) / 2.0
                elif realcompare(x1, x3) == "EQ" and realcompare(y1, y3) == "EQ":
                    circumradius = dist(x1, y1, x2, y2) / 2.0
                elif realcompare(x2, x3) == "EQ" and realcompare(y2, y3) == "EQ":
                    circumradius = dist(x1, y1, x2, y2) / 2.0
            else:
                a = dist(x1, y1, x2, y2)
                b = dist(x2, y2, x3, y3)
                c = dist(x3, y3, x1, y1)
                area = triangle_area(x1, y1, x2, y2, x3, y3)
                if realcompare(area, 0.0) != "EQ":
                    circumradius = (a * b * c) / (4.0 * area)

            if realcompare(circumradius, parameters["RADIUS2"]) != "GT": # Check for "contained in or on"
                condition2_met = True
                break

        if condition1_met and condition2_met:
            cmv[13] = True

    # LIC 14: There exists at least one set of three data points, separated by exactly E_PTS and F_PTS consecutive intervening points, respectively, that are the vertices of a triangle with area greater than AREA1.
    # In addition, there exist three data points (which can be the same or different from the three data points just mentioned) separated by exactly E_PTS and F_PTS consecutive intervening points, respectively, that are the vertices of a triangle with area less than AREA2.
    # Both parts must be true for the LIC to be true. The condition is not met when NUMPOINTS < 5.
    # Constraints: (0 <= AREA2)
    if numpoints >= 5 and 
        1 <= parameters["E_PTS"] and 
        1 <= parameters["F_PTS"] and 
        parameters["E_PTS"] + parameters["F_PTS"] <= numpoints - 3 and 
        realcompare(parameters["AREA2"], 0.0) != "LT":
        
        condition1_met = False
        for i in range(numpoints - (parameters["E_PTS"] + parameters["F_PTS"] + 2)):
            j = i + parameters["E_PTS"] + 1
            k = j + parameters["F_PTS"] + 1

            x1, y1 = x_coords[i], y_coords[i]
            x2, y2 = x_coords[j], y_coords[j]
            x3, y3 = x_coords[k], y_coords[k]

            area = triangle_area(x1, y1, x2, y2, x3, y3)
            if realcompare(area, parameters["AREA1"]) == "GT":
                condition1_met = True
                break
        
        condition2_met = False
        for i in range(numpoints - (parameters["E_PTS"] + parameters["F_PTS"] + 2)):
            j = i + parameters["E_PTS"] + 1
            k = j + parameters["F_PTS"] + 1

            x1, y1 = x_coords[i], y_coords[i]
            x2, y2 = x_coords[j], y_coords[j]
            x3, y3 = x_coords[k], y_coords[k]

            area = triangle_area(x1, y1, x2, y2, x3, y3)
            if realcompare(area, parameters["AREA2"]) == "LT":
                condition2_met = True
                break
        
        if condition1_met and condition2_met:
            cmv[14] = True
            
    return cmv

def calculate_pum(cmv, lcm, pum_diag):
    pum = [[False for _ in range(15)] for _ in range(15)]
    for i in range(15):
        for j in range(15):
            if i == j:
                pum[i][j] = pum_diag[i]
            else:
                if lcm[i][j] == "NOTUSED":
                    pum[i][j] = True
                elif lcm[i][j] == "ANDD":
                    pum[i][j] = cmv[i] and cmv[j]
                elif lcm[i][j] == "ORR":
                    pum[i][j] = cmv[i] or cmv[j]
    return pum

def calculate_fuv(pum, pum_diag):
    fuv = [False] * 15
    for i in range(15):
        if not pum_diag[i]: # If PUM[i,i] is false, it should not hold back launch
            fuv[i] = True
        else:
            # Check if all elements in PUM row i are true
            all_true_in_row = True
            for j in range(15):
                if not pum[i][j]:
                    all_true_in_row = False
                    break
            fuv[i] = all_true_in_row
    return fuv

def decide(numpoints, x, y, parameters, lcm, pum_diag):
    cmv = lic(x, y, numpoints, parameters)
    pum = calculate_pum(cmv, lcm, pum_diag)
    fuv = calculate_fuv(pum, pum_diag)
    
    launch = all(fuv)

    return {
        "cmv": cmv,
        "pum": pum,
        "fuv": fuv,
        "launch": launch
    }

if __name__ == '__main__':
    input_data = json.load(sys.stdin)
    result = decide(
        input_data["numpoints"],
        input_data["x"],
        input_data["y"],
        input_data["parameters"],
        input_data["lcm"],
        input_data["pum_diag"]
    )
    json.dump(result, sys.stdout)
