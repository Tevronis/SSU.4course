import re

from obfuscator import utils
from obfuscator.utils import types, checkTypes
from obfuscator.elements.varElement import VarElement


class FunctionElement:
    def __init__(self, name, variables=None, returnType=None):
        self.name = name
        self.variables = variables
        self.returnType = returnType

    def addVariable(self, v):
        self.variables.append(v)

    @staticmethod
    def delTypes(block, q=None):
        if q is None:
            q = FunctionElement.parseFunction(block)
        result = [q[0]]
        for line in q[1:]:
            if not checkTypes(line.split()[0]):
                result.append(line)
        result.append('}')
        return FunctionElement.glue(result)

    @staticmethod
    def glue(lines):
        result = ""
        for line in lines:
            result += line
        return result

    @staticmethod
    def getVariables(block, q=None):
        if q is None:
            q = FunctionElement.parseFunction(block)
        result = []
        for line in q[1:]:
            for item in VarElement.getVar(line):
                result.append(item)

        return result

    @staticmethod
    def isFunction(block):
        pat = r'[\w\d_]+\s+[\w\d_]+\s*\(.*\)\s*\{'
        p = re.compile(pat)
        return True if p.search(block) else False

    @staticmethod
    def getHead(block):
        pat = r'[\w\d_]+\s+[\w\d_]+\s*\(.*\)\s*\{'
        r = re.search(pat, block)
        start = r.end()
        return r.group(), start

    @staticmethod
    def parseFunction(block):
        # НЕ СТОИЛО ТЕБЕ ЗАХОДИТЬ СЮДА СТАЛКЕР
        def startWithFor(block):
            pat = r'^\s*for'
            return False if re.search(pat, block) else True

        def startWithWhile(block):
            pat = r'^\s*while'
            return False if re.search(pat, block) else True

        result = []
        head, shift = FunctionElement.getHead(block)
        # print(head, shift)
        result.append(head)
        pat = r'([\w\d\s<>().,\-=\[\]"\']+[;:]).?'
        while shift < len(block):
            # log = block[shift:]
            if startWithFor(block[shift:]) and block[shift:shift + 2] != 'if' and startWithWhile(block[shift:]):
                m = re.search(pat, block[shift:], re.DOTALL)
                if not m:
                    break
                line = m.group()
                shift += m.end()
                result.append(line)
            else:
                ss = utils.getIndexOfEndRightBracersSeq(block, shift, ['{', '}']) + 1
                result.append(block[shift: ss])
                shift = ss
        # возвращает распаршенный блок: заголовок, строки форы
        return result
