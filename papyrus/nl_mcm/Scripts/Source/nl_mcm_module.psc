Scriptname nl_mcm_module extends Quest

;@author NeverLost
;@version 1.0.0

import Ui
import Debug

;-------\------------\
; MODULE \ PROPERTIES \
;--------------------------------------------------------

; MODULE CODES
int property OK = 1 autoreadonly
int property ERROR = 0 autoreadonly
int property ERROR_NOT_FOUND = -1 autoreadonly
int property ERROR_MCM_NOT_FOUND = -2 autoreadonly
int property ERROR_MAX_PAGE_REACHED = -3 autoreadonly
int property ERROR_PAGE_NAME_TAKEN = -4 autoreadonly
int property ERROR_NOT_INITIALIZED = -5 autoreadonly
int property ERROR_PAGE_NOT_FOUND = -6 autoreadonly
int property ERROR_PRESET_NOT_FOUND = -7 autoreadonly
int property ERROR_LOADING_DATA = -8 autoreadonly
int property ERROR_BUSY_WITH_DATA = -9 autoreadonly

; PAGE
int property OPTION_FLAG_NONE = 0x00 autoReadonly
int property OPTION_FLAG_DISABLED = 0x01 autoReadonly
int property OPTION_FLAG_HIDDEN	 = 0x02 autoReadonly
int property OPTION_FLAG_WITH_UNMAP	= 0x04 autoReadonly

int property LEFT_TO_RIGHT = 1 autoReadonly
int property TOP_TO_BOTTOM = 2 autoReadonly

string property MENU_ROOT
	string function Get()
		return "_root.ConfigPanelFader.configPanel"
	endfunction
endproperty

string property JOURNAL_MENU
	string function Get()
		return "Journal Menu"
	endfunction
endproperty

string property MSG_ERROR
	string function Get()
		return "NL_MCM(" + _page_name + "): An error occured."
	endfunction
endproperty

string property MSG_ERROR_NOT_FOUND
	string function Get()
		return "NL_MCM(" + _page_name + "): Quest with editor id " + _quest_editorid + " could not be found."
	endfunction
endproperty

string property MSG_ERROR_MCM_NOT_FOUND
	string function Get()
		return "NL_MCM(" + _page_name + "): Quest with editor id " + _quest_editorid + " has no nl_mcm attached."
	endfunction
endproperty

string property MSG_ERROR_MAX_PAGE_REACHED
	string function Get()
		return "NL_MCM(" + _page_name + "): The hooked MCM has already reached the page limit."
	endfunction
endproperty

string property MSG_ERROR_PAGE_NAME_TAKEN
	string function Get()
		return "NL_MCM(" + _page_name + "): The hooked MCM already has a page with the same name."
	endfunction
endproperty

string property MSG_ERROR_NOT_INITIALIZED
	string function Get()
		return "NL_MCM(" + _page_name + "): The hooked MCM is not initialized."
	endfunction
endproperty

string property MSG_ERROR_PAGE_NOT_FOUND
	string function Get()
		return "NL_MCM(" + _page_name + "): The hooked MCM has no matching page name."
	endfunction
endproperty

nl_mcm property UNSAFE_RAW_MCM hidden
    nl_mcm function Get()
        return MCM
    endFunction
endproperty

;-------\----------\
; MODULE \ INTERNAL \
;--------------------------------------------------------

int property EVENT_DEFAULT = 0 autoreadonly
int property EVENT_HIGHLIGHT = 1 autoreadonly
int property EVENT_SELECT = 2 autoreadonly
int property EVENT_OPEN = 3 autoreadonly
int property EVENT_ACCEPT = 4 autoreadonly
int property EVENT_CHANGE = 5 autoreadonly

nl_mcm MCM
string _quest_editorid
string _page_name
int _z
int _current_version

event _OnPageDraw()
	int version = GetVersion()
	
	if _current_version < version
		MCM.ShowMessage("Detected new module version: " + _current_version + " -> " + version + "\nUPDATING", false, "OK", "")
		OnVersionUpdateBase(version)
		OnVersionUpdate(version)
		_current_version = version
	endIf
	
	OnPageDraw()
endevent

