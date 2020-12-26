from os import path
from common.util import *
from .p_data import *
from .p_doc import *

class File_Data:
    def __init__(self, file_path):
        name, ext =  path.splitext(path.basename(file_path).lower())

        if not ext == FILE_EXT:
            raise Exception()
        
        if not path.isfile(file_path):
            raise Exception()

        file = open(file_path, 'r')
        line = file.readline()
        
        if not line:
            raise Exception()

        if line.lower().find(name) != 11:
            raise Exception()

        file.seek(0, 0)
        
        self.doc = None
        self.doc_containers = [
            Doc_Container("Properties", Property),
            Doc_Container("Events", Event),
            Doc_Container("Functions", Function)
        ]

        # Data
        doc = Doc.from_file(file)

        if not doc:
            doc = Doc(sanitize_line(line), file_name, Data())
        elif not isinstance(doc.data, Script):
            self.add(doc)
            doc = Doc(sanitize_line(line), file_name, Data())

        self.doc = doc

        while doc := Doc.from_file(file):
            for container in self.doc_containers:
                if container.append(doc):
                    break

        container.sort() for container in self.doc_containers

        file.close()

    def to_md(self):
        return "# Documentation ({})".format(self.doc.name)

    def create_md(self, file_path):
        if self.isempty():
            return

        file_name = self.doc.name + '.md'
        file_path = path.join(file_path, file_name)
        
        with open(file_path, 'w') as file:
            file.write(self.to_md())
            file.write(self.doc.data.to_md())
            file.write("\n\n## Overview")

            # Index
            for doc_container in self.doc_containers:
                if doc_container:
                    file.write(doc_container.to_md_index())

                    for doc in doc_container:
                        file.write(doc.to_md_index())

                    file.write("\n")

            # Content
            for doc_container in self.doc_containers:
                if doc_container:
                    file.write(doc_container.to_md())

                    for doc in doc_container:
                        file.write(doc.to_md())

                    file.write("\n")