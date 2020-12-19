from os import path
from .util import *
from .doc import *

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
        print(doc)

    def isempty(self):
        return len(self.properties), len(self.events), len(self.functions) == 0
    
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

    def generate_md(self, path):
        if self.isempty():
            return

        self.sort()