event _OnPageEvent(string state_name, int event_id, float f, string str)
	GoToState(state_name)

	if event_id == EVENT_DEFAULT
		OnDefaultST()
	elseif event_id == EVENT_HIGHLIGHT
		OnHighlightST()
	elseif event_id == EVENT_SELECT
		OnSelectST()
	elseif event_id == EVENT_OPEN
		OnSliderOpenST()
		OnMenuOpenST()
		OnColorOpenST()
		OnInputOpenST()
	elseif event_id == EVENT_ACCEPT
		OnSliderAcceptST(f)
		OnMenuAcceptST(f as int)
		OnColorAcceptST(f as int)
		OnInputAcceptST(str)
	elseif event_id == EVENT_CHANGE
		OnKeyMapChangeST(f as int)
	endif
endevent

auto state _inactive
	event _OnPageDraw()
		Trace("NL_MCM: WARN, _OnPageDraw sent in inactive state!")
	endevent

	event _OnPageEvent(string state_name, int event_id, float f, string str)
		Trace("NL_MCM: WARN, _OnPageEvent sent in inactive state!")
	endevent

	event OnMenuOpen(string name)
		int return_code = RegisterModule(_page_name, _z, _quest_editorid)
		
		if return_code == OK || return_code == ERROR_MCM_NOT_FOUND
			StopTryingToRegister()
		endif
	endevent

;-------\-----\
; MODULE \ API \
;--------------------------------------------------------

	int function KeepTryingToRegister()
		if _page_name == ""
			return ERROR
		endif
		RegisterForMenu(JOURNAL_MENU)
		
		return OK
	endfunction
	
	int function StopTryingToRegister()
		UnregisterForMenu(JOURNAL_MENU)
		_quest_editorid = ""
		_page_name = ""
		_z = 0
		
		return OK
	endfunction

	int function RegisterModule(string page_name, int z = 0, string quest_editorid = "")				
		_quest_editorid = quest_editorid
		_page_name = page_name
		_z = z
		
		if quest_editorid == ""
			MCM = (self as quest) as nl_mcm
		else
			quest mcm_quest = Quest.GetQuest(quest_editorid)
			
			if !mcm_quest
				Notification(MSG_ERROR_NOT_FOUND)
				return ERROR_NOT_FOUND
			endif
		
			MCM = mcm_quest as nl_mcm
		endif
		
		if !MCM
			Notification(MSG_ERROR_MCM_NOT_FOUND)
			return ERROR_MCM_NOT_FOUND
		endif
		
		int error_code = MCM._RegisterModule(self, page_name, z)
		
		if error_code == OK
			_current_version = GetVersion()
			OnPageInit()
			GoToState("")
		elseif error_code == ERROR_MAX_PAGE_REACHED
			Notification(MSG_ERROR_MAX_PAGE_REACHED)
		elseif error_code == ERROR_PAGE_NAME_TAKEN
			Notification(MSG_ERROR_PAGE_NAME_TAKEN)
		endif
		
		return error_code
	endfunction
		
	int function UnregisterModule()
		return ERROR
	endfunction
endstate

int function KeepTryingToRegister()
	return ERROR
endfunction

int function StopTryingToRegister()
	return ERROR
endfunction

int function RegisterModule(string page_name, int z = 0, string quest_editorid = "")
	return ERROR
endfunction

int function UnregisterModule()
	int error_code = MCM._UnregisterModule(_page_name)
	
	if error_code == OK
		GoToState("_inactive")
		_quest_editorid = ""
		_page_name = ""
		_z = 0
	elseif error_code == ERROR_NOT_INITIALIZED
		Notification(MSG_ERROR_NOT_INITIALIZED)
	elseif error_code == ERROR_PAGE_NOT_FOUND
		Notification(MSG_ERROR_PAGE_NOT_FOUND)
	endif
	
	return error_code
endfunction

;--------\-----\
; MCM API \ NEW \
;--------------------------------------------------------

function AddParagraph(string text, string begin_format = "", string end_format = "", int flags = 0x01)
	MCM.AddParagraph(text, begin_format, end_format, flags)
endfunction

function SetSplashScreen(string path, float x = 0.0, float y = 0.0)
	MCM.SetSplashScreen(path, x, y)
