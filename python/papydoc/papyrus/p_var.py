from common.defines import DOC_VAR, DOC_END

class Var:
    NAME = ''

    @classmethod
    def from_file(cls, file):
        type_, desc = cls._parse_var(file)

        if not type_:
            return None

        return VAR_TYPES[type_](desc)

    @staticmethod
    def _parse_var(file):
        line = file.readline().strip()
        
        if line[0] == DOC_END:
            return None, None
        
        line = line.split(' ')

        if len(line) <= 1:
            raise Exception()

        type_ = line[0]

        if len(type_) <= 1:
            raise Exception()

        type_ = type_[1:].lower()
        desc = ' '.join(line[1:]) + '\n'

        while True:
            prev_pos = file.tell()
            line = file.readline()
            
            if not line:
                raise Exception()
            
            line = line.strip()

            if not line:
                continue

            if line[0] == DOC_VAR or line[0] == DOC_END:
                file.seek(prev_pos)
                break
            
            desc = desc + line + '\n'

        return type_, desc[:-1]

    def __init__(self, desc):
        self.desc = desc

    def to_md(self):
        return "\n\n##### {}:\n{}".format(self.__class__.NAME.capitalize(), self.desc)

class Author(Var):
    NAME = 'author'

    def to_md(self):
        return "\n### {}: {}".format(self.__class__.NAME.capitalize(), self.desc)

class Version(Var):
    NAME = 'version'

    def to_md(self):
        return "\n### {}: {}".format(self.__class__.NAME.capitalize(), self.desc)

class Param(Var):
    NAME = 'param'

    def to_md(self):
        return "\n* " + self.desc

class Get(Var):
    NAME = 'get'

class Set(Var):
    NAME = 'set'

class Usage(Var):
    NAME = 'usage'

class Return(Var):
    NAME = 'return'

VAR_TYPES = {
    Author.NAME : Author,
    Version.NAME : Version,
    Param.NAME : Param,
    Get.NAME : Get,
    Set.NAME : Set,
    Usage.NAME : Usage,
    Return.NAME : Return,
}