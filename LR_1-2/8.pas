﻿var x1,x2,a1,a2:integer;
begin
  x1:=random(900)+100;
  writeln('Трёхзначное число = ',x1);
  x2:=random(9000)+1000;
  writeln('Четырёхзначное число = ',x2);
  a1:=x1 div 100;
  a2:=x2 div 1000;
  writeln('Первая цифра трёхзначного числа = ',a1,'. Первая цифра четырёхзначного числа = ',a2);
end.