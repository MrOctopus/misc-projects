from .util import *

class Var:
    @classmethod
    def _parse_var(cls, file, valid_types):
        var_ = ""
        line = file.readline().strip()

        line_split = line.split(' ')
        var_ = line_split[0][1:]

        if not var_ in valid_types:
            raise Exception()

        pass

        desc = ""

        while True:
            prev_pos = file.tell()
            line = file.readline()
            
            # Malformed comment
            if not line:
                raise Exception()
            
            line = line.strip()

            if not line:
                continue

            if line[0] == Doc.END:
                return desc

            if line[0] == Doc.VAL:
                file.seek(prev_pos)
                return False

            desc += line + '\n'

    @classmethod
    def from_file(cls, file, valid_types):
        var = cls._parse_var(file, valid_types)

        if not var:
            return None

        return var

    def __init__(self, var, type, desc):
        self.var_ = var_
        self.type_ = type_
        self.desc = desc

class Data:
    NAME = ''
    VALID_VARS = ()

    @classmethod
    def _parse_desc(cls, file):
        has_vars = False
        desc = ""

        # One Line comment
        line = file.readline().strip()

        if line[-1] == Doc.END:
            desc = line[1:-1]
            return has_vars, desc

        # Multi line comment
        while True:                        
            prev_pos = file.tell() 
            line = file.readline()

            if not line:
                raise Exception()

            line = line.strip()

            if not line:
                continue

            if line[0] == Doc.END:
                break
            elif line[0] == Doc.VAR:
                has_vars = True
                file.seek(prev_pos)
                break
            else:
                desc += line + '\n'

        return has_vars, desc[:-1]

    @classmethod
    def _parse_vars(cls, file):
        vars_ = []
        
        while var := Var.from_file(file, cls.VALID_VARS):
            if not var.type_ == 'param' and any(x._type == var._type for x in l):
                raise Exception()

            vars_.append(var)

        return vars_

    @classmethod
    def from_file(cls, file):
        has_vars, desc = cls._parse_desc(file)
        vars_ = None

        if has_vars:
            vars_ = cls._parse_vars(file)

        return cls(desc, vars_)

    def __init__(self, desc, vars_):
        self.desc = desc
        self.vars_ = vars_

    def __str__(self):
        return "{}\n\n".format(self.desc)


class Script(Data):
    NAME = 'scriptname'
    VALID_VARS = (
        'author',
        'version'
    )

    def __str__(self):
        return super().__str__() + ""

class Property(Data):
    NAME = 'property'
    VALID_VARS = (
        'get',
        'set',
        'usage',
        'context'
    )
    SIMPLE_ENDING = ('auto', 'autoreadonly')
    EXT_ENDING = 'endproperty'

class Event(Data):
    NAME = 'event'
    VALID_VARS = (
        'param',
        'usage',
        'context'
    )

class Function(Data):
    NAME = 'function'
    VALID_VARS = (
        'param',
        'return',
        'usage',
        'context'
    )

Data_Types = {
    Script.NAME : Script,
    Property.NAME : Property,
    Event.NAME : Event,
    Function.NAME : Function
}

# Merge with data?
class Doc:
    START = '{'
    END = '}'
    VAR = '@'

    @classmethod
    def _get_type(cls, header_lower):
        for key in Data_Types:
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

            if line and line[0] is Doc.START:
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

    @classmethod
    def from_file(cls, file):
        header = cls._parse_header(file)

        if not header:
            return None

        header_lower = header.lower()

        type_ = cls._get_type(header_lower)
        name = cls._get_name(header, header_lower, type_)
        
        data = Data_Types[type_].from_file(file)

        if isinstance(data, Property) and not header_lower.endswith(Property.SIMPLE_ENDING):
            cls._skip_property(file)

        # Return directly
        doc = Doc(header, name, data)

        return doc

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