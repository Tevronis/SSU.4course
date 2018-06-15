from generators import *

import utils


class Mt(Generator):
    PARAMS = ['p', 'u', 's', 't', 'l', 'a', 'b', 'c', 'ff', 'w']

    p = 624
    w = 32
    r = 31
    q = 397

    # /u:11 /s:7 /t:15 /l:18 /a:2567483615 /b:2636928640 /c:4022730752 /ff:1812433253 /i:4022666752
    def __init__(self, params):
        self.w = utils.getParam(params.w, utils.gen_param, [4, 12])
        self.u = utils.getParam(params.u, utils.gen_param, [2, 31])
        self.s = utils.getParam(params.s, utils.gen_param, [2, 31])
        self.t = utils.getParam(params.t, utils.gen_param, [2, 31])
        self.l = utils.getParam(params.l, utils.gen_param, [2, 31])
        self.a = utils.getParam(params.a, utils.gen_param, [2 ** 30, 2 ** 31])
        self.b = utils.getParam(params.b, utils.gen_param, [2 ** 30, 2 ** 31])
        self.c = utils.getParam(params.c, utils.gen_param, [2 ** 30, 2 ** 31])
        self.ff = utils.getParam(params.ff, utils.gen_param, [2 ** 30, 2 ** 31])
        print('Аргументы: p: {}, u: {}, s: {}, t: {}, l: {}, a: {}, b: {}, c: {}, ff: {}, w: {}'.format(
            self.p, self.u, self.s, self.t, self.l, self.a, self.b, self.c, self.ff, self.w))
        self.mask_all = (2 ** Mt.w) - 1
        self.mask_last = 2 ** Mt.r
        self.mask_first = (2 ** Mt.r) - 1

        self.seed = utils.getParam(params.i, utils.gen_param, [100, 100000]) & self.mask_all

        self.a = [0] * Mt.p
        self.a[0] = self.seed
        for i in range(1, Mt.p):
            self.a[i] = ((self.ff * self.a[i - 1]) ^ ((self.a[i - 1] >> (Mt.w - 2)) + i)) & self.mask_all

        self.n = 0


    def gen(self):
        for i in range(Mt.p):
            y = (self.a[i] & self.mask_last) + (self.a[(i + 1) % Mt.p] & self.mask_first)
            self.a[i] = self.a[(i + Mt.q) % Mt.p] ^ (y >> 1)
            if y % 2:
                self.a[i] ^= self.b

    def __next__(self):
        if self.n == 0:
            self.gen()

        y = self.a[self.n]
        y ^= y >> self.u
        y ^= (y << self.s) & self.b
        y ^= (y << self.t) & self.c
        y ^= y >> self.l

        self.n = (self.n + 1) % Mt.p
        return y

    @staticmethod
    def info():
        return """
mt
Вихрь Мерсенна
Аргументы:
p, u, s, t, l, a, b, c, ff
w > 0, колличество значащих бит на выходе
"""
