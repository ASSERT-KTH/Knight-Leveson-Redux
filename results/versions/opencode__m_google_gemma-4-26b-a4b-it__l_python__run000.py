import sys
import json
import math

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

def get_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def get_area(p1, p2, p3):
    return 0.5 * abs(p1[0]*(p2[1] - p3[1]) + p2[0]*(p3[1] - p1[1]) + p3[0]*(p1[1] - p2[1]))

def get_angle(p1, v, p2):
    # Vectors v->p1 and v->p2
    v1 = (p1[0] - v[0], p1[1] - v[1])
    v2 = (p2[0] - v[0], p2[1] - v[1])
    
    dot = v1[0]*v2[0] + v1[1]*v2[1]
    mag1 = math.sqrt(v1[0]**2 + v1[1]**2)
    mag2 = math.sqrt(v2[0]**2 + v2[1]**2)
    
    if mag1 == 0 or mag2 == 0:
        return None
    
    cos_theta = dot / (mag1 * mag2)
    # Clamp cos_theta to [-1, 1] to avoid math domain errors
    cos_theta = max(-1.0, min(1.0, cos_theta))
    return math.acos(cos_theta)

def get_quadrant(x, y):
    # Quadrant I: x > 0, y > 0
    # Quadrant II: x < 0, y > 0
    # Quadrant III: x < 0, y < 0
    # Quadrant IV: x > 0, y < 0
    # Special cases from spec:
    # (0,0) -> I
    # (-1,0) -> II
    # (0,-1) -> III
    # (0,1) -> I
    # (1,0) -> I
    
    if x >= 0 and y >= 0:
        return 1
    elif x < 0 and y >= 0:
        return 2
    elif x < 0 and y < 0:
        return 3
    elif x >= 0 and y < 0:
        return 4
    return 1 # Should not happen

def circle_contains(points, radius):
    if not points:
        return True
    # Smallest enclosing circle is a hard problem, but for 3 points it's either
    # the circumcircle or the circle defined by the diameter of the two furthest points.
    # Wait, the LICs only ever ask about 3 points for the circle check.
    
    if len(points) == 1:
        return True
    if len(points) == 2:
        dist = get_distance(points[0], points[1])
        return realcompare(dist, 2 * radius) != "GT"
    if len(points) == 3:
        # Check if any two points form a diameter that covers the third
        p1, p2, p3 = points
        d12 = get_distance(p1, p2)
        d13 = get_distance(p1, p3)
        d23 = get_distance(p2, p3)
        
        # Check if they can be contained in radius
        # For 3 points, the smallest enclosing circle radius R is:
        # If it's an obtuse or right triangle, R = half of longest side.
        # If it's acute, R = circumradius.
        
        sides = sorted([d12, d13, d23])
        a, b, c = sides[0], sides[1], sides[2]
        
        if realcompare(a**2 + b**2, c**2) != "LT": # obtuse or right
            r_min = c / 2.0
        else: # acute
            # R = (abc) / (4 * area)
            area = get_area(p1, p2, p3)
            if area == 0:
                r_min = c / 2.0
            else:
                r_min = (a * b * c) / (4.0 * area)
        
        return realcompare(r_min, radius) != "GT"
    return False

def line_distance(p1, p2, p):
    # Distance from point p to line passing through p1 and p2
    # If p1 == p2, return distance to p1
    if realcompare(p1[0], p2[0]) == "EQ" and realcompare(p1[1], p2[1]) == "EQ":
        return get_distance(p1, p)
    
    num = abs((p2[1] - p1[1]) * p[0] - (p2[0] - p1[0]) * p[1] + p2[0] * p1[1] - p2[1] * p1[0])
    den = get_distance(p1, p2)
    return num / den

