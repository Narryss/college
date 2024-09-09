unit Unit1;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, Forms, Controls, Graphics, Dialogs, StdCtrls, Buttons;

type

  { TForm1 }

  TForm1 = class(TForm)
    ButtonUmnoz: TButton;
    ButtonMinus: TButton;
    ButtonPlus: TButton;
    Button5: TButton;
    Button4: TButton;
    Button1: TButton;
    Button6: TButton;
    Button2: TButton;
    Button3: TButton;
    Button0: TButton;
    ButtonDiv: TButton;
    ButtonEqual: TButton;
    ButtonClear: TButton;
    ButtonClearEntry: TButton;
    Button7: TButton;
    ButtonLastClear: TButton;
    ButtonMod: TButton;
    ClearButton: TButton;
    ButtonDel: TButton;
    Button9: TButton;
    Button8: TButton;
    Edit1: TEdit;
    procedure ClearEntryClick(Sender: TObject);
    procedure Clear_LastClick(Sender: TObject);
    procedure ClearClick(Sender: TObject);
    procedure ClickZnak(Sender: TObject);
    procedure ClickBut(Sender: TObject);
    procedure equalClick(Sender: TObject);
  private

  public

  end;

var
  Form1: TForm1;
  a, b, c: real;
  d, e, f: integer;
  znak : string;

implementation

{$R *.lfm}

{ TForm1 }

procedure TForm1.ClearEntryClick(Sender: TObject);
begin
  Edit1.Clear;
end;

procedure TForm1.Clear_LastClick(Sender: TObject);
var
  str: string;
begin
  str:= Edit1.Text;
  if str <> '' then
  delete(str, Length(str),1);
  Edit1.Text:=str;
end;

procedure TForm1.ClearClick(Sender: TObject);
begin
  Edit1.Clear;
  a:=0;
  b:=0;
  c:=0;
  d:=0;
  e:=0;
  f:=0;
end;

procedure TForm1.ClickZnak(Sender: TObject);
begin
   if Edit1.Text = '' then
      ShowMessage('Введите число')
   else
   begin
        d:= strToInt(Edit1.Text);
        a:= strToFloat(Edit1.Text);
        Edit1.clear;
        znak:=(Sender as TButton).Caption;
   end;
end;

procedure TForm1.ClickBut(Sender: TObject);
begin
  Edit1.Text:=Edit1.Text + (Sender as TButton).Caption;
end;

procedure TForm1.equalClick(Sender: TObject);
begin
  if Edit1.Text = '' then
     ShowMessage('Ввидите число')
  else
  begin
  e:= strToInt(Edit1.text);
  b:= strtoFLoat(Edit1.Text);
  Edit1.Clear;
  case znak of
  '+' : c:= a+b;
  '-' : c:= a-b;
  '*' : c:=a*b;
  '/': if b = 0 then showmessage('На ноль делить нельзая') else
  c:=a/b;
  'Div': begin
  f:=d div e;
  c:=f;
  end;
  'Mod':begin
  f:=d mod e;
  c:=f;
  end;
  end;
  end;
  Edit1.Text:= FloatToStr(f);
  Edit1.Text:= FloatToStr(c);

end;

end.

