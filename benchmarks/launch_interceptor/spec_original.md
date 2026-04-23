# Launch Interceptor Program Specification

## Functional Requirements

All communication with software which calls your procedure is to be accomplished through the global variables and constant defined in this section.

### Constant

The value of the global constant `PI` is available to your procedure, representing the number of radians in 180 degrees.

### Input Variables

The values of the following global variables are available to your procedure:

| Variable                   | Description                                  |
| -------------------------- | -------------------------------------------- |
| `X`, `Y`                  | Parallel arrays containing the coordinates of data points |
| `NUMPOINTS`               | The number of planar data points             |
| `PARAMETERS`              | Record holding parameters for LICs           |
| `LCM`                     | Logical Connector Matrix                     |
| `PUM` (diagonal elements) | Preliminary Unlocking Matrix                 |

### Output Variables

The values of the following global variables are to be set by your procedure:

| Variable                       | Description                    |
| ------------------------------ | ------------------------------ |
| `PUM` (off-diagonal elements)  | Preliminary Unlocking Matrix   |
| `CMV`                          | Conditions Met Vector          |
| `FUV`                          | Final Unlocking Vector         |
| `LAUNCH`                       | Final launch/no launch decision |

### Global Declarations

The global declarations have been made as follows:

```pascal
const
  PI = 3.1415926535;

type
  POINTRANGE  = 1..100;
  LICRANGE    = 1..15;
  NPOINTS     = 2..100;
  NPTYPE      = 3..100;
  CONNECTORS  = (NOTUSED, ORR, ANDD);
  NUMQUADS    = 1..3;
  COORDINATE  = array[POINTRANGE] of real;
  CMATRIX     = array[LICRANGE, LICRANGE] of CONNECTORS;
  BMATRIX     = array[LICRANGE, LICRANGE] of boolean;
  VECTOR      = array[LICRANGE] of boolean;
  COMPTYPE    = (LT, EQ, GT);

var
  X          : COORDINATE;  {X coordinates of data points}
  Y          : COORDINATE;  {Y coordinates of data points}
  NUMPOINTS  : NPOINTS;     {Number of data points}
  PARAMETERS : record
    LENGTH1  : real;         {Length in LICs 1, 8, 13}
    RADIUS1  : real;         {Radius in LICs 2, 9, 14}
    EPSILON  : real;         {Deviation from PI in LICs 3, 10}
    AREA1    : real;         {Area in LICs 4, 11, 15}
    Q_PTS    : NPOINTS;      {No. of consecutive points in LIC 5}
    QUADS    : NUMQUADS;     {No. of quadrants in LIC 5}
    DIST     : real;         {Distance in LIC 7}
    N_PTS    : NPTYPE;       {No. of consecutive pts. in LIC 7}
    K_PTS    : POINTRANGE;   {No. of int. pts. in LICs 8, 13}
    A_PTS    : POINTRANGE;   {No. of int. pts. in LICs 9, 14}
    B_PTS    : POINTRANGE;   {No. of int. pts. in LICs 9, 14}
    C_PTS    : POINTRANGE;   {No. of int. pts. in LIC 10}
    D_PTS    : POINTRANGE;   {No. of int. pts. in LIC 10}
    E_PTS    : POINTRANGE;   {No. of int. pts. in LICs 11, 15}
    F_PTS    : POINTRANGE;   {No. of int. pts. in LICs 11, 15}
    G_PTS    : POINTRANGE;   {No. of int. pts. in LIC 12}
    LENGTH2  : real;         {Maximum length in LIC 13}
    RADIUS2  : real;         {Maximum radius in LIC 14}
    AREA2    : real;         {Maximum area in LIC 15}
  end;
  LCM     : CMATRIX;     {Logical Connector Matrix}
  PUM     : BMATRIX;     {Preliminary Unlocking Matrix}
  CMV     : VECTOR;      {Conditions Met Vector}
  FUV     : VECTOR;      {Final Unlocking Vector}
  LAUNCH  : boolean;     {Decision: Launch or No Launch}

function REALCOMPARE(A, B : real) : COMPTYPE;
  {compares real numbers - see Nonfunctional Requirements}
```