def decide(numpoints, x, y, parameters, lcm, pum_diag):
    PI = 3.1415926535
    points = list(zip(x, y))
    cmv = [False] * 15
    
    # LIC 1
    for i in range(numpoints - 1):
        if realcompare(get_distance(points[i], points[i+1]), parameters['LENGTH1']) == "GT":
            cmv[0] = True
            break
            
    # LIC 2
    for i in range(numpoints - 2):
        if not circle_contains(points[i:i+3], parameters['RADIUS1']):
            cmv[1] = True
            break
            
    # LIC 3
    for i in range(numpoints - 2):
        angle = get_angle(points[i], points[i+1], points[i+2])
        if angle is not None:
            if realcompare(angle, PI - parameters['EPSILON']) == "LT" or \
               realcompare(angle, PI + parameters['EPSILON']) == "GT":
                cmv[2] = True
                break
                
    # LIC 4
    for i in range(numpoints - 2):
        if realcompare(get_area(points[i], points[i+1], points[i+2]), parameters['AREA1']) == "GT":
            cmv[3] = True
            break
            
    # LIC 5
    for i in range(numpoints - parameters['Q_PTS'] + 1):
        subset = points[i:i + parameters['Q_PTS']]
        quads = set(get_quadrant(p[0], p[1]) for p in subset)
        if len(quads) > parameters['QUADS']:
            cmv[4] = True
            break
            
    # LIC 6
    for i in range(numpoints - 1):
        if realcompare(points[i+1][0] - points[i][0], 0) == "LT":
            cmv[5] = True
            break
            
    # LIC 7
    if numpoints >= 3:
        for i in range(numpoints - parameters['N_PTS'] + 1):
            subset = points[i:i + parameters['N_PTS']]
            p_first = subset[0]
            p_last = subset[-1]
            for p in subset:
                if realcompare(line_distance(p_first, p_last, p), parameters['DIST']) == "GT":
                    cmv[6] = True
                    break
            if cmv[6]: break
            
    # LIC 8
    if numpoints >= 3:
        k = parameters['K_PTS']
        for i in range(numpoints - k - 1):
            if realcompare(get_distance(points[i], points[i + k + 1]), parameters['LENGTH1']) == "GT":
                cmv[7] = True
                break
                
    # LIC 9
    if numpoints >= 5:
        a = parameters['A_PTS']
        b = parameters['B_PTS']
        for i in range(numpoints - (a + b + 2)):
            p1 = points[i]
            p2 = points[i + a + 1]
            p3 = points[i + a + b + 2]
            if not circle_contains([p1, p2, p3], parameters['RADIUS1']):
                cmv[8] = True
                break
                
    # LIC 10
    if numpoints >= 5:
        a = parameters['C_PTS']
        b = parameters['D_PTS']
        for i in range(numpoints - (a + b + 2)):
            p1 = points[i]
            p2 = points[i + a + 1]
            p3 = points[i + a + b + 2]
            angle = get_angle(p1, p2, p3)
            if angle is not None:
                if realcompare(angle, PI - parameters['EPSILON']) == "LT" or \
                   realcompare(angle, PI + parameters['EPSILON']) == "GT":
                    cmv[9] = True
                    break
                    
    # LIC 11
    if numpoints >= 5:
        e = parameters['E_PTS']
        f = parameters['F_PTS']
        for i in range(numpoints - (e + f + 2)):
            p1 = points[i]
            p2 = points[i + e + 1]
            p3 = points[i + e + f + 2]
            if realcompare(get_area(p1, p2, p3), parameters['AREA1']) == "GT":
                cmv[10] = True
                break
                
    # LIC 12
    if numpoints >= 3:
        g = parameters['G_PTS']
        for i in range(numpoints - g - 1):
            j = i + g + 1
            if realcompare(points[j][0] - points[i][0], 0) == "LT":
                cmv[11] = True
                break
                
    # LIC 13
    if numpoints >= 3:
        k = parameters['K_PTS']
        cond_part1 = False
        cond_part2 = False
        for i in range(numpoints - k - 1):
            if realcompare(get_distance(points[i], points[i + k + 1]), parameters['LENGTH1']) == "GT":
                cond_part1 = True
            if realcompare(get_distance(points[i], points[i + k + 1]), parameters['LENGTH2']) == "LT":
                cond_part2 = True
            if cond_part1 and cond_part2:
                cmv[12] = True
                break
                
    # LIC 14
    if numpoints >= 5:
        a = parameters['A_PTS']
        b = parameters['B_PTS']
        cond_part1 = False
        cond_part2 = False
        for i in range(numpoints - (a + b + 2)):
            p1, p2, p3 = points[i], points[i + a + 1], points[i + a + b + 2]
            if not circle_contains([p1, p2, p3], parameters['RADIUS1']):
                cond_part1 = True
            if circle_contains([p1, p2, p3], parameters['RADIUS2']):
                cond_part2 = True
            if cond_part1 and cond_part2:
                cmv[13] = True
                break
                
    # LIC 15
    if numpoints >= 5:
        e = parameters['E_PTS']
        f = parameters['F_PTS']
        cond_part1 = False
        cond_part2 = False
        for i in range(numpoints - (e + f + 2)):
            p1, p2, p3 = points[i], points[i + e + 1], points[i + e + f + 2]
            if realcompare(get_area(p1, p2, p3), parameters['AREA1']) == "GT":
                cond_part1 = True
            if realcompare(get_area(p1, p2, p3), parameters['AREA2']) == "LT":
                cond_part2 = True
            if cond_part1 and cond_part2:
                cmv[14] = True
                break
                
    # PUM Generation
    pum = [[False for _ in range(15)] for _ in range(15)]
    for i in range(15):
        for j in range(15):
            if i == j:
                continue 
            
            connector = lcm[i][j]
            if connector == "NOTUSED":
                pum[i][j] = True
            elif connector == "ANDD":
                pum[i][j] = cmv[i] and cmv[j]
            elif connector == "ORR":
                pum[i][j] = cmv[i] or cmv[j]
                
    # Fill diagonal from pum_diag
    for i in range(15):
        pum[i][i] = pum_diag[i]
            
    # FUV Generation
    fuv = [False] * 15
    for i in range(15):
        # FUV[i] is true if PUM[i, i] is false OR all elements in PUM row i are true.
        if not pum[i][i]:
            fuv[i] = True
        else:
            all_true = True
            for j in range(15):
                if not pum[i][j]:
                    all_true = False
                    break
            if all_true:
                fuv[i] = True
                
    # Launch Decision
    launch = all(fuv)
    
    return cmv, pum, fuv, launch

if __name__ == "__main__":
    input_data = json.load(sys.stdin)
    
    numpoints = input_data['numpoints']
    x = input_data['x']
    y = input_data['y']
    parameters = input_data['parameters']
    lcm = input_data['lcm']
    pum_diag = input_data['pum_diag']
    
    cmv, pum, fuv, launch = decide(numpoints, x, y, parameters, lcm, pum_diag)
    
    output = {
        "cmv": cmv,
        "pum": pum,
        "fuv": fuv,
        "launch": launch
    }
    print(json.dumps(output))
