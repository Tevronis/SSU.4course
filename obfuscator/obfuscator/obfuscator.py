# coding=utf-8
import random
import re

from obfuscator import utils
from obfuscator.elements.forElement import ForElement
from obfuscator.elements.functionElement import FunctionElement
from obfuscator.elements.varElement import VarElement
from obfuscator.utils import forGOTO, checkTypes


class Obfuscator:

    def __init__(self, file):
        self.varGlobal = []
        self.blocks = []

        with open(file) as f:
            self.text = f.read()
        self.__precondition()
        self.deleteComments()
        self.__genBlocks()

    def renameGlobalVariables(self):
        for item in self.varGlobal:
            self.text = Obfuscator.renameVariable(self.text, item.name)

    def getFunctions(self):
        pat = r'[\w\d_]+\s+([\w\d_]+)\s*\(.*\)\s*\{'
        p = re.compile(pat)
        ww = p.findall(self.text)
        result = [FunctionElement(item) for item in ww if item != 'main']
        return result

    def renameFunctions(self):
        funs = self.getFunctions()
        for fun in funs:
            self.text = self.renameVariable(self.text, fun.name)

    def __genBlocks(self):
        gen = self.__genBlock()
        for s, f in gen:
            self.blocks.append(self.text[s:f])
            if FunctionElement.isFunction(self.blocks[-1]) and self.blocks[-1][-1] != '}':
                self.blocks[-1] = self.blocks[-1] + '}'

    def renameVariables(self):
        for i, block in enumerate(self.blocks):
            self.blocks[i] = self.__refactorVariableOnBlock(block)

    def generateGoto(self):
        def generatePivo(lines, variables):
            result = [lines[0]]

            for var_ in variables:
                item = "\n\t{} {};".format(var_.type, var_.name)
                result.append(item)

            mark = self.__generateVarName()
            prev_mark = self.__generateVarName()
            result.append('\n\tgoto ' + str(prev_mark) + ';')
            ll = []
            for idx in range(1, len(lines)):
                item = forGOTO(prev_mark, mark, idx, lines[idx])
                mark, prev_mark = self.__generateVarName(), mark
                ll.append(item)
            random.shuffle(ll)
            toReturn = ''.join(result)
            for item in ll:
                toReturn += '\n\t' + str(item.from_) + ':\n'
                toReturn += str(item.value)
                toReturn += '\n\tgoto ' + str(item.to) + ';'
            toReturn += '\n\t' + str(prev_mark) + ':\n'
            toReturn += '\tint %s;\n}' % self.__generateVarName()
            return toReturn

        def setGoto(block):
            if FunctionElement.isFunction(block):
                parse_item = FunctionElement.parseFunction(block)

                variables = FunctionElement.getVariables(block, parse_item)
                result = FunctionElement.delTypes(block, parse_item)
                item = FunctionElement.parseFunction(result)
                result = generatePivo(item, variables)
                return result
            return block

        for idx, block in enumerate(self.blocks):
            self.blocks[idx] = setGoto(block)
        self.concatBlocks()

    def concatBlocks(self):
        self.text = ''
        for block in self.blocks:
            self.text += block

    def deleteComments(self):
        pat = "/\*.*?\*/"
        self.text = re.sub(pat, r'', self.text, flags=re.DOTALL)
        self.text = re.sub(r'//([^\n\t\r])+', r'', self.text)

    @staticmethod
    def renameVariable(block, arg):
        to = Obfuscator.__generateVarName()
        pat = r'\b(' + arg + r')\b'
        result = re.sub(pat, to, block)
        return result

    @staticmethod
    def __generateVarName():
        return r'N' + str(random.randint(1, 1000000000))

    def __refactorVariableOnBlock(self, block):
        def replaceArgs(block):
            patt = r"""\(( .* )\)\s*\{"""
            args = re.findall(patt, block, re.X)
            args = str(args[0]).split(',')
            for item in args:
                if item != '':
                    arg = item.split()[1]
                    block = Obfuscator.renameVariable(block, arg)
            return block

        def replaceFors(block):
            start = - 2
            while True:
                start, name = ForElement.getStartOnBlock(block, start + 2, len(block))
                if not start:
                    break

                if ForElement.forWithBrackets(block, start):
                    finish = utils.getIndexOfEndRightBracersSeq(block, start)
                    finish += 1

                    res = Obfuscator.renameVariable(block[start:finish], name)
                    block = block[:start] + res + block[finish:]
                else:
                    raise Exception('я не обрабатываю форы без скобочек сорян')
            return block

        def replaceVars(block, function=True):
            variables = []
            pat = r'[\w\d_<>]+\s+([\w\s_*]+).*;'
            r = re.compile(pat)
            # TODO избавиться от \n
            for line in block.split('\n'):
                if r.search(line):
                    line = line.strip()
                    m = line.split()

                    if checkTypes(m[0]):
                        v = VarElement.getVar(line[:])
                        variables += v
            if function:
                for item in variables:
                    block = Obfuscator.renameVariable(block, item.name)
            else:
                return variables
            return block

        if not FunctionElement.isFunction(block):
            vars = replaceVars(block, False)
            for var in vars:
                self.varGlobal.append(var)
            return block
        # Меняем аргументы во всей функции
        block = replaceArgs(block)
        # Меняем переменные в циклах
        block = replaceFors(block)
        # Меняем остальные переменные
        block = replaceVars(block)

        return block

    def __isGlobal(self, v):
        if self.varGlobal[v]:
            return True

    def __genBlock(self):
        finish = 0
        pat = r'[\w\d_]+\s+[\w\d_]+\s*\(.*\)\s*\{'
        p = re.compile(pat)
        for m in p.finditer(self.text):
            start = m.start()
            yield finish, start
            finish = utils.getIndexOfEndRightBracersSeq(self.text, start) + 1
            yield start, finish

        yield finish, len(self.text)

    def __precondition(self):
        self.text = re.sub(r' <', r'<', self.text)
        self.text = re.sub(r'< ', r'<', self.text)
        self.text = re.sub(r' >', r'>', self.text)