### Required Computations

It can be assumed that all input data and parameters that are measured in some form of units use the same, consistent units. For example, all lengths are measured in the same units that are used to define the planar space from which the input data comes. Therefore, no unit conversion is necessary.

Given the parameter values in the global record `PARAMETERS`, the procedure `DECIDE` must evaluate each of the Launch Interceptor Conditions (LICs) described below for the set of `NUMPOINTS` points:

```
(X[1], Y[1]), ..., (X[NUMPOINTS], Y[NUMPOINTS])
```

where 2 <= `NUMPOINTS` <= 100.

The Conditions Met Vector (CMV) should be set according to the results of these calculations, i.e., the global array element `CMV[i]` should be set to true if and only if the i-th LIC is met.

#### Launch Interceptor Conditions (LICs)

**LIC 1:** There exists at least one set of two consecutive data points that are a distance greater than the length, `LENGTH1`, apart.

> Constraints: (0 <= LENGTH1)

**LIC 2:** There exists at least one set of three consecutive data points that cannot all be contained within or on a circle of radius `RADIUS1`.

> Constraints: (0 <= RADIUS1)

**LIC 3:** There exists at least one set of three consecutive data points which form an angle such that:

- angle < (PI - EPSILON), or
- angle > (PI + EPSILON)

The second of the three consecutive points is always the vertex of the angle. If either the first point or the last point (or both) coincides with the vertex, the angle is undefined and the LIC is not satisfied by those three points.

> Constraints: (0 <= EPSILON < PI)

**LIC 4:** There exists at least one set of three consecutive data points that are the vertices of a triangle with area greater than `AREA1`.

> Constraints: (0 <= AREA1)

**LIC 5:** There exists at least one set of `Q_PTS` consecutive data points that lie in more than `QUADS` quadrants. Where there is ambiguity as to which quadrant contains a given point, priority of decision will be by quadrant number, i.e., I, II, III, IV. For example, the data point (0,0) is in quadrant I, the point (-1,0) is in quadrant II, the point (0,-1) is in quadrant III, the point (0,1) is in quadrant I, and the point (1,0) is in quadrant I.

> Constraints: (2 <= Q_PTS <= NUMPOINTS), (1 <= QUADS <= 3)

**LIC 6:** There exists at least one set of two consecutive data points, (X[i], Y[i]) and (X[j], Y[j]), such that X[j] - X[i] < 0 (where i = j - 1).

**LIC 7:** There exists at least one set of `N_PTS` consecutive data points such that at least one of the points lies a distance greater than `DIST` from the line joining the first and last of these `N_PTS` points. If the first and last points of these `N_PTS` are identical, then the calculated distance to compare with `DIST` will be the distance from the coincident point to all other points of the `N_PTS` consecutive points. The condition is not met when NUMPOINTS < 3.

> Constraints: (3 <= N_PTS <= NUMPOINTS), (0 <= DIST)

**LIC 8:** There exists at least one set of two data points separated by exactly `K_PTS` consecutive intervening points that are a distance greater than the length, `LENGTH1`, apart. The condition is not met when NUMPOINTS < 3.

> Constraints: (1 <= K_PTS <= NUMPOINTS - 2)

**LIC 9:** There exists at least one set of three data points separated by exactly `A_PTS` and `B_PTS` consecutive intervening points, respectively, that cannot be contained within or on a circle of radius `RADIUS1`. The condition is not met when NUMPOINTS < 5.

> Constraints: (1 <= A_PTS), (1 <= B_PTS), A_PTS + B_PTS <= NUMPOINTS - 3

**LIC 10:** There exists at least one set of three data points separated by exactly `C_PTS` and `D_PTS` consecutive intervening points, respectively, that form an angle such that:

- angle < (PI - EPSILON), or
- angle > (PI + EPSILON)

The second point of the set of three points is always the vertex of the angle. If either the first point or the last point (or both) coincide with the vertex, the angle is undefined and the LIC is not satisfied by those three points. The condition is not met when NUMPOINTS < 5.

> Constraints: (1 <= C_PTS), (1 <= D_PTS), C_PTS + D_PTS <= NUMPOINTS - 3

**LIC 11:** There exists at least one set of three data points separated by exactly `E_PTS` and `F_PTS` consecutive intervening points, respectively, that are the vertices of a triangle with area greater than `AREA1`. The condition is not met when NUMPOINTS < 5.

> Constraints: (1 <= E_PTS), (1 <= F_PTS), E_PTS + F_PTS <= NUMPOINTS - 3

**LIC 12:** There exists at least one set of two data points, (X[i], Y[i]) and (X[j], Y[j]), separated by exactly `G_PTS` consecutive intervening points, such that X[j] - X[i] < 0 (where i < j). The condition is not met when NUMPOINTS < 3.

> Constraints: (1 <= G_PTS <= NUMPOINTS - 2)

**LIC 13:** There exists at least one set of two data points, separated by exactly `K_PTS` consecutive intervening points, which are a distance greater than the length, `LENGTH1`, apart. In addition, there exists at least one set of two data points (which can be the same or different from the two data points just mentioned), separated by exactly `K_PTS` consecutive intervening points, that are a distance less than the length, `LENGTH2`, apart. Both parts must be true for the LIC to be true. The condition is not met when NUMPOINTS < 3.

> Constraints: (0 <= LENGTH2)

**LIC 14:** There exists at least one set of three data points, separated by exactly `A_PTS` and `B_PTS` consecutive intervening points, respectively, that cannot be contained within or on a circle of radius `RADIUS1`. In addition, there exists at least one set of three data points (which can be the same or different from the three data points just mentioned) separated by exactly `A_PTS` and `B_PTS` consecutive intervening points, respectively, that can be contained in or on a circle of radius `RADIUS2`. Both parts must be true for the LIC to be true. The condition is not met when NUMPOINTS < 5.

> Constraints: (0 <= RADIUS2)

**LIC 15:** There exists at least one set of three data points, separated by exactly `E_PTS` and `F_PTS` consecutive intervening points, respectively, that are the vertices of a triangle with area greater than `AREA1`. In addition, there exist three data points (which can be the same or different from the three data points just mentioned) separated by exactly `E_PTS` and `F_PTS` consecutive intervening points, respectively, that are the vertices of a triangle with area less than `AREA2`. Both parts must be true for the LIC to be true. The condition is not met when NUMPOINTS < 5.

> Constraints: (0 <= AREA2)

#### Combining LICs: The Preliminary Unlocking Matrix (PUM)

The Conditions Met Vector (CMV) can now be used in conjunction with the Logical Connector Matrix (LCM) to form the off-diagonal elements of the Preliminary Unlocking Matrix (PUM). The entries in the LCM represent the logical connectors to be used between pairs of LICs to determine the corresponding entry in the PUM, i.e., `LCM[i, j]` represents the Boolean operator to be applied to `CMV[i]` and `CMV[j]`. `PUM[i, j]` is set according to the result of this operation:

- If `LCM[i, j]` is **NOTUSED**, then `PUM[i, j]` should be set to **true**.
- If `LCM[i, j]` is **ANDD**, `PUM[i, j]` should be set to true only if (`CMV[i]` AND `CMV[j]`) is true.
- If `LCM[i, j]` is **ORR**, `PUM[i, j]` should be set to true if (`CMV[i]` OR `CMV[j]`) is true.

Note that the LCM is symmetric, i.e., `LCM[i, j]` = `LCM[j, i]` for all i and j.

**Example:**

Assume that the given Logical Connector Matrix is as shown below:

| LIC | 1       | 2       | 3       | 4       | 5       | ... | 15      |
| --- | ------- | ------- | ------- | ------- | ------- | --- | ------- |
| 1   | —       | ANDD    | ORR     | ANDD    | NOTUSED | ... | NOTUSED |
| 2   | ANDD    | —       | ORR     | ORR     | NOTUSED | ... | NOTUSED |
| 3   | ORR     | ORR     | —       | ANDD    | NOTUSED | ... | NOTUSED |
| 4   | ANDD    | ORR     | ANDD    | —       | NOTUSED | ... | NOTUSED |
| 5   | NOTUSED | NOTUSED | NOTUSED | NOTUSED | —       | ... | NOTUSED |
| ... | ...     | ...     | ...     | ...     | ...     | ... | ...     |
| 15  | NOTUSED | NOTUSED | NOTUSED | NOTUSED | NOTUSED | ... | —       |

Also assume that the entries in the CMV have been computed as described, giving the following results:

| Condition | Value |
| --------- | ----- |
| 1         | false |
| 2         | true  |
| 3         | true  |
| 4         | true  |
| 5         | false |
| ...       | ...   |
| 15        | false |

The following PUM is generated:

| LIC | 1     | 2     | 3    | 4     | 5    | ... | 15   |
| --- | ----- | ----- | ---- | ----- | ---- | --- | ---- |
| 1   | \*    | false | true | false | true | ... | true |
| 2   | false | \*    | true | true  | true | ... | true |
| 3   | true  | true  | \*   | true  | true | ... | true |
| 4   | false | true  | true | \*    | true | ... | true |
| 5   | true  | true  | true | true  | \*   | ... | true |
| ... | ...   | ...   | ...  | ...   | ...  | ... | ...  |
| 15  | true  | true  | true | true  | true | ... | \*   |

Explanation of selected PUM entries:

1. `PUM[1, 2]` is false because `LCM[1, 2]` is ANDD, and at least one of `CMV[1]` and `CMV[2]` is false.
2. `PUM[1, 3]` is true because `LCM[1, 3]` is ORR, and at least one of `CMV[1]` and `CMV[3]` is true.
3. `PUM[2, 3]` is true because `LCM[2, 3]` is ORR, and at least one of `CMV[2]` and `CMV[3]` is true.
4. `PUM[3, 4]` is true because `LCM[3, 4]` is ANDD, and both `CMV[3]` and `CMV[4]` are true.
5. `PUM[1, 5]` is true because `LCM[1, 5]` is NOTUSED.

#### Final Unlocking Vector (FUV)

The Final Unlocking Vector (FUV) is generated from the Preliminary Unlocking Matrix. The input diagonal elements of the PUM indicate whether the corresponding LIC is to be considered as a factor in signaling interceptor launch. `FUV[i]` should be set to true if `PUM[i, i]` is false (indicating that the associated LIC should not hold back launch) or if all elements in PUM row i are true.

**Example:**

Assume that the PUM now appears as follows:

| LIC | 1     | 2     | 3    | 4     | 5     | ... | 15    |
| --- | ----- | ----- | ---- | ----- | ----- | --- | ----- |
| 1   | true  | false | true | false | true  | ... | true  |
| 2   | false | false | true | true  | true  | ... | true  |
| 3   | true  | true  | true | true  | true  | ... | true  |
| 4   | false | true  | true | false | true  | ... | true  |
| 5   | true  | true  | true | true  | false | ... | true  |
| ... | ...   | ...   | ...  | ...   | ...   | ... | ...   |
| 15  | true  | true  | true | true  | true  | ... | false |

The FUV generated is as follows:

| Condition | Value |
| --------- | ----- |
| 1         | false |
| 2         | true  |
| 3         | true  |
| 4         | true  |
| 5         | true  |
| ...       | ...   |
| 15        | true  |

Explanation of selected FUV entries:

1. `FUV[1]` is false because `PUM[1, 1]` is true, but `PUM[1, 2]` and `PUM[1, 4]` are false.
2. `FUV[2]` is true because `PUM[2, 2]` is false.
3. `FUV[3]` is true because `PUM[3, i]` is true for all i, 1 <= i <= 15.

#### Launch Decision

The final launch/no launch decision is based on the FUV. The decision to launch requires that all elements in the FUV be true, i.e., `LAUNCH` should be set to true if and only if `FUV[i]` is true for all i, 1 <= i <= 15. For the example, `LAUNCH` is false because `FUV[1]` is false.

## Software Support

The only software facilities you may use to prepare are:

1. GCC compiler

## Nonfunctional Requirements

1. The functional requirements are to be implemented by a parameterless Pascal procedure named `DECIDE`. It will perform no input or output, because the calling program will provide input data through global variables. Likewise, `DECIDE` should store its results in global variables.

2. Whenever real numbers must be compared within the procedure `DECIDE`, that comparison should be made with a fixed amount of precision. The program which calls `DECIDE` will provide a function called `REALCOMPARE`. (See function header in declarations.) This function compares two real numbers, A and B, with respect to the six most significant digits. `REALCOMPARE` returns `LT` if A < B, `EQ` if A = B, or `GT` if A > B. `DECIDE` should call this function for all comparisons of real numbers.

3. Information contained in the global variables when the subroutine is called will remain valid throughout the execution of the procedure. There are no feedback or time series effects during a call to `DECIDE`, or from multiple calls to `DECIDE`.

4. Do not include input error checking. Assume that the calling program ensures inputs are complete and within the specified range.

5. No double precision or complex variables should be used.

6. There are no constraints on memory space or execution time, but efficient, well-structured code with descriptive comments is preferred.

7. In writing the subroutine, do not use any language-dependent software tools other than the Hull V Pascal compiler.

## Glossary

**angle**
: An angle is formed by two rays which share a common endpoint called a vertex. If one ray is rotated about the vertex until it coincides with the other ray, the amount of rotation required is the measure of the angle. Three points can be used to determine an angle by drawing a ray from the second point through the first point and another ray from the second point through the third point. Note that different angles are described according to whether the ray is rotated clockwise or counterclockwise. Either can be used in this problem because of the way the LICs are defined.

**CMV** (Conditions Met Vector)
: The CMV is a Boolean vector whose elements have a one-to-one correspondence with the launch interceptor conditions. If the radar tracking data satisfy a certain LIC, then the corresponding element of the CMV is to be set to true.

**consecutive**
: Two points are consecutive if they are adjacent in the input data vectors X and Y. Thus (X[i], Y[i]) and (X[i + 1], Y[i + 1]) are adjacent.

**diagonal element**
: Consider a matrix M, with n rows and n columns. The diagonal elements of the matrix are M[i, i], where i = 1, ..., n.

**FUV** (Final Unlocking Vector)
: The FUV is a Boolean vector which is the basis for deciding whether to launch an interceptor. If all elements of the FUV are true, a launch should occur.

**LCM** (Logical Connector Matrix)
: The LCM describes how individual LICs should be logically combined. For example, the value of LCM[i, j] indicates whether LIC #i should combine with LIC #j by the logical AND, OR, or not at all.

**LIC** (Launch Interceptor Condition)
: If radar tracking data exhibit a certain combination of characteristics, then an interceptor should be launched. Each characteristic is an LIC.

**matrix**
: For purposes of this problem, a matrix can be considered to be a two-dimensional array.

**off-diagonal element**
: An off-diagonal element of a matrix is any element which is not a diagonal element.

**planar data points**
: Planar data points are points that are all located within the same plane.

**PUM** (Preliminary Unlocking Matrix)
: Every element of the Boolean PUM corresponds to an element of the LCM. If the logical connection dictated by the LCM element gives the value "true," the corresponding PUM element is to be set to true.

**quadrant**
: The x and y axes of the Cartesian coordinate system divide a plane into four areas called quadrants. They are labeled I, II, III, IV, beginning with the area where both coordinates are positive and numbering counterclockwise.

**radius**
: The length of the radius of a circle is the distance from the center of the circle to any point on the circle's circumference.

**ray**
: A ray is a straight line that extends from a point.

**vector**
: For purposes of this problem, a vector may be considered to be a one-dimensional array.

**vertex**
: When two rays originate from a common point to form an angle, the point of their origination is called the vertex of that angle.
