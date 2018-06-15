from generators import *

import utils


class Lc(Generator):
    PARAMS = ['m', 'a', 'c']

    # Example: /g:lc /i:7 /n:100 /f:output.txt /a:106 /c:1283 /m:6075
    def __init__(self, parser):
        self.X = utils.getParam(parser.i, utils.gen_param, [20, 1000])
        self.m = utils.getParam(parser.m, utils.gen_param, [200, 10000])
        self.a = utils.getParam(parser.a, utils.gen_param, [20, 1000])
        self.c = utils.getParam(parser.c, utils.gen_param, [20, 1000])
        print('Аргументы: m: {}, a: {}, c: {}'.format(self.m, self.a, self.c))
        assert self.m > 0
        assert 0 <= self.a <= self.m
        assert 0 <= self.c <= self.m
        assert 0 <= self.X <= self.m

    def gen(self):
        self.X = (self.a * self.X + self.c) % self.m
        return self.X

    @staticmethod
    def info():
        return """
lc
Линейный конгруэнтный метод
Аргументы: 
m > 0, модуль
0 <= a <= m, множитель
0 <= c <= m, приращение
0 <= X0 <= m, начальное состояние
Формула: Xn+1 = (a*Xn + c) mod m
"""