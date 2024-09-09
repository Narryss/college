Unit DKR;
uses GraphABC;

procedure Snowflake(x,y,l,u:real; t:integer);
procedure Snowflake2(var x,y:real; l,u:real; t:integer);

begin
    Snowflake(x,y,l,u,t);
    x := x + l*cos(u);
    y := y - l*sin(u);
end;

begin
    if t > 0 then
    begin
        l := l/3;
        Snowflake2(x, y, l, u, t-1);
        Snowflake2(x, y, l, u+pi/3, t-1);
        Snowflake2(x, y, l, u-pi/3, t-1);
        Snowflake2(x, y, l, u, t-1);
    end
    else
        Line(Round(x), Round(y), Round(x+cos(u)*l), Round(y-sin(u)*l))
end;
 
begin
  SetWindowSize(1000,600);
end.