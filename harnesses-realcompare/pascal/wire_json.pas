{ Minimal JSON parse/emit for the LIP harness wire format (RTL only; no fpjson). }
unit wire_json;

{$mode objfpc}{$H+}

interface

uses
  SysUtils, globals;

procedure ApplyWireJson(const line: string);
function BuildOutputLine: string;

implementation

var
  S: string;
  P: Integer;

procedure SkipWs;
begin
  while (P <= Length(S)) and (S[P] in [#9, #10, #13, ' ']) do
    Inc(P);
end;

procedure Expect(const c: Char);
begin
  SkipWs;
  if (P > Length(S)) or (S[P] <> c) then
    raise Exception.Create('JSON: expected ' + c);
  Inc(P);
end;

function Peek: Char;
begin
  SkipWs;
  if P <= Length(S) then
    Result := S[P]
  else
    Result := #0;
end;

function ParseNumber: double;
var
  startp: integer;
  code: integer;
  t: string;
begin
  SkipWs;
  startp := P;
  if (P <= Length(S)) and (S[P] = '-') then
    Inc(P);
  while (P <= Length(S)) and (S[P] in ['0'..'9']) do
    Inc(P);
  if (P <= Length(S)) and (S[P] = '.') then
  begin
    Inc(P);
    while (P <= Length(S)) and (S[P] in ['0'..'9']) do
      Inc(P);
  end;
  if (P <= Length(S)) and (S[P] in ['e', 'E']) then
  begin
    Inc(P);
    if (P <= Length(S)) and (S[P] in ['+', '-']) then
      Inc(P);
    while (P <= Length(S)) and (S[P] in ['0'..'9']) do
      Inc(P);
  end;
  t := Copy(S, startp, P - startp);
  Val(t, Result, code);
  if code <> 0 then
    raise Exception.Create('JSON: bad number ' + t);
end;

function ParseInt: integer;
begin
  Result := Trunc(ParseNumber);
end;

function ParseString: string;
var
  c: Char;
begin
  Expect('"');
  Result := '';
  while (P <= Length(S)) and (S[P] <> '"') do
  begin
    if S[P] = '\' then
    begin
      Inc(P);
      if P > Length(S) then
        Break;
      c := S[P];
      case c of
        'n': Result := Result + #10;
        'r': Result := Result + #13;
        't': Result := Result + #9;
        else
          Result := Result + c;
      end;
      Inc(P);
    end
    else
    begin
      Result := Result + S[P];
      Inc(P);
    end;
  end;
  Expect('"');
end;

function ParseBool: boolean;
begin
  SkipWs;
  if Copy(S, P, 4) = 'true' then
  begin
    Inc(P, 4);
    Exit(True);
  end;
  if Copy(S, P, 5) = 'false' then
  begin
    Inc(P, 5);
    Exit(False);
  end;
  raise Exception.Create('JSON: expected bool');
end;

procedure ParseKey(const want: string);
begin
  Expect('"');
  if Copy(S, P, Length(want)) <> want then
    raise Exception.Create('JSON: bad key');
  Inc(P, Length(want));
  Expect('"');
  Expect(':');
end;

procedure ParseParametersBlock;
var
  first: boolean;
  k: string;
begin
  Expect('{');
  first := True;
  while Peek <> '}' do
  begin
    if not first then
      Expect(',');
    first := False;
    k := ParseString;
    Expect(':');
    if k = 'LENGTH1' then
      PARAMETERS.LENGTH1 := ParseNumber
    else if k = 'RADIUS1' then
      PARAMETERS.RADIUS1 := ParseNumber
    else if k = 'EPSILON' then
      PARAMETERS.EPSILON := ParseNumber
    else if k = 'AREA1' then
      PARAMETERS.AREA1 := ParseNumber
    else if k = 'Q_PTS' then
      PARAMETERS.Q_PTS := ParseInt
    else if k = 'QUADS' then
      PARAMETERS.QUADS := ParseInt
    else if k = 'DIST' then
      PARAMETERS.DIST := ParseNumber
    else if k = 'N_PTS' then
      PARAMETERS.N_PTS := ParseInt
    else if k = 'K_PTS' then
      PARAMETERS.K_PTS := ParseInt
    else if k = 'A_PTS' then
      PARAMETERS.A_PTS := ParseInt
    else if k = 'B_PTS' then
      PARAMETERS.B_PTS := ParseInt
    else if k = 'C_PTS' then
      PARAMETERS.C_PTS := ParseInt
    else if k = 'D_PTS' then
      PARAMETERS.D_PTS := ParseInt
    else if k = 'E_PTS' then
      PARAMETERS.E_PTS := ParseInt
    else if k = 'F_PTS' then
      PARAMETERS.F_PTS := ParseInt
    else if k = 'G_PTS' then
      PARAMETERS.G_PTS := ParseInt
    else if k = 'LENGTH2' then
      PARAMETERS.LENGTH2 := ParseNumber
    else if k = 'RADIUS2' then
      PARAMETERS.RADIUS2 := ParseNumber
    else if k = 'AREA2' then
      PARAMETERS.AREA2 := ParseNumber
    else
      raise Exception.Create('unknown parameter key: ' + k);
  end;
  Expect('}');
end;

function ConnFromStr(const t: string): CONNECTORS;
var
  u: string;
begin
  u := UpperCase(Trim(t));
  if u = 'NOTUSED' then
    ConnFromStr := NOTUSED
  else if u = 'ORR' then
    ConnFromStr := ORR
  else if u = 'ANDD' then
    ConnFromStr := ANDD
  else
    raise Exception.Create('invalid connector: ' + t);
end;

procedure ParseInputIntoGlobals;
var
  np, i, j: integer;
begin
  Expect('{');
  ParseKey('numpoints');
  np := ParseInt;
  if (np < 2) or (np > 100) then
    raise Exception.Create('bad numpoints');
  NUMPOINTS := np;
  Expect(',');
  ParseKey('x');
  Expect('[');
  for i := 0 to np - 1 do
  begin
    if i > 0 then
      Expect(',');
    X[i + 1] := ParseNumber;
  end;
  Expect(']');
  Expect(',');
  ParseKey('y');
  Expect('[');
  for i := 0 to np - 1 do
  begin
    if i > 0 then
      Expect(',');
    Y[i + 1] := ParseNumber;
  end;
  Expect(']');
  Expect(',');
  ParseKey('parameters');
  ParseParametersBlock;
  Expect(',');
  ParseKey('lcm');
  Expect('[');
  for i := 0 to 14 do
  begin
    if i > 0 then
      Expect(',');
    Expect('[');
    for j := 0 to 14 do
    begin
      if j > 0 then
        Expect(',');
      LCM[i + 1, j + 1] := ConnFromStr(ParseString);
    end;
    Expect(']');
  end;
  Expect(']');
  Expect(',');
  ParseKey('pum_diag');
  Expect('[');
  for i := 0 to 14 do
  begin
    if i > 0 then
      Expect(',');
    PUM[i + 1, i + 1] := ParseBool;
  end;
  Expect(']');
  Expect('}');
  SkipWs;
  if P <= Length(S) then
    raise Exception.Create('JSON: trailing junk');
end;

procedure ApplyWireJson(const line: string);
begin
  S := line;
  P := 1;
  ParseInputIntoGlobals;
end;

function BoolStr(b: boolean): string;
begin
  if b then
    Result := 'true'
  else
    Result := 'false';
end;

function BuildOutputLine: string;
var
  i, j: integer;
  t: string;
begin
  t := '{"cmv":[';
  for i := 1 to 15 do
  begin
    if i > 1 then
      t := t + ',';
    t := t + BoolStr(CMV[i]);
  end;
  t := t + '],"pum":[';
  for i := 1 to 15 do
  begin
    if i > 1 then
      t := t + ',';
    t := t + '[';
    for j := 1 to 15 do
    begin
      if j > 1 then
        t := t + ',';
      t := t + BoolStr(PUM[i, j]);
    end;
    t := t + ']';
  end;
  t := t + '],"fuv":[';
  for i := 1 to 15 do
  begin
    if i > 1 then
      t := t + ',';
    t := t + BoolStr(FUV[i]);
  end;
  t := t + '],"launch":' + BoolStr(LAUNCH) + '}';
  Result := t;
end;

end.
