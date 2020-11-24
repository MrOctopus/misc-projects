#!/usr/bin/env python

__author__ = "NeverLost"
__version__ = "1.0.0"

import sys
import os.path

class Type:
    FUNCTION = 0
    PROPERTY = 1

class Doc:
    def __init__(self):
        pass

def generate_md():
    pass

def main(file_path : String):  
    if not file_path.lower().endswith(".dds"):
        return

    name = path.splitext(path.basename(file_path))[0].lower()
    file = open(file_path, 'r')
    
    # TODO(NeverLost): Check if scriptname equals name
    
    # TODO(NeverLost): Generate docs
    
    # TODO(NeverLost): Generate md
    
    file.close()

if __name__ is "__main__":
    # Check arg error
    if len(sys.argv) == 1:
        return

    main()