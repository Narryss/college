﻿var x1,x2,x3:integer;
begin
write('Введите три числа ');
  read(x1,x2,x3);
  if x1<x2 then if x1<x3 then write(x1) else write(x3) else if x2<x3 then write(x2) else write(x3);
  write(' - это наименьшее число');
    end.
