{ Minimal stub so `fpc lip_harness.pas` can compile without an agent. }
unit lipdecide;

{$mode objfpc}{$H+}

interface

uses
  globals;

procedure DECIDE;

implementation

procedure DECIDE;
var
  i, j: integer;
begin
  for i := 1 to 15 do
    CMV[i] := False;
  for i := 1 to 15 do
    FUV[i] := False;
  LAUNCH := False;
  for i := 1 to 15 do
    for j := 1 to 15 do
      if i <> j then
        PUM[i, j] := False;
end;

end.
