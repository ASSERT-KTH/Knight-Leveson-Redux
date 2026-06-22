{ JSON-lines driver: stdin one case per line, stdout one result per line. }
program lip_harness;

{$mode objfpc}{$H+}

uses
  SysUtils, wire_json, globals, lipdecide;

var
  line: string;
  outstr: string;
begin
  while not EOF(Input) do
  begin
    ReadLn(line);
    line := Trim(line);
    if line = '' then
      continue;
    ApplyWireJson(line);
    DECIDE;
    outstr := BuildOutputLine;
    WriteLn(outstr);
    Flush(Output);
  end;
end.
