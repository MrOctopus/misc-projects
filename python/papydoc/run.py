#!/usr/bin/env python

__author__ = "NeverLost"
__version__ = "1.0.0"

import argparse
import glob

from os import path
from common.defines import FILE_EXT
from papyrus.p_file import File_data

def main():
    arg_parser = argparse.ArgumentParser(prog = "PaPyDoc")
    arg_parser.add_argument("-r", dest = "rec", help = "Enables recursive search", action='store_true')
    arg_parser.add_argument("-o", dest = "output", help = "Output path")
    arg_parser.add_argument("path", help = "specifies the file path")

    args = arg_parser.parse_args()

    #if not path.isdir(args.path):
    #    ext = path.splitext(args.path)[1].lower()
#
#        if ext != FILE_EXT:
#           if ext:
#              raise Exception()
#
#            args.path += FILE_EXT
#    else:
#        args.path += '*' + FILE_EXT

#    files
    files = glob.iglob(args.path, recursive=args.rec)
    #files = Path().rglob(args.path) if args.rec else Path.glob(args.path)
    readFiles = 0

    print(arg_parser.prog + ':')
    print("     TRYING TO READ FILES:")
    print()

    for file in files:
        print(file)

        try:
            file_data = File_Data(file)

            if args.output:
                file_data.create_md(args.output)
            else:
                file_data.create_md(path.dirname(file))

            ++readFiles
            print(readFiles)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()