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
    START_DOC = '{'
    END_DOC = '}'

    @classmethod
    def from_file(file):
        previous_line = ""

        while True:
            line = file.readline()

            if not line:
                throw Exception

            line = line.strip()

            if line[0] is Doc.START_DOC:
                pass
            else:
                previous_line = line

    def __init__(self, name, name_full, description = "", params = None, return_val = ""):
        self.name = name
        self.name_full = name_full
        
        if description:
            self.description = description

        if params:
            self.params = params

        if return_val:
            self.return_val = return_val
        
    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name
        
    def __str__(self):
        # TODO(NeverLost): Convert to md
        return ""

class File_Doc:
    @classmethod
    def from_file(file_name : str, file):
        line = file.readline()
        
        if not line:
            throw Exception
            
        if line.lower().find(file_name.lower()) != 11:
            throw Exception
            
        #return cls(Doc_File(file_name, file, line))

    def __init__(self, doc):
        # Primary
        self.doc = doc
        
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
            self.functions.append(doc)
    
    def sort(self):
        self.properties.sort()
        self.events.sort()
        self.functions.sort()

def generate_md(doc_data):
    if not isinstance(doc_data, Doc_Data):
        return
        
    if doc_data.isempty():
        return
        
    doc_data.sort()
        
    # TODO(NeverLost): Generate md

def parse_file(file_path : str):
    if not file_path.lower().endswith(".psc"):
        return
    
    if not path.isfile(file_path):
        return
    
    file_name = path.splitext(path.basename(file_path))[0]
    
    with open(file_path, 'r') as file:
        try:
            file_doc = File_Doc(file_name, file)
        except Exception:
            return

        while True:
            try:
                doc = Doc.from_file(file)
                file_doc.add(doc)
            except Exception:
                break

def main(file_path : str):  
    if len(sys.argv) == 1:
        return

    # TODO(NeverLost): Support multiple args
    # TODO(NeverLost): Use argparse
    for file_path in sys.argv[1:]:
        doc_data = parse_file(file_path)
        generate_md(doc_data)

if __name__ is "__main__":
    main()