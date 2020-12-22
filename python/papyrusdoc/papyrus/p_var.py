from common.defines import *

class Var:
    @classmethod
    def from_file(cls, file, valid_types):
        var = cls._parse_var(file, valid_types)

        if not var:
            return None

        return var

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

            if line[0] == DOC_END:
                return desc

            if line[0] == DOC_VAR:
                file.seek(prev_pos)
                return False

            desc += line + '\n'

    def __init__(self, var_, type_, desc):
        self.var_ = var_
        self.type_ = type_
        self.desc = desc