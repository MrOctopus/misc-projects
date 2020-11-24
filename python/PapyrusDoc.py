#!/usr/bin/env python

__author__ = "NeverLost"
__version__ = "1.0.0"

import sys
import os.path

# len("Scriptname ") = 11
EXPECTED_NAME_INDEX = 11

class Type:
    PROPERTY = "property"
    EVENT = "event"
    FUNCTION = "function"

class Doc:
    def __init__(self):
        self.name = ""
        
    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name
        
    def __str__(self):
        # TODO(NeverLost): Convert to md
        return ""

class Doc_Data:
    def __init__(self, name : String, author = "" : String, version = 1 : int):
        # Primary
        self.name = name
        self.author = author
        self.version = version
        
        # Secondary
        self.properties = []
        self.events = []
        self.functions = []
    
    def isempty(self):
        return len(self.properties), len(self.events), len(self.functions) == 0
    
    def add(self, doc):
        if not isinstance(doc, Doc):
            return
        
        if doc.type is Type.PROPERTY
            self.properties.append(doc)
        elif doc.type is Type.EVENT:
            self.events.append(doc)
        elif doc.type is Type.FUNCTION:
            slef.functions.append(doc)
    
    def sort(self):
        self.properties.sort()
        self.events.sort()
        self.functions.sort()

def generate_md(doc_data):
    if doc_data is None:
        return
        
    if doc_data.isempty():
        return
        
    doc_data.sort()
        
    # TODO(NeverLost): Generate md

def parse_file(file_path : String):
    if not file_path.lower().endswith(".dds"):
        return
    
    if not path.isfile(file_path):
        return
    
    name = path.splitext(path.basename(file_path))[0].lower()
    file = open(file_path, 'r')
    
    if file.readline().find(name) != 11:
        return
    
    # TODO(NeverLost): Generate docs
    
    file.close()

def main(file_path : String):  
    if len(sys.argv) == 1:
        return

    # TODO(NeverLost): Support multiple args
    # TODO(NeverLost): Use argparse
    for file in sys.argv[1:]:
        doc_data = parse_file(file)
        generate_md(doc_data)

if __name__ is "__main__":
    main()