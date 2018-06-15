import re

from obfuscator import utils


class ForElement:
    @staticmethod
    def getStartOnBlock(block, s, f):
        pat = r'for\s*\([\w\d_]+\s+([\w\d_]+).*\)'
        r = re.compile(pat)
        vars = r.search(block[s:f])
        try:
            return s + vars.start(), vars.group(1)
        except:
            return None, None

    @staticmethod
    def forWithBrackets(block, s):
        s = utils.getIndexOfEndRightBracersSeq(block, s, ['(', ')'])
        return True if '{' in block[s: s + 20] else False
