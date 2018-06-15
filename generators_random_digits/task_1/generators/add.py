from generators import *

import utils


class Add(Generator):
    PARAMS = ['m', 'x0', 'x1']

    # Example: /g:lc /i:7 /n:100 /f:output.txt /m:6075 /x0:7 /x1:11
    def __init__(self, param):
        self.m = utils.getParam(param.m, utils.gen_param, [100, 100000])
        self.x0 = utils.getParam(param.x0, utils.gen_param, [100, self.m])
        self.x1 = utils.getParam(param.x1, utils.gen_param, [100, self.m])
        print('Аргументы: m: {}, x0: {}, x1: {}'.format(self.m, self.x0, self.x1))
        assert self.m > 0

    def gen(self):
        self.x0, self.x1 = self.x1, (self.x0 + self.x1) % self.m
        return self.x1

    @staticmethod
    def info():
        return """
add
Аддитивный ГПСЧ
Аргументы: 
m > 0, модуль
x0, начальное состояние 1
x1, начальное состояние 2
Формула: Xn+1 = (Xn + Xn-1) mod m
"""
