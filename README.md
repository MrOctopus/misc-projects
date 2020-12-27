# misc-projects
This repository is a collection of miscellaneous projects that I've made.
Their degree of completeness varies greately, so check the notes for each project before
using them.

## C++

### papyrusdrm.cpp
Exploits a bug in the champollion.exe decompiler by randomizing the compiler debug timestamp in a compiled papyrus file (.pex). Champollion expects the timestamp to be a 32 bit int, but in reality it is stored as a 64 bit int. Using the remaining bits crashes Champollion, but keeps the compiled script working in game. This effectively enforces a DRM upon the compiled script file. Reversing the process can be done through a hex-editor.

## Papyrus

### nl_util.psc
A papyrus utility script for key, value storage. Only requires SKSE. Example:
* keyname2
    - value
    - value

## Pascal

### nl_BatchParallax.pas
A pascal script that can be run using xEdit.exe. The script batch enables the required parallax flags in a given folder for all .nif files. The script supports
both LE and SE versions of Skyrim.

### nl_DeleteRecordsMod.pas
A pascal script that can be run using xEdit.exe. The script deletes placed references matching a given set of criterias. The modulo at which references are deleted
can be changed in the user input.

### nl_replaceTreeScript.pas
An incomplete pascal script that can be run using xEdit.exe. The purpose of the script is to enable batch replacing of placed references depending on their region parent.
The script only works in an hardcoded format at the moment.

## Python

### DDS-Format-Genie.py
A simple python script for determining the compression format used in a .dds file. Supports specific format filters and recursive traversal of .dds files.

### TexconvExtended.py
A python wrapper for the Texconv.exe program made by microsoft. The purpose of the script is to fix the recursive flag so that the folder structure is maintained
when no output path is given and the overwrite flag is enabled.