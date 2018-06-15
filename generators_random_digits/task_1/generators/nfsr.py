from generators import *

import utils


class NFSR(Generator):
    PARAMS = ['p1', 'l1', 'p2', 'l2', 'p3', 'l3', 'w']

    # 5 5 5 101 201 991
    def __init__(self, params):
        self.p1 = utils.getParam(params.p1, utils.gen_param, [3, 10])
        self.p2 = utils.getParam(params.p2, utils.gen_param, [3, 10])
        self.p3 = utils.getParam(params.p3, utils.gen_param, [3, 10])
        self.l1 = utils.getParam(params.l1, utils.gen_param, [100, 10000])
        self.l2 = utils.getParam(params.l2, utils.gen_param, [100, 10000])
        self.l3 = utils.getParam(params.l3, utils.gen_param, [100, 10000])
        self.bits1 = list(map(int, bin(self.l1)[2:]))
        self.bits2 = list(map(int, bin(self.l2)[2:]))
        self.bits3 = list(map(int, bin(self.l3)[2:]))
        self.w = utils.getParam(params.p3, utils.gen_param, [3, 12])
        print('Аргументы: p1: {}, p2: {}, p3: {}, l1: {}, l2: {}, l3: {}, w: {}'.format(
            self.p1, self.p2, self.p3, self.l1, self.l2, self.l3, self.w))
        self.__validate()

    def __gen_bit(self, bits, p):
        lb = len(bits) - 1
        bit = 0
        for i in range(p):
            bit = bit ^ bits[lb - i]
        bits = [bit, *bits]
        bits = bits[:-1]
        return bit, bits

    def gen(self):
        result = 1
        for i in range(self.w):
            x1, self.bits1 = self.__gen_bit(self.bits1, self.p1)
            x2, self.bits2 = self.__gen_bit(self.bits2, self.p2)
            x3, self.bits3 = self.__gen_bit(self.bits3, self.p3)
            x = (x1 * x2) ^ (x2 * x3) ^ x3
            result = result | (x << i)
        return result

    def __validate(self):
        if self.p1 > len(self.bits1):
            raise Exception("p1 > колличества бит во входном слове")
        if self.p2 > len(self.bits2):
            raise Exception("p2 > колличества бит во входном слове")
        if self.p3 > len(self.bits3):
            raise Exception("p3 > колличества бит во входном слове")

    @staticmethod
    def info():
        return """
nfsr
Нелинейная комбинация РСЛОС
Аргументы:
p1, l1, p2, l2, p3, l3 - параметры для lfsr
w > 0, колличество значащих бит на выходе
"""