from generators import *

import utils


class LFSR(Generator):
    PARAMS = ['p', 'x', 'w']

    # a = 576897324234
    def __init__(self, params):
        self.p = utils.getParam(params.p, utils.gen_param, [10, 1000])
        self.w = utils.getParam(params.w, utils.gen_param, [3, 12])
        self.X = utils.getParam(params.x, utils.gen_param, [2 ** (self.p + 1), 2 ** (self.p + 3)])
        self.bits = list(map(int, bin(self.X)[2:]))
        self.lb = len(self.bits) - 1
        print('Аргументы: p: {}, x: {}, w: {}'.format(self.p, self.X, self.w))
        self.__validate()

    def __gen_bit(self):
        bit = 0
        for i in range(18):
            bit = bit ^ self.bits[self.p - i]
        self.bits = [bit, *self.bits]
        self.bits = self.bits[:-1]
        return bit

    def gen(self):
        result = 1
        for i in range(self.w):
            result = result | (self.__gen_bit() << i)
        return result

    def __validate(self):
        assert self.p > 0
        assert self.w > 0
        if self.p > self.lb:
            raise Exception("Некорректные p или X")

    @staticmethod
    def info():
        return """
lfsr
Регистр сдвига с обратной линейной связью
Аргументы: 
p > 0, колличество бит используемых следующего бита
x, |x| >= p, начальное значение, необходимо, чтобы его длинна была больше или равна p
w > 0, колличество значащих бит на выходе
Формула: Xn+1 = (Xn + Xn-1) mod m
"""
