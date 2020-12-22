from common.defines import *
from .p_var import Var

class Data:
    NAME = ''
    VALID_VARS = ()

    @classmethod
    def from_file(cls, file):
        has_vars, desc = cls._parse_desc(file)
        vars_ = None

        if has_vars:
            vars_ = cls._parse_vars(file)

        return cls(desc, vars_)

    @classmethod
    def _parse_desc(cls, file):
        has_vars = False
        desc = ""

        # One Line comment
        line = file.readline().strip()

        if line[-1] == DOC_END:
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

            if line[0] == DOC_END:
                break
            elif line[0] == DOC_VAR:
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

    def __init__(self, desc = "", vars_ = []):
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
    SIMPLE_ENDING = ('auto', 'autoreadonly')
    EXT_ENDING = 'endproperty'
    VALID_VARS = (
        'get',
        'set',
        'usage',
        'context'
    )

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