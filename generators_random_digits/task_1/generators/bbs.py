import random
from math import gcd

import sympy
from generators import *

import utils


class BBS(Generator):
    PARAMS = ['p', 'q', 'l']

    # p 355789347 q 257923422 x 346711
    # /g:bbs /i:346711 /n:1000 /f:output.txt /p:355789347 /q:257923422 /l:9
    def __init__(self, params):
        self.w = utils.getParam(params.l, utils.gen_param, [3, 12])
        self.p = utils.getParam(params.p, BBS.gen_pq, [100, 1000000])  # & ((2 ** 9) - 1)
        self.q = utils.getParam(params.q, BBS.gen_pq, [100, 1000000])  # & ((2 ** 9) - 1)
        self.n = self.p * self.q
        self.x = utils.getParam(params.i, BBS.chose_x, [self.n])
        self.X = (self.x * self.x) % self.n
        self.lstbit = 7
        print('Аргументы: w: {}, p: {}, q: {}, n: {}, x: {}'.format(self.w, self.p, self.q, self.n, self.x))
        self.validate()

    def gen(self):
        result = 1
        for i in range(1, self.w):
            self.X = pow(self.X, 2, self.n)
            w = int((self.X & (1 << self.lstbit)) != 0)
            result = result | (w << i)
        return result

    @staticmethod
    def chose_x(n):
        result = 7
        while gcd(result, n[0]) != 1:
            result = random.randint(100, 10000000)
        return result

    def validate(self):
        if (self.p - 3) % 4 != 0:
            raise Exception("p not valid: (p - 3) = 0 (mod 4)")
        if (self.q - 3) % 4 != 0:
            raise Exception("q not valid: (q - 3) = 0 (mod 4)")
        if gcd(self.x, self.n) != 1:
            raise Exception("gcd(x, n) != 1")

    def __next__(self):
        return self.gen()

    @staticmethod
    def gen_pq(args):
        result = 5
        while (result - 3) % 4 != 0:
            result = sympy.randprime(args[0], args[1])
        return result

    @staticmethod
    def info():
        return """
bbs
Алгоритм Блюма-Блюма-Шуба (BBS)
Аргументы:
p, q - простые числа
i - начальное значение
l > 0, колличество значащих бит на выходе
"""