import random

from generators import *

import utils


class FParam(Generator):
    PARAMS = ['p', 'q1', 'q2', 'q3', 'w']
    good = [[89, 20, 40, 69],
            [107, 31, 57, 82],
            [127, 22, 63, 83],
            [521, 86, 197, 447],
            [607, 167, 307, 461],
            [1279, 339, 630, 988],
            [2203, 585, 1197, 1656],
            [2281, 577, 1109, 1709],
            [3217, 809, 1621, 2381],
            [4253, 1093, 2254, 3297]]

    # Example: /g:lc /i:576897324234789332534655424534 /n:100 /f:output.txt /q1:20 /q2:40 /q3:69 /p:10 /w:10
    # необходимо все параметры задавать или никаких
    def __init__(self, params):
        self.ggood = random.choice(self.good)
        self.q1 = utils.getParam(params.q1, self.good_param, 1)
        self.q2 = utils.getParam(params.q1, self.good_param, 2)
        self.q3 = utils.getParam(params.q1, self.good_param, 3)
        self.p = utils.getParam(params.p, self.good_param, 0)
        self.X = utils.getParam(params.i, utils.gen_param, [2 ** (self.p + 1), 2 ** (self.p + 3)])
        self.w = utils.getParam(params.w, utils.gen_param, [3, 11])
        self.bits = list(map(int, bin(self.X)[2:]))
        print('Аргументы: q1: {}, q2: {}, q3: {}, p: {}, X: {}, w: {}'.format(self.q1, self.q2, self.q3, self.p, self.X, self.w))
        self.__validate()

    def __gen_bit(self):
        bit = self.bits[self.q1] ^ self.bits[self.q2] ^ self.bits[self.q3]
        self.bits = [bit, *self.bits]
        self.bits = self.bits[:-1]
        return bit

    def gen(self):
        result = 1
        for i in range(self.w):
            result = result | (self.__gen_bit() << i)
        return result

    def good_param(self, idx):
        return self.ggood[idx]

    def __validate(self):
        assert self.p > self.q1
        assert self.p > self.q2
        assert self.p > self.q3

    @staticmethod
    def info():
        return """
5p
Пятипараметрический метод
Аргументы: 
p > 0, колличество бит используемых следующего бита
q1, q2, q3 - индексы битов числа Х

w > 0, колличество значащих бит на выходе
Формула: Xn+1 = (Xn + Xn-1) mod m
"""