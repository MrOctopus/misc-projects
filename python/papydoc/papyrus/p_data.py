from common.defines import DOC_VAR, DOC_END

from .p_var import Var, Author, Version, Get, Set, Usage, Param, Return

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

    @staticmethod
    def _parse_desc(file):
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

            if line[0] == DOC_VAR:
                has_vars = True
                file.seek(prev_pos)
                break
            
            if line[0] == DOC_END:
                break
            
            desc += line + '\n'

        return has_vars, desc[:-1]

    @classmethod
    def _parse_vars(cls, file):
        vars_ = []
        
        while (var := Var.from_file(file)):
            if not var.__class__ in cls.VALID_VARS:
                raise Exception()

            if not var.__class__ == Param and any(x.__class__ is var.__class__ for x in vars_):
                raise Exception()

            vars_.append(var)

        return vars_

    def __init__(self, desc = "", vars_ = None):
        self.desc = desc
        self.vars_ = vars_

    def to_md(self):
        return "\n{}{}".format(self.desc, self.to_md_vars())

    def to_md_vars(self):
        if not self.vars_:
            return ''

        return '\n' + ''.join([var.to_md() for var in self.vars_])

class Data_Param(Data):
    def to_md_vars(self):
        if not self.vars_:
            return ''

        params, rest = [], []

        for var in self.vars_:
            (rest, params)[var.__class__ is Param].append(var)

        var_str = ""

        if len(params) > 0:
            var_str = "\n\n##### {}s:{}".format(Param.NAME.capitalize(), ''.join([var.to_md() for var in params]))

        return var_str +  ''.join([var.to_md() for var in rest])

class Script(Data):
    NAME = 'scriptname'
    VALID_VARS = (
        Author,
        Version
    )

    def to_md(self):
        return "{}\n{}".format(self.to_md_vars(), self.desc)

class Property(Data):
    NAME = 'property'
    SIMPLE_END = ('auto', 'autoreadonly')
    EXT_END = 'endproperty'
    VALID_VARS = (
        Get,
        Set,
        Usage
    )

class Event(Data_Param):
    NAME = 'event'
    VALID_VARS = (
        Param,
        Usage
    )


class Function(Data_Param):
    NAME = 'function'
    VALID_VARS = (
        Param,
        Usage,
        Return
    )

DATA_TYPES = {
    Script.NAME : Script,
    Property.NAME : Property,
    Event.NAME : Event,
    Function.NAME : Function
}