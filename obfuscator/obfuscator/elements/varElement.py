import re

from obfuscator.utils import checkTypes


class VarElement:
    def __init__(self, name: str, type, value=''):
        self.name = name.strip()
        self.type = type
        self.value = value

    @staticmethod
    def getVar(line):
        if not checkTypes(line.split()[0]):
            return []
        result = []
        line = line.replace(';', '')
        pat = '\(.*\)'
        line = re.sub(pat, '', line)
        _type = line.split()[0]
        line_pars = line.split(',')
        line_pars[0] = line_pars[0].replace(_type + ' ', '')
        for item in line_pars:
            it = item.replace(' ', '').replace('*', '')
            if not '=' in item:
                result.append(VarElement(it, _type))
            else:
                result.append(VarElement(it.split('=')[0], _type, it.split('=')[1]))
        return result

    def __str__(self):
        return 'name: "{}" type: "{}" value: "{}"'.format(self.name, self.type, self.value)
