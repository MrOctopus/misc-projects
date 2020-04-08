{
  Deletes every (*) record
}
unit UserScript;

var
	Count: Integer;
	CountRem: Integer;
	modVal: Integer;
	s1: string;
	s2: string;
  
function Initialize: integer;
var
	tmpS: string;
begin
  Result := 0;
  
  // ask for input
  if not InputQuery('Enter', 'REFR ID', s1) then begin
    Result := 2;
    Exit;
  end;
  if not InputQuery('Enter', 'Baserecord contains. Leave blank for no comparison', s2) then begin
    Result := 2;
    Exit;
  end;
  if not InputQuery('Enter', 'Delete every (*) record. Leave blank for default 50%', tmpS) then begin
    Result := 2;
    Exit;
  end;
  
  // empty string - do nothing
  if (s1 = '') OR (length(s1) <> 4) then begin
    Result := 3;
	Exit;
  end;

  if (tmpS = '') then modVal := 2 else modVal := StrToInt(tmpS);
end;

function Process(e: IInterface): integer;
var
	baseRec: IwbMainRecord;
begin
	if (signature(e)) <> 'REFR' then exit; // If not Reference
	
	baseRec := BaseRecord(e);
	if (signature(baseRec) <> s1) then exit; // If not matching type
	if (s2 <> '') AND (pos(s2, EditorID(baseRec)) = 0) then exit; // Does not contain str
	
	Inc(Count);
	if Count mod modVal = 0 then begin
		AddMessage('Removing: ' + Name(e));
		RemoveNode(e);
		Inc(CountRem);
	end;
end;

function Finalize: integer;
begin
  AddMessage('Total REFR records of defined type: ' + IntToStr(Count));
  AddMessage('Records removed: ' + IntToStr(CountRem));
end;


end.