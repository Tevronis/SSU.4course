import random
import sympy


def isPrime(n):
    sympy.isprime(n)


def getParam(arg, func, args):
    if not arg is None:
        return arg
    return func(args)


def gen_param(args):
    return random.randint(args[0], args[1])
