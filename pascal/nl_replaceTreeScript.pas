{
  Deletes every record above height limit.
}
unit UserScript;

var
	Count: Integer;
	newFile: IInterface;
	
function Process(e: IInterface): integer;
var
	i: integer;
	rec: IInterface;
	frm: TForm;
	clb: TCheckListBox;
begin
	if (signature(e)) <> 'REFR' then exit; // If not Reference
	
	rec := BaseRecord(e);
	if (signature(rec) <> 'TREE') then exit; // If not matching type
	if (pos('TreePineForest01', EditorID(rec)) = 0) then exit; // Does not contain str
	
	if EditorIDExists(ElementByName(ChildrenOf(GetContainer(e)), 'XCLR - Regions')) then begin
	
		Inc(Count);
		if (Count mod 1 = 0) then begin // percentage, currently at 100%
			if not Assigned(newFile) then begin
				frm := frmFileSelect;
				try
				  frm.Caption := 'Select a plugin for the overrides';
				  clb := TCheckListBox(frm.FindComponent('CheckListBox1'));
				  clb.Items.Add('<new file>');
				  for i := Pred(FileCount) downto 0 do
					if GetFileName(e) <> GetFileName(FileByIndex(i)) then
					  clb.Items.InsertObject(1, GetFileName(FileByIndex(i)), FileByIndex(i))
					else
					  Break;
				  if frm.ShowModal <> mrOk then begin
					Result := 1;
					Exit;
				  end;
				  for i := 0 to Pred(clb.Items.Count) do
					if clb.Checked[i] then begin
					  if i = 0 then newFile := AddNewFile else
						newFile := ObjectToElement(clb.Items.Objects[i]);
					  Break;
					end;
				finally
				  frm.Free;
				end;
				if not Assigned(newFile) then begin
				  Result := 1;
				  Exit;
				end;
			end;
				
			AddMessage('Switching models');
			AddRequiredElementMasters(e, newFile, False);
			
			rec := wbCopyElementToFile(e, newFile, False, True);
			SetElementEditValues(rec, 'NAME - Base', '01000802');
		end;
	end;
end;

function EditorIDExists(container: IwbContainer): boolean;
var
  i: integer;
  s: string;
begin
  for i := 0 to ElementCount(container) -1 do begin
  s := EditorID(LinksTo(ElementByIndex(container, i)));
	if (pos(s, 'DanPineForest02') <> 0 OR pos(s, 'DanPineForest03') <> 0 OR pos(s, 'DanPineForest04') <> 0 OR pos(s, 'DanPineForest05') <> 0 OR pos(s, 'DanPineForest06') <> 0 OR pos(s, 'DanPineForest01Megan') OR pos(s, 'anDanPineForest01') <> 0 OR pos(s, 'PineForest01Andrew') <> 0) then begin
		Result := true;
		exit;
	end;
  end;
end;

end.