endfunction

function SetSliderDialog(float value, float range_start, float range_end, float interval, float default)
	MCM.SetSliderDialog(value, range_start, range_end, interval, default)
endFunction 

function SetMenuDialog(string[] options, int start_i, int default_i = 0)
	MCM.SetMenuDialog(options, start_i, default_i)
endFunction

function RefreshPages()
	MCM.RefreshPages()
endfunction

function ExitMCM(bool fully = false)
	if GetString(JOURNAL_MENU, MENU_ROOT + ".titlebar.textField.text") != _page_name
		return
	endif
	
	InvokeInt(JOURNAL_MENU, MENU_ROOT + ".changeFocus", 0)
	Invoke(JOURNAL_MENU, MENU_ROOT + ".contentHolder.modListPanel.showList")
	
	if fully
		Invoke(JOURNAL_MENU, "_root.QuestJournalFader.Menu_mc.ConfigPanelClose")
		InvokeBool(JOURNAL_MENU, "_root.QuestJournalFader.Menu_mc.CloseMenu", true)
	endif
endfunction

;--------\----------\
; MCM API \ ORIGINAL \
;--------------------------------------------------------

int property CurrentVersion hidden
    int function Get()
        return _current_version
    endFunction
endproperty

function SetCursorFillMode(int a_fillMode)
	MCM.SetCursorFillMode(a_fillMode)
endfunction

int function AddHeaderOption(string a_text, int a_flags = 0)
	return MCM.AddHeaderOption(a_text, a_flags)
endfunction

int function AddEmptyOption()
	return MCM.AddEmptyOption()
endfunction

function AddTextOptionST(string a_stateName, string a_text, string a_value, int a_flags = 0)
	MCM.AddTextOptionST(a_stateName, a_text, a_value, a_flags)
endfunction

function AddToggleOptionST(string a_stateName, string a_text, bool a_checked, int a_flags = 0)
	MCM.AddToggleOptionST(a_stateName, a_text, a_checked, a_flags)
endfunction

function AddSliderOptionST(string a_stateName, string a_text, float a_value, string a_formatString = "{0}", int a_flags = 0)
	MCM.AddSliderOptionST(a_stateName, a_text, a_value, a_formatString, a_flags)
endfunction

function AddMenuOptionST(string a_stateName, string a_text, string a_value, int a_flags = 0)
	MCM.AddMenuOptionST(a_stateName, a_text, a_value, a_flags)
endfunction

function AddColorOptionST(string a_stateName, string a_text, int a_color, int a_flags = 0)
	MCM.AddColorOptionST(a_stateName, a_text, a_color, a_flags)
endfunction

function AddKeyMapOptionST(string a_stateName, string a_text, int a_keyCode, int a_flags = 0)	
	MCM.AddKeyMapOptionST(a_stateName, a_text, a_keyCode, a_flags)
endfunction

function SetOptionFlagsST(int a_flags, bool a_noUpdate = false, string a_stateName = "")
	if a_stateName == ""
		a_stateName = GetState()
	endif
	MCM.SetOptionFlagsST(a_flags, a_noUpdate, a_stateName)
endfunction

function SetTextOptionValueST(string a_value, bool a_noUpdate = false, string a_stateName = "")
	if a_stateName == ""
		a_stateName = GetState()
	endif
	MCM.SetTextOptionValueST(a_value, a_noUpdate, a_stateName)
endfunction

function SetToggleOptionValueST(bool a_checked, bool a_noUpdate = false, string a_stateName = "")
	if a_stateName == ""
		a_stateName = GetState()
	endif
	MCM.SetToggleOptionValueST(a_checked, a_noUpdate, a_stateName)
endfunction

function SetSliderOptionValueST(float a_value, string a_formatString = "{0}", bool a_noUpdate = false, string a_stateName = "")	
	if a_stateName == ""
		a_stateName = GetState()
	endif
	MCM.SetSliderOptionValueST(a_value, a_formatString, a_noUpdate, a_stateName)
endfunction

function SetMenuOptionValueST(string a_value, bool a_noUpdate = false, string a_stateName = "")
	if a_stateName == ""
		a_stateName = GetState()
	endif
	MCM.SetMenuOptionValueST(a_value, a_noUpdate, a_stateName)
