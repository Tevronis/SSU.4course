import random
from math import gcd

import sympy
from generators import *

import utils
from utils import isPrime


class RSAG(Generator):
    PARAMS = ['p', 'q', 'e', 'w']

    # p = 3557 q = 2579 e=3 w=8
    # /g:rsa /i:7 /n:100 /f:output.txt /p:3557 /q:2579 /e:3 /w:8
    def __init__(self, params):
        self.P = utils.getParam(params.p, RSAG.gen_prime, [100, 100000])
        self.Q = utils.getParam(params.q, RSAG.gen_prime, [100, 100000])
        self.n = self.P * self.Q
        self.f = (self.P - 1) * (self.Q - 1)
        self.e = utils.getParam(params.e, RSAG.gen_e, [1000]) #self.f])
        self.X = utils.getParam(params.i, utils.gen_param, [1, self.n])
        self.w = utils.getParam(params.w, utils.gen_param, [3, 12])
        print('Аргументы: p: {}, q: {}, e: {}, w: {}'.format(self.P, self.Q, self.e, self.w))
        self.lstbit = 5

    @staticmethod
    def gen_e(args):
        items = [x for x in range(2, args[0]) if gcd(args[0], x) == 1]
        return random.choice(items)

    def gen(self):
        result = 1
        for i in range(1, self.w):
            self.X = pow(self.X, self.e, self.n)
            w = int((self.X & (1 << self.lstbit)) != 0)
            result = result | (w << i)
        return result

    def validate(self):
        if isPrime(self.P):
            raise Exception("p not prime")
        if isPrime(self.Q):
            raise Exception("q not prime")
        if gcd(self.e, self.f) != 1:
            raise Exception("gcd(e, f) != 1")

    def __next__(self):
        return self.gen()

    @staticmethod
    def gen_prime(args):
        result = sympy.randprime(args[0], args[1])
        print("primes are genered")
        return result

    @staticmethod
    def info():
        return """
rsa
RSA
Аргументы:
p, q - простые числа
e, gcd(e, f) == 1
w > 0, колличество значащих бит на выходе
"""