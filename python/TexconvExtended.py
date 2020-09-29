#!/usr/bin/env python

__author__ = "NeverLost"
__version__ = "1.2.0"

import os
import sys
import subprocess

# CHANGE THIS TO THE PATH OF TEXCONV
PATH_TEXCONV = r"C:\Users\MrOctopus\Desktop\Misc\Texconv.exe"

# IGNORE EVERYTHING BELOW
VALID_FORMATS = [".BMP", ".JPG", ".JPEG", ".PNG", ".DDS", ".TGA", ".HDR", ".TIF", ".TIFF", ".WDP", ".HDP", ".JXR"]

# Quit with error message
def error_quit(error : str, err_code : int):
    print("[ERROR] {}".format(error))
    quit(err_code)

# Run the extended version of texconv
def extended_run(args, maintain_folders : bool):
    path = os.path.abspath(args[-1])
    ext = os.path.splitext(path)[1].upper()
    
    if not ext in VALID_FORMATS:
        error_quit("Failed to read {}".format(args[-1]), 2)

    path = path.rpartition(os.sep)

    for root, dirs, files in os.walk(path[0]):
        if maintain_folders:
            args[1] = root
            
        args[-1] = os.path.join(root, path[2])
        subprocess.run([PATH_TEXCONV] + args)

def main():
    print("")
    print("TEXCONV EXTENDED")
    print("----------------")

    if not os.path.isfile(PATH_TEXCONV):
        error_quit("Could not find texconv", 1)

    # Remove filename from args, create tmp_args
    # and check for flags
    args = sys.argv[1:]
    tmp_args = [each_string.lower() for each_string in args]

    if len(args) == 0:
        subprocess.run([PATH_TEXCONV])
        
    elif tmp_args.count('-r') == 0:
        subprocess.run([PATH_TEXCONV] + args)
        
    else:
        del args[tmp_args.index('-r')]
        
        maintain_folders = False

        if tmp_args.count('-o') == 0:
            args.insert(0, '-o')
            args.insert(1, 'tmp')
            maintain_folders = True
        
        extended_run(args, maintain_folders)
            
main()