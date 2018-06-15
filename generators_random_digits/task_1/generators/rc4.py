from generators import *

import utils


class RC4(Generator):
    PARAMS = ['k']

    def __init__(self, params):
        mask = (2 ** 256) - 1
        self.K = utils.getParam(params.k, utils.gen_param, [0, mask]) & mask
        self.S = [i for i in range(256)]
        j = 0
        for i in range(256):
            j = (j + self.S[i] + RC4.get_byte(self.K, i)) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
        self.i = 0
        self.j = 0
        print('Аргументы: K: {}'.format(self.K))

    def gen(self):
        self.i = (self.i + 1) % 256
        self.j = (self.j + self.S[self.i]) % 256
        self.S[self.i], self.S[self.j] = self.S[self.j], self.S[self.i]
        t = (self.S[self.i] + self.S[self.j]) % 256
        return self.S[t]

    def __next__(self):
        return self.gen()

    @staticmethod
    def get_byte(a, i):
        return (a >> (i * 8)) & (2 ** 8 - 1)

    @staticmethod
    def info():
        return """
rc4
RC4
Аргументы:
k > 0, ключ
Генерирует случайные числа в интервале [0, 256]
"""