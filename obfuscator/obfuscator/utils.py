import re

types = ['^int', '^string', '^double', '^float', '^vector<.*>', '^set<.*>']


class forGOTO:
    def __init__(self, from_, to, idx, value):
        self.from_ = from_
        self.to = to
        self.idx = idx
        self.value = value


def getIndexOfEndRightBracersSeq(text, start, char=None):
    if char is None:
        char = ['{', '}']

    result = start
    while text[result] != char[0]:
        result += 1
    balance = 1
    while balance != 0:
        result += 1
        if text[result] == char[0]:
            balance += 1
        if text[result] == char[1]:
            balance -= 1
    return result


def checkTypes(item):
    for pat in types:
        r = re.search(pat, item)
        if r:
            return True
    return False
