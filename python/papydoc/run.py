#!/usr/bin/env python

__author__ = "NeverLost"
__version__ = "1.0.0"

import argparse
import glob

from os import path

from common.defines import FILE_EXT

from papyrus.p_file import PapyDoc

def main():
    arg_parser = argparse.ArgumentParser(prog = "PaPyDoc")
    arg_parser.add_argument("-r", dest = "rec", help = "Enables recursive search", action='store_true')
    arg_parser.add_argument("-o", dest = "output", help = "Output path")
    arg_parser.add_argument("path", help = "specifies the file path")

    args = arg_parser.parse_args()

    if path.isfile(args.path):
        ext = path.splitext(args.path)[1].lower()

        if ext != FILE_EXT:
            if ext:
                raise Exception()

            args.path += FILE_EXT

    if args.rec:
        args.path = path.join('**', args.path)

    file_paths = glob.iglob(args.path, recursive=args.rec)
    readFiles = 0

    print(arg_parser.prog + ':')

    for file_path in file_paths:
        print(file_path)

        try:
            papy_doc = PapyDoc.from_file_path(file_path)

            if args.output:
                papy_doc.create_md_at(args.output)
            else:
                papy_doc.create_md_at(path.dirname(file_path))

            readFiles += 1
            print(readFiles)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()