endfunction

function SetColorOptionValueST(int a_color, bool a_noUpdate = false, string a_stateName = "")
	if a_stateName == ""
		a_stateName = GetState()
	endif
	MCM.SetColorOptionValueST(a_color, a_noUpdate, a_stateName)
endfunction

function SetKeyMapOptionValueST(int a_keyCode, bool a_noUpdate = false, string a_stateName = "")
	if a_stateName == ""
		a_stateName = GetState()
	endif
	MCM.SetKeyMapOptionValueST(a_keyCode, a_noUpdate, a_stateName)
endfunction

function SetSliderDialogStartValue(float a_value)
	MCM.SetSliderDialogStartValue(a_value)
endfunction

function SetSliderDialogDefaultValue(float a_value)
	MCM.SetSliderDialogDefaultValue(a_value)
endfunction

function SetSliderDialogRange(float a_minValue, float a_maxValue)
	MCM.SetSliderDialogRange(a_minValue, a_maxValue)
endfunction

function SetSliderDialogInterval(float a_value)
	MCM.SetSliderDialogInterval(a_value)
endfunction

function SetMenuDialogStartIndex(int a_value)
	MCM.SetMenuDialogStartIndex(a_value)
endfunction

function SetMenuDialogDefaultIndex(int a_value)
    MCM.SetMenuDialogDefaultIndex(a_value)
endfunction

function SetMenuDialogOptions(string[] a_options)
	MCM.SetMenuDialogOptions(a_options)
endfunction

function SetColorDialogStartColor(int a_color)
	MCM.SetColorDialogStartColor(a_color)
endfunction

function SetColorDialogDefaultColor(int a_color)
	MCM.SetColorDialogDefaultColor(a_color)
endfunction

function SetCursorPosition(int a_position)
	MCM.SetCursorPosition(a_position)
endfunction

function SetInfoText(string a_text)
	MCM.SetInfoText(a_text)
endfunction

function ForcePageReset()
	MCM.ForcePageReset()
endfunction

function LoadCustomContent(string a_source, float a_x = 0.0, float a_y = 0.0)
	MCM.LoadCustomContent(a_source, a_x, a_y)
endfunction

function UnloadCustomContent()
	MCM.UnloadCustomContent()
endfunction

bool function ShowMessage(string a_message, bool a_withCancel = true, string a_acceptLabel = "$Accept", string a_cancelLabel = "$Cancel")
	return MCM.ShowMessage(a_message, a_withCancel, a_acceptLabel, a_cancelLabel)
endfunction

int function SaveMCMToPreset(string preset_name)
	return MCM.SaveMCMToPreset(preset_name)
endfunction

int function LoadMCMFromPreset(string preset_name, bool no_ext = false)
	return MCM.LoadMCMFromPreset(preset_name, no_ext)
endfunction

int function GetMCMSavedPresets(string[] none_array, string default_fill, bool no_ext = true)
	return MCM.GetMCMSavedPresets(none_array, default_fill, no_ext)
endfunction 

int function DeleteMCMSavedPreset(string preset_name)
	return MCM.DeleteMCMSavedPreset(preset_name)
endfunction

;-------------\
; OVERRIDE API \
;--------------------------------------------------------

int function GetVersion()
	return 1
endfunction

int function SaveData()
endfunction

function LoadData(int jObj)
endfunction

event OnVersionUpdateBase(int a_version)
endevent

event OnVersionUpdate(int a_version)
endevent

event OnConfigClose()
endevent

event OnPageInit()
endevent

event OnPageDraw()
endevent

event OnDefaultST()
endevent

event OnHighlightST()
endevent

event OnSelectST()
endevent

event OnSliderOpenST()
endevent

event OnMenuOpenST()
endevent

event OnColorOpenST()
endevent

event OnSliderAcceptST(float f)
endevent

event OnMenuAcceptST(int i)
endevent

event OnColorAcceptST(int col)
endevent

event OnInputOpenST()
endevent

event OnInputAcceptST(string str)
endevent

event OnKeyMapChangeST(int keycode)
endevent
