from collections import UserList
from bisect import insort

from common.defines import DOC_START
from common.util import sanitize_line

from .p_data import Script, Property, Event, Function, DATA_TYPES

class Doc:
    @classmethod
    def from_file(cls, file):
        header = cls._parse_header(file)

        if not header:
            return None

        header_lower = header.lower()

        type_ = cls._get_type(header_lower)
        name = cls._get_name(header, header_lower, type_)
        
        data = DATA_TYPES[type_].from_file(file)

        if isinstance(data, Property) and not header_lower.endswith(Property.SIMPLE_END):
            cls._skip_property(file)

        return cls(header, name, data)

    @staticmethod
    def _get_type(header_lower):
        for key in DATA_TYPES:
            type_index = header_lower.find(key)
            if type_index != -1:
                return key

        # Could not find type
        raise Exception()

    @staticmethod
    def _get_name(header, header_lower, type_):
        start_index = header_lower.find(type_)
            
        if start_index == -1:
            raise Exception()

        start_index = start_index + len(type_) + 1

        if type_ in (Script.NAME, Property.NAME):
            end_index = header_lower.find(' ', start_index)

            if end_index != -1:
                return header[start_index:end_index]
            else:
                return header[start_index:]
        
        elif (end_index := header_lower.find('(', start_index)) != -1:
            return header[start_index:end_index]

        raise Exception()

    @staticmethod
    def _parse_header(file):      
        prev_line = ""

        while True:
            prev_pos = file.tell()
            line = file.readline()

            if not line:
                return ""

            line = line.strip()

            if line and line[0] is DOC_START:
                file.seek(prev_pos)
                return prev_line

            prev_line = line

    @staticmethod
    def _skip_property(file):
        while True:
            line = file.readline()

            if not line:
                raise Exception()

            line = line.strip()

            if line and line.lower().startswith(Property.EXT_END):
                break

    def __init__(self, header, name, data):
        self.header = header
        self.name = name
        self.data = data
        
    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def to_md(self):
        return "\n#### <a id=\"{}\"></a> `{}`{}\n***".format(self.name, self.header, self.data.to_md())

    def to_md_index(self):
        return "\n* [{0}](#{0})".format(self.name)

class Doc_Container(UserList):
    def __init__(self, name, type_):
        super().__init__([])
        self.name = name
        self.type_ = type_

    def __add__(self, doc):
        if isinstance(doc.data, self.type_):
            return super().__add__(doc)
        return False

    def insort(self, doc):
        if isinstance(doc.data, self.type_):
            return insort(self, doc)
        return False

    def append(self, doc):
        if isinstance(doc.data, self.type_):
            return super().append(doc) 
        return False

    def extend(self, doc_list):
        for doc in doc_list:
            if not isinstance(doc.data, self.type_):
                return False
        return super().extend(doc_list)

    def to_md(self):
        return "\n## " + self.name

    def to_md_index(self):
        return "\n### " + self.name