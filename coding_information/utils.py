class node:
    def __init__(self, ch, x, left=None, right=None):
        self.ch = ch
        self.x = x
        self.left = left
        self.right = right

    @staticmethod
    def cmp(f, s):
        if f.x == s.x:
            return 0
        return 1 if f.x < s.x else -1

    @staticmethod
    def cmp_rev(f, s):
        if f.x == s.x:
            return 0
        return -1 if f.x < s.x else 1


def byteToChar(mas):
    res = 0
    for i, item in enumerate(mas):
        if item == '1':
            res += 2 ** i
    return chr(res)


def charToByte(ch):
    result = ''
    x = ord(ch)
    for i in range(8):
        result += str(x % 2)
        x //= 2
    return result
