{
	@Author NeverLost. Based on code by Zilav (https://pastebin.com/raw/MxjSvzTq).
	Batch edits nif files to be parallax compatible
}
unit BatchParallaxScript;

// TODO: Fix input
// TODO: Fix ignorelist
// TODO: Tidy up code

const
	SEShape = 'BSTriShape'; // SE
	LEShape = 'NiTriShape'; // LE

function Initialize: Integer;
var
	sPath, sFile: string;
	TDirectory: TDirectory;
	files: TStringDynArray;
	i: integer;
	nif: TwbNifFile;
	SEChanged, LEChanged: Boolean;
begin
	// START OF UI
	if (InputQuery('Enter', 'Path to nif folder', sPath) = False) OR (Length(sPath) = 0) then begin
		exit(2);
	end;

	nif := TwbNifFile.Create;

	try
		files := TDirectory.GetFiles(sPath, '*.nif', soAllDirectories);

		for i := 0 to Pred(Length(files)) do begin
		  sFile := files[i];
		  if pos('lod', LowerCase(sFile)) <> 0 then continue;
		  
		  nif.LoadFromFile(sFile);
		  
		  AddMessage(' ');
		  AddMessage('FNR ' + IntToStr(i) + ': Adding parallax to: ' + sFile);
		  SEChanged := ReadBlockType(nif, SEShape);
		  LEChanged := ReadBlockType(nif, LEShape);

		  if (SEChanged) OR (LEChanged) then begin
			nif.SaveToFile(sFile);
			AddMessage('	SUCCESS. Added parallax to file.');
		  end
		  else
			AddMessage('	ERROR. Failed to add parallax to file.');
		end;

	finally
		nif.Free;
	end;

	Result := 1;
end;

function ReadBlockType(nif: TwbNifFile; shapeType: string): Boolean;
var
	bFilesChanged: Boolean;
	nodes: TList;
	shape, shader, data, textureSet: TwbNifBlock;
	i: Integer;
	tmp: string;
begin
	bFilesChanged := false;
	nodes := TList.Create;
	
	try
		nif.BlocksByType(shapeType, false, nodes);
		
		if nodes.Count <> 0 then		
			for i := 0 to Pred(nodes.Count) do begin
				shape := TwbNifBlock(nodes[i]);
				shader := nil;
				data := nil;
				textureSet := nil;
			
				if not IsValidBlock(nif, shape, shader, data, textureSet) then continue;
				
				if data = nil then shape.NativeValues['VertexDesc\VF'] := 944
				else data.NativeValues['Has Vertex Colors'] := 1;
			
				shader.NativeValues['Shader Type'] := 3;
				shader.NativeValues['Shader Flags 1\Parallax'] := 1;
				shader.NativeValues['Shader Flags 2\Vertex_Colors'] := 1;
				
				tmp := textureSet.NativeValues['Textures\[0]'];
				Insert('_p', tmp, pos('.dds',tmp));
				textureSet.NativeValues['Textures\[3]'] := tmp;
				
				bFilesChanged := true;
			end;
	finally
		nodes.Free;
	end;
	
	Result := bFilesChanged;
end;

function IsValidBlock(nif: TwbNifFile; var shape, shader, data, textureSet: TwbNifBlock): Boolean;
var
	index: Integer;
	alpha: TwbNifBlock;
	textures: TdfElement;
begin
	// Start of shape errors
	if strcomp(shape.BlockType, LEShape) = 0 then begin
		index := shape.NativeValues['Data'];
		if index = -1 then begin
			Msg(shape, 'WARN', 'Does not contain a data block.');
			exit(false)
		end
		else if shape.NativeValues['Skin Instance'] <> -1 then begin
			Msg(shape, 'WARN', 'Contains a NiSkinInstance.');
			exit(false)
		end;
	
		data := nif.Blocks[index];
	end
	else begin
		if shape.NativeValues['Skin'] <> -1 then begin
			Msg(shape, 'WARN', 'Contains a NiSkinInstance.');
			exit(false)
		end;
	end;
	
	// Start of alpha errors
	index := shape.NativeValues['Alpha Property'];
	if index <> -1 then begin
		Msg(shape, 'WARN', 'Contains a NiAlphaProperty.');
		exit(false)
	end;
	
	// Start of shader errors				
	index := shape.NativeValues['Shader Property'];
	if index = -1 then begin
		Msg(shape, 'WARN', 'Does not contain BSLightingShaderProperty.');
		exit(false)
	end;
	
	shader := nif.Blocks[index];
	if (shader.NativeValues['Shader Type'] <> 0) and (shader.NativeValues['Shader Type'] <> 3) then begin
		Msg(shape, 'WARN', 'Uses an incompatible shader.: ' + IntToStr(shader.NativeValues['Shader Type']));
		exit(false)
	end;
	if shader.NativeValues['Shader Flags 1\Decal'] <> 0 then begin
		Msg(shape, 'WARN', 'Has the Decal flag enabled.');
		exit(false)
	end;

	// Start of textureset errors
	index := shader.NativeValues['Texture Set'];
	if index = -1 then begin
		Msg(shape, 'WARN', 'Does not contain a textureSet block.');
		exit(false)
	end;
	
	textureSet := nif.Blocks[index];
	textures := textureSet[0];
	
	//for i := 0 to Pred(textures.Count) do begin
	//	if ignoreList.IndexOf(textures[i]) <> -1 then begin
	//		Msg(blockIndex, 'WARN', 'Textureset block contains an ignored texture.');
	//		Result := False;
	//	end;
	//end;}
	
	Result := true;
end;

procedure Msg(var shape: TwbNifBlock; strType, str: string);
begin
    AddMessage('	' + strType + '. Block: ' + IntToStr(shape.Index()) + ' ' + str);
end;

end.