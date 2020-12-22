from common.defines import *
from .p_data import Script, Property, Event, Function
from common.util import *

class Doc:
    TYPES = {
        Script.NAME : Script,
        Property.NAME : Property,
        Event.NAME : Event,
        Function.NAME : Function
    }

    @classmethod
    def from_file(cls, file):
        header = cls._parse_header(file)

        if not header:
            return None

        header_lower = header.lower()

        type_ = cls._get_type(header_lower)
        name = cls._get_name(header, header_lower, type_)
        
        data = cls.TYPES[type_].from_file(file)

        if isinstance(data, Property) and not header_lower.endswith(Property.SIMPLE_ENDING):
            cls._skip_property(file)

        # Return directly
        doc = Doc(header, name, data)

        return doc

    @classmethod
    def _get_type(cls, header_lower):
        for key in cls.TYPES:
            type_index = header_lower.find(key)
            if type_index != -1:
                return key

        # Could not find type
        raise Exception()

    @classmethod
    def _get_name(cls, header, header_lower, type_):
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

    @classmethod
    def _parse_header(cls, file):      
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

    @classmethod
    def _skip_property(cls, file):
        while True:
            line = file.readline()

            if not line:
                raise Exception()

            line = line.strip()

            if line and line.lower().startswith(Property.EXT_ENDING):
                break

    def __init__(self, header, name, data):
        self.header = header
        self.name = name
        self.data = data
        
    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name
        
    def __str__(self):
        return "#### <a id=\"{}\"></a> `{}`\n".format(self.name, self.header) + str(self.data)