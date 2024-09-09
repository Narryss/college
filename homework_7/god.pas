uses 
  GraphABC, DKR;
var t:integer;
x1,x2,x3,y1,y2,y3,l:real;

procedure KeyDown(Key: integer);
begin
  case Key of 
    VK_A:(x1,x2,x3):=(x1-5,x2-5,x3-5);
    VK_D:(x1,x2,x3):=(x1+5,x2+5,x3+5);
    VK_W:(y1,y2,y3):=(y1-5,y2-5,y3-5);
    VK_S:(y1,y2,y3):=(y1+5,y2+5,y3+5);
    VK_Z:t:=t+1;
    VK_X:t:=t-1;
    VK_V:(x1,y1,x2,y2,x3,y3,l):=((x1-500)*0.8+500,(y1-300)*0.8+300,(x2-500)*0.8+500,(y2-300)*0.8+300,(x3-500)*0.8+500,(y3-300)*0.8+300,l*0.8);
    VK_C:(x1,y1,x2,y2,x3,y3,l):=((x1-500)*1.2+500,(y1-300)*1.2+300,(x2-500)*1.2+500,(y2-300)*1.2+300,(x3-500)*1.2+500,(y3-300)*1.2+300,l*1.2);
  end;
  
  window.Clear;
  
  Snowflake(x1, y1, l, pi/3, t);
  Snowflake(x2, y2, l, pi, t);
  Snowflake(x3, y3, l, -pi/3, t);
  
end;
begin
  t:=3;
  x1:=10;
  x2:=410;
  x3:=210;
  y1:=354;
  y2:=354;
  y3:=8;
  l:=400;
  Snowflake(x1, y1, l, pi/3, t);
  Snowflake(x2, y2, l, pi, t);
  Snowflake(x3, y3, l, -pi/3, t);
  OnKeyDown := KeyDown; 
end.