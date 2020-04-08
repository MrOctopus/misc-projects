#!/usr/bin/env python

__author__ = "NeverLost"
__version__ = "1.1.0"

import os, sys, subprocess

# CHANGE THIS TO THE PATH OF TEXCONV.EXE
PATH_TEXCONV = r"C:\Users\MAX\Desktop\Misc\Texconv Test\Texconv.exe"

# IGNORE EVERYTHING BELOW
VALID_FORMATS = [".BMP", ".JPG", ".JPEG", ".PNG", ".DDS", ".TGA", ".HDR", ".TIF", ".TIFF", ".WDP", ".HDP", ".JXR"]

overwrite_output = False

def traverse(dir_path, name_file, args):
    for objname in os.listdir(dir_path):
        obj = os.path.join(dir_path, objname)

        if os.path.isdir(obj):
            traverse(obj, name_file, args)
    
    if overwrite_output:
        args[1] = dir_path
        
    args[-1] = os.path.join(dir_path + os.sep, name_file)
    subprocess.call([PATH_TEXCONV] + args)

def main():
    print("")
    print("TEXCONV EXTENDED")
    print("----------------")

    tmp_args = [each_string.lower() for each_string in sys.argv]

    if len(sys.argv) == 1:
        subprocess.call([PATH_TEXCONV])
        
    elif tmp_args.count('-r') == 0:
        subprocess.call([PATH_TEXCONV] + sys.argv[1:])
        
    else:
        del sys.argv[tmp_args.index('-r')]
        
        if tmp_args.count('-o') == 0:
            overwrite_output = True
            sys.argv.insert(1, '-o')
            sys.argv.insert(2, 'tmp')

        path_abs = os.path.abspath(sys.argv[-1])
        
        if os.path.splitext(path_abs)[1].upper() in VALID_FORMATS:
            path_delim = path_abs.rpartition(os.sep)
            traverse(path_delim[0], path_delim[2], sys.argv[1:])
            
        else:
            print("reading "+sys.argv[-1]+" FAILED")
            
main()