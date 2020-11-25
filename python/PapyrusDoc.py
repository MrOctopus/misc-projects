#!/usr/bin/env python

__author__ = "NeverLost"
__version__ = "1.0.0"

import sys
import os.path
import enum

class Type(enum):
    SCRIPT = 0
    PROPERTY = 1
    EVENT = 2
    FUNCTION = 3

class Doc:
    TYPES_DOC("scriptname", "property", "event", "function")
    START_DOC = '{'
    END_DOC = '}'

    @classmethod
    def from_file(file):
        previous_line = ""

        while line := file.readline():
            line = line.strip()

            if line[0] is Doc.START_DOC:
                # Read different types here
                # Throw exceptions on malformed comments
                pass
            else:
                previous_line = line

        # EOF
        return None

    @from_line

    def __init__(self, name, name_full, description = None, params = None, return_val = None):
        self.name = name
        self.name_full = name_full
        self.description = description
        self.params = params
        self.return_val = return_val
        
    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name
        
    def __str__(self):
        # TODO(NeverLost): Convert to md
        return ""

class File_Doc:
    # len("Scriptname ") = 11
    EXPECTED_NAME_INDEX = 11

    @classmethod
    def from_file(file_name : str, file):
        line = file.readline()
        
        if not line:
            throw Exception()
            
        if line.lower().find(file_name.lower()) != cls.EXPECTED_NAME_INDEX:
            throw Exception()
        
        file.seek(0, 0)
        doc = Doc.from_file(file)

        if not doc
            file_doc = cls(Doc(file_name, line))
        elif not doc.type is Type.SCRIPT:
            file_doc = cls(Doc(file_name, line))
            file_doc.add(doc)
        else:
            file_doc = cls(doc)

        return file_doc

    def __init__(self, doc):
        # Primary
        if not isinstance(doc, Doc):
            throw Exception()

        self.doc = doc
        
        # Secondary
        self.properties = []
        self.events = []
        self.functions = []
    
    def isempty(self):
        return len(self.properties), len(self.events), len(self.functions) == 0
    
    def add(self, doc):
        if not isinstance(doc, Doc):
            throw Exception()
        
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
        throw Exception()
    
    if not path.isfile(file_path):
        throw Exception()
    
    file_name = path.splitext(path.basename(file_path))[0]
    
    with open(file_path, 'r') as file:
        file_doc = File_Doc.from_file(file_name, file)

        while doc := Doc.from_file(file):            
            file_doc.add(doc)

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