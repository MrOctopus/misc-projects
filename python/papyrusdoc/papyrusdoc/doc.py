from .util import *

class Data:
    def __init__(self, desc = ""):
        self.desc = desc

    def parse(self, file):
        # One Line comment
        line = file.readline().strip()

        if (end_index := line.find(Doc.END)) != -1:
            self.description = line[1:end_index]
            return None

        # Multi line comment
        while line:
            line = file.readline()
            
            # Malformed comment
            if not line:
                raise Exception()
            
            line = line.strip()

            if not line:
                self.desc += '\n'
                continue
            elif line[0] == Doc.END:
                return None
            elif line[0] == Doc.VAL:
                return line
            else:
                self.desc += line + '\n'

class Script(Data):
    VALID = (
        'author',
        'version'
    )

    def __init__(self, desc = "", author = "", version = ""):
        super().__init__(desc)
        self.author = author
        self.version = version

    def parse(self, file):
        last_line = super().parse(file)

        if not last_line: 
            return self

        #while line == Doc.VAR:
        #    break
        return self

class Property(Data):
    def __init__(self, desc = "", getter = None, setter = None):
        super().__init__(desc)
        self.getter = getter
        self.setter = setter

class Event(Data):
    VALID = (
        'param'
    )

    def __init__(self, desc = "", params = []):
        super().__init__(desc)
        self.params = params

class Function(Data):
    VALID = (
        'param',
        'return'
    )

    def __init__(self, desc = "", params = [], return_val = ""):
        super().__init__(desc)
        self.params = params
        self.return_val = return_val

DATA_TYPES = {
    'scriptname': Script,
    'property': Property,
    'event': Event,
    'function': Function
}
DATA_TYPES_TUPLE = tuple(DATA_TYPES)

class Header:
    def __init__(self, decl = "", name = "", data_type = ""):
        self.decl = decl
        self.name = name
        self.data_type = data_type

    def _get_decl_type(self, decl_lower):
        for key in DATA_TYPES_TUPLE:
            type_index = decl_lower.find(key)
            if type_index != -1:
                return key

        # Could not find type
        raise Exception()

    def _get_decl_name(self, decl_lower):
        start_index = decl_lower.find(self.data_type)
            
        if start_index == -1:
            raise Exception()

        start_index = start_index + len(self.data_type) + 1

        # TODO(NeverLost)
        # Rewrite this.
        # Horrible code
        if self.data_type in DATA_TYPES_TUPLE[0:2]:
            end_index = decl_lower.find(' ', start_index)

            if end_index != -1:
                return self.decl[start_index:end_index]
            else:
                return self.decl[start_index:]
        
        elif (end_index := decl_lower.find('(', start_index)) != -1:
            return self.decl[start_index:end_index]

        # Malformed header
        raise Exception()

    def parse(self, file):        
        # TODO(NeverLost): This is not too readable
        # Rewrite
        # Find header
        while True:
            prev_pos = file.tell()
            line = file.readline()

            if not line:
                return None

            line = line.strip()

            if not line:
                continue

            if line[0] is Doc.START:
                file.seek(prev_pos)
                break

            self.decl = line


        self.decl = sanitize_line(self.decl)
        decl_lower = self.decl.lower()
        self.data_type = self._get_decl_type(decl_lower)
        self.name = self._get_decl_name(decl_lower)

        return self

class Doc:
    START = '{'
    END = '}'
    VAR = '@'
    DOC_END = (END, VAR)

    def __init__(self, header = None, data = None):
        self.header = header
        self.data = data
        
    def __eq__(self, other):
        return self.header.name == other.header.name

    def __lt__(self, other):
        return self.header.name < other.header.name
        
    #def __str__(self):
        # TODO(NeverLost): Convert to md
    #    return ""

    def parse(self, file):
        header = Header().parse(file)

        if not header:
            return None

        data = DATA_TYPES[header.data_type]().parse(file)

        print(vars(header))
        print(data)

        return self