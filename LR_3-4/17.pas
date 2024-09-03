var b,m:integer;
begin
b:=1;
readln(m);
repeat
if m <> 0 then begin b:= b*2; m:=m-1; end
until m<=0;
writeln(b);
end.