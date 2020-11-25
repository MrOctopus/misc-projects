#!/usr/bin/env python

__author__ = "NeverLost"
__version__ = "1.0.0"

import sys
import os.path
import enum

class Doc:
    def __init__(self, name, name_full, description = ""):
        self.name = name
        self.name_full = name_full
        self.description = description
        
    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name
        
    def __str__(self):
        # TODO(NeverLost): Convert to md
        return ""

class Doc_Script(Doc):
    def __init__(self):
        pass

class Doc_Property(Doc):
    def __init__(self):
        super().__init__()
        self.functions = functions

class Doc_Event(Doc):
    def __init__(self):
        super().__init__()
        self.params = params

class Doc_Function(Doc):
    def __init__(self):
        super().__init__()
        self.params = params
        self.return_val = return_val

class Doc_Factory:
    # Types
    SCRIPT = 'scriptname'
    PROPERTY = 'property'
    EVENT = 'event'
    FUNCTION = 'function'

    TYPES = {
        SCRIPT: Doc_Script, 
        PROPERTY: Doc_Property, 
        EVENT: Doc_Event,
        FUNCTION: Doc_Function
    }

    # Terminators
    START = '{'
    END = '}'
    VAR = '@'

    def __new__(cls, file):
        prev_line = ""

        # Find first comment
        while True:
            current_line = file.readline()

            if not current_line:
                return None

            current_line = current_line.strip()

            if current_line[0] is cls.START:
                break
    
            prev_line = current_line

        # Sanitize header
        offset_index = 0

        while index := prev_line.find(';', offset_index) != -1:
            lchar_index = index - 1

            if prev_line[lchar_index] == '\\':
                offset_index = index + 1
            else:
                prev_line = prev_line[:lchar_index].strip()

        prev_line_lower = prev_line.lower()

        # Parse
        doc_type = cls.parse_type(prev_line_lower)
        doc_name = cls.parse_name(prev_line, prev_line_lower, doc_type)
        doc_data = cls.parse_data(file, current_line)

        return cls.TYPES[doc_type[0]](doc_name, doc_data)

    @classmethod
    def parse_type(cls, header_lower):
        for key in cls.TYPES.keys():
            index = header_lower.find(key)
            if index != -1:
                return tuple(key, index)

        raise Exception()
    
    @classmethod
    def parse_name(cls, header, header_lower, doc_type):
        start_index = doc_type[1] + len(doc_type[0]) + 1
        
        if doc_type in (cls.SCRIPT, cls.PROPERTY):
            return tuple(header[start_index:], header)

        end_index = header_lower.find('(', start_index) 
            
        if end_index != -1:
            return tuple(header[start_index:end_index - 1], header)

        raise Exception()

    @classmethod
    def parse_data(cls, file, current_line):
        # Comment parsing
        if current_line.find(cls.END) != -1:

            # Single line comment
            pass

        while True:
            current_line = file.readline()

            # EOF
            if not current_line:
                raise Exception()

            current_line = current_line.strip()
            end_index = current_line.find(cls.END)

            if end_index > 0:
                raise Exception()

class File_Data:
    # len("Scriptname ") = 11
    EXPECTED_NAME_INDEX = 11

    def __init__(self, file_path, file):
        line = file.readline()
        
        if not line:
            raise Exception()
            
        self.file_name = path.splitext(path.basename(file_path))[0]

        if line.lower().find(file_name.lower()) != cls.EXPECTED_NAME_INDEX:
            raise Exception()

        dir_path = path.dirname(file_path)
        
        file.seek(0, 0)
        doc = Doc.from_file(file)

        if issubclass(doc, Doc):
            file_doc = cls(Doc(file_name, line))
            file_doc.add(doc)
        elif doc:
            file_doc = cls(Doc(file_name, line))
        else:
            file_doc = cls(doc)

        return file_doc

        self.doc = doc
        
        # Secondary
        self.properties = []
        self.events = []
        self.functions = []
    
    def isempty(self):
        return len(self.properties), len(self.events), len(self.functions) == 0
    
    def add(self, doc):        
        if isinstance(doc, Doc_Property):
            self.properties.append(doc)
        elif isinstance(doc, Doc_Event):
            self.events.append(doc)
        elif isinstance(doc, Doc_Function):
            self.functions.append(doc)
        else:
            raise Exception()
    
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
        raise Exception()
    
    if not path.isfile(file_path):
        raise Exception()
    
    with open(file_path, 'r') as file:
        file_doc = File_Data(file_path, file)

        while doc := Doc_Factory(file):            
            file_doc.add(doc)

def main(file_path : str):
    if len(sys.argv) == 1:
        return

    # TODO(NeverLost): Support multiple args
    # TODO(NeverLost): Use argparse
    for file_path in sys.argv[1:]:
        doc_data = parse_file(file_path)
        generate_md(doc_data)

if __name__ == "__main__":
    pass
    #main()