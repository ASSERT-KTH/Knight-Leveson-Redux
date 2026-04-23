{ Shared globals for Launch Interceptor (K&L spec). }
unit globals;

{$mode objfpc}{$H+}

interface

const
  PI = 3.1415926535;

type
  POINTRANGE = 1..100;
  LICRANGE = 1..15;
  NPOINTS = 2..100;
  NPTYPE = 3..100;
  CONNECTORS = (NOTUSED, ORR, ANDD);
  NUMQUADS = 1..3;
  COORDINATE = array[POINTRANGE] of real;
  CMATRIX = array[LICRANGE, LICRANGE] of CONNECTORS;
  BMATRIX = array[LICRANGE, LICRANGE] of boolean;
  VECTOR = array[LICRANGE] of boolean;
  COMPTYPE = (LT, EQ, GT);

var
  X: COORDINATE;
  Y: COORDINATE;
  NUMPOINTS: NPOINTS;
  PARAMETERS: record
    LENGTH1: real;
    RADIUS1: real;
    EPSILON: real;
    AREA1: real;
    Q_PTS: NPOINTS;
    QUADS: NUMQUADS;
    DIST: real;
    N_PTS: NPTYPE;
    K_PTS: POINTRANGE;
    A_PTS: POINTRANGE;
    B_PTS: POINTRANGE;
    C_PTS: POINTRANGE;
    D_PTS: POINTRANGE;
    E_PTS: POINTRANGE;
    F_PTS: POINTRANGE;
    G_PTS: POINTRANGE;
    LENGTH2: real;
    RADIUS2: real;
    AREA2: real;
  end;
  LCM: CMATRIX;
  PUM: BMATRIX;
  CMV: VECTOR;
  FUV: VECTOR;
  LAUNCH: boolean;

implementation

end.
