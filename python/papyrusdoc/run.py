#!/usr/bin/env python

__author__ = "NeverLost"
__version__ = "1.0.0"

import sys

from os import path
from papyrus import p_file
from common import defines
from papyrus.p_doc import Doc

def parse_file(file_path):
    if not file_path.lower().endswith(defines.FILE_EXT):
        raise Exception()
    
    if not path.isfile(file_path):
        raise Exception()
    
    with open(file_path, 'r') as file:
        file_data = p_file.File_Data(file, file_path)

        while doc := Doc.from_file(file):            
            file_data.add(doc)
            print(doc)

        return file_data

def main():
    if len(sys.argv) == 1:
        return

    # TODO(NeverLost): Use argparse
    for file_path in sys.argv[1:]:
        try:
            file_data = parse_file(file_path)
            file_data.generate_md_at(path.dirname(file_path))
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()