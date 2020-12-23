from os import path
from common.util import *
from .p_data import *
from .p_doc import *

class File_Data:
    def __init__(self, file, file_path):
        line = file.readline()
        
        if not line:
            raise Exception()

        file_name = path.basename(file_path)
        file_name = path.splitext(file_name)[0]

        if line.find(file_name) != 11:
            raise Exception()

        file.seek(0, 0)

        # Data
        self.properties = []
        self.events = []
        self.functions = []

        doc = Doc.from_file(file)

        if not doc:
            doc = Doc(sanitize_line(line), file_name, Data())
        elif not isinstance(doc.data, Script):
            self.add(doc)
            doc = Doc(sanitize_line(line), file_name, Data())

        self.doc = doc

    def isempty(self):
        return len(self.properties) and len(self.events) and len(self.functions) == 0
    
    def add(self, doc):        
        if isinstance(doc.data, Property):
            self.properties.append(doc)
        elif isinstance(doc.data, Event):
            self.events.append(doc)
        elif isinstance(doc.data, Function):
            self.functions.append(doc)
        else:
            return False
        return True
    
    def sort(self):
        self.properties.sort()
        self.events.sort()
        self.functions.sort()

    def create_md(self, file_path):
        if self.isempty():
            return

        self.sort()

        file_name = self.doc.name + '.md'
        file_path = path.join(file_path, file_name)
        
        # TODO(NeverLost): This is obviously written very very poorly
        # will have to go back at some point for refactoring, but it works for now
        with open(file_path, 'w') as file:
            file.write("# Documentation ("+ self.doc.name + ")")
            file.write(self.doc.data.to_md())
            file.write("\n\n## Overview")

            # Index
            if len(self.properties) > 0:
                file.write("\n### Properties")

                for prop in self.properties:
                    file.write(prop.to_md_index())

                file.write("\n")

            if len(self.events) > 0:
                file.write("\n### Events")

                for event in self.events:
                    file.write(event.to_md_index())

                file.write("\n")

            if len(self.functions) > 0:
                file.write("\n### Functions")

                for function in self.functions:
                    file.write(function.to_md_index())

                file.write("\n")

            # Description
            if len(self.properties) > 0:
                file.write("\n## Properties")

                for prop in self.properties:
                    file.write(prop.to_md())

                file.write("\n")

            if len(self.events) > 0:
                file.write("\n## Events")

                for event in self.events:
                    file.write(event.to_md())

                file.write("\n")

            if len(self.functions) > 0:
                file.write("\n## Functions")

                for function in self.functions:
                    file.write(function.to_md())

                file.write("\n")