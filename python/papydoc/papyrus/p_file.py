from os import path

from common.util import sanitize_line

from .p_data import Script, Property, Event, Function
from .p_doc import Doc, Doc_Container

class PapyDoc:
    @classmethod
    def from_file_path(cls, file_path):
        with open(file_path, 'r') as file:
            file_doc, doc_containers = cls._parse_docs(file)
            return cls(file_doc, doc_containers)
    
    @staticmethod
    def _parse_docs(file):
        header = file.readline()

        if not header:
            raise Exception("Has no content.")
        
        file.seek(0, 0)
        file_doc = Doc.from_file(file)
        
        if not file_doc:
            raise Exception("Has no documentation.")
        
        doc_containers = [
            Doc_Container("Properties", Property),
            Doc_Container("Events", Event),
            Doc_Container("Functions", Function)
        ]

        if not isinstance(file_doc.data, Script):
            for container in doc_containers:
                if container.append(file_doc):
                    break

            file_name = path.splitext(path.basename(file.name))[0].lower()
            file_doc = Doc(sanitize_line(header), file_name, Script())

        while doc := Doc.from_file(file):
            for container in doc_containers:
                if container.insort(doc):
                    break

        return file_doc, doc_containers

    def __init__(self, doc, doc_containers):
        self.doc = doc
        self.doc_containers = doc_containers

    def isempty(self):
        return not any(self.doc_containers)

    def to_md(self):
        return "# Documentation ({}){}".format(self.doc.name, self.doc.data.to_md())

    def create_md_at(self, file_path):
        if self.isempty():
            return
        
        file_name = self.doc.name + '.md'
        file_path = path.join(file_path, file_name)

        with open(file_path, 'w') as file:
            file.write(self.to_md())
            file.write("\n\n## Overview")

            # Index
            for container in self.doc_containers:
                if container:
                    file.write(container.to_md_index())

                    for doc in container:
                        file.write(doc.to_md_index())

                    file.write("\n")

            # Content
            for container in self.doc_containers:
                if container:
                    file.write(container.to_md())

                    for doc in container:
                        file.write(doc.to_md())

                    file.write("\n")