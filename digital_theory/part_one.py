# -*- coding: utf-8 -*-
import math
import random
from math import sqrt, trunc, log

from utils import *


def test_simple(fn):
    def wrapped():
        for i in range(3, 100):
            if fn(i):
                print str(i) + ' is simple'

    return wrapped


def test_wilson(num):
    def wilson(p):
        return True if (math.factorial(p - 1) + 1) % p == 0 else False

    print 'Test Wilson:\t\t',
    for item in num:
        yield wilson(item)


def test_ferma(num):
    print 'Test Ferma:\t\t\t',

    def ferma(n):
        bad = False
        for a in range(1, n):
            if gcd(a, n) == 1:
                if not (a ** (n - 1)) % n == 1:
                    bad = True
                    break
        return not bad

    for item in num:
        yield ferma(item)


def test_yakobi():
    for i in range(2, 100):
        for j in range(1, 100):
            if j % 2 == 1:
                r = yakobi(i, j)
                print '({0} {1}): {2}'.format(i, j, r)
            else:
                print '({0} {1}): {2}'.format(i, j, 'none')


def test_solovei2(num):
    print 'test Solovei:\t\t',

    def solo(nm):
        for k in range(1, 5):
            a = random.randrange(1, nm)
            if not gcd(a, nm) > 1:
                b = a ** ((nm - 1) / 2)
                r = yakobi(a, nm)
                if (b - r) % nm != 0:
                    break
            else:
                break
        else:
            return True
        return False

    for item in num:
        yield solo(item)


def test_solovei(cnt, prints=True):
    if prints:
        print 'test Solovei:'
    result = []
    for n in range(2, cnt, 1):
        for k in range(1, 5):
            a = random.randrange(1, n)
            if not gcd(a, n) > 1:
                b = a ** ((n - 1) / 2)
                r = yakobi(a, n)
                if (b - r) % n != 0:
                    break
            else:
                break
        else:
            result.append(n)
            if prints:
                print str(n) + ' is simple'
    return result


def test_miller_rabin(num):
    def getST(x):
        for s in range(4 * x):
            for t in range(1, 4 * x, 2):
                if x == 2 ** s * t:
                    return s, t

    def miller_rabin(n):
        s, t = getST(n - 1)
        rng = 10
        for k in range(rng):
            a = random.randrange(2, n - 2)
            x = (a ** t) % n
            if x == 1 or x == n - 1:
                continue
            for i in range(s):
                x = (x * x) % n
                if x == 1:
                    return False
                if x == n - 1:
                    break
            return False
        return True

    print 'test Rabin-Miller:\t',
    for item in num:
        yield miller_rabin(item)


def Factor(n):
    result = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            result.append(d)
            n //= d
        else:
            d += 1
    if n > 1:
        result.append(n)
    return result


def test_karmaikla(num):
    # http://cryptowiki.net/index.php?title=Числа_Кармайкла
    print 'test Karmaikla:\t\t',
    sq = [i * i for i in range(2, 1000)]

    def without_2(x):
        for item in sq:
            if x % item == 0:
                return False
        return True

    def karmaikl(n):
        if without_2(n):
            fac = Factor(n)
            if len(fac) == 1:
                return False
            for item in fac:
                if (n - 1) % (item - 1) != 0:
                    break
            else:
                return True
            return False
        else:
            return False

    for item in num:
        yield karmaikl(item)


def test_polinom(num):
    print 'test polinom:\t\t',

    def AKS(number):
        a = 2
        coefficients = generateCoefficientsAKS(number, a)
        result = True
        for v in coefficients:
            if not (v % number == 0):
                result = False
        return result

    def C(n, k):
        result = 1
        m = max(n - k, k)
        for i in range(m + 1, n + 1):
            result *= i
        for i in range(2, n - m + 1):
            result //= i
        return result

    def generateCoefficientsAKS(n, a):
        av = a
        an = a
        result = [0 for i in range(n)]
        for i in range(1, n):
            result[i] = C(n, i) * an
            an = an * av
        result[0] = an - av
        return result

    for item in num:
        if item > 2000:
            yield 'BIGNUM'
        else:
            yield AKS(item)


def test_luke(num):
    # https://ru.wikipedia.org/wiki/Тест_простоты_Люка
    print 'Test Luke: \t\t\t',
    simples = []

    def luke(n, k):
        q = [x for x in simples if (n - 1) % x == 0]
        for i in range(k):
            a = random.randrange(2, n)
            if not (a ** (n - 1) - 1) % n == 0:
                return False
            for counter, item in enumerate(q):
                if not (a ** ((n - 1) // item) - 1) % n == 0:
                    if counter != len(q) - 1:
                        continue
                    else:
                        return True
                else:
                    break
        return True

    k = 5  # точность
    for item in num:
        simples = test_solovei(item, False)
        yield luke(item, k)


# @test_simple
def test_poklingtona(num=[2]):
    # https://ru.wikipedia.org/wiki/Критерий_Поклингтона
    print 'Test Poklington: \t',
    simples = []

    def polington(n, k):
        q = [x for x in simples if (x < (n - 1)) and ((n - 1) % x == 0) and (x > math.sqrt(n) - 1)]
        for i in range(k):
            a = random.randrange(2, n)
            if (a ** (n - 1) - 1) % n == 0:
                for item in q:
                    if gcd(n, a ** ((n - 1) // item) - 1) == 1:
                        return True
        return False

    k = 5  # точность
    for item in num:
        simples = test_solovei(item, False)
        yield polington(item, k)


def test_factor_ferma(num):
    print 'Test factor Ferma: ',

    def factor_ferma(n):
        m = trunc(sqrt(n))
        x = 1
        while True:
            B = (m + x) ** 2 - n
            a = trunc(sqrt(B))
            b = (a + 1) ** 2
            a **= 2
            if B == a or B == b:
                A = m + x
                B = sqrt(B)
                return int(A + B), int(A - B)
            x += 1
    for item in num:
        yield factor_ferma(item)


def test_dixsona(num):
    print 'Test Dixona: \t\t',

    def factor(N, B):
        answer = set()

        def isBsmooth(n, b):
            nn = n
            if n == 0:
                return [], False
            factors = []
            for i in b:
                while n % i == 0:
                    n = n // i
                    factors.append(i)
            res = 1
            for item in factors:
                res *= item
            if n == 1 and res == nn:
                d = dict()
                for i in b:
                    d[i] = 0
                for f in factors:
                    d[f] += 1
                return d, True
            return [], False

        def foo(B, x, y):
            result = 1
            for i in range(len(B)):
                result *= B[i] ** ((x[i] + y[i]) // 2)
            return result

        Bs_arrays = []
        Bsmooth = []
        BsmoothMod = []
        for b in range(int(N ** 0.5), N):
            a = b ** 2 % N
            ww1, ww2 = isBsmooth(a, B)
            if ww2:
                Bs_arrays.append(b)
                Bsmooth.append(ww1.values())
                BsmoothMod.append([x % 2 for x in ww1.values()])

        for i in range(len(BsmoothMod)):
            for j in range(i + 1, len(BsmoothMod)):
                res = xor_arrays(BsmoothMod[i], BsmoothMod[j])
                if array_equal_0(res):
                    x = Bs_arrays[i] * Bs_arrays[j] % N
                    y = foo(B, Bsmooth[i], Bsmooth[j]) % N
                    if (x - y) % N == 0 or (x + y) % N == 0:
                        continue
                    s = gcd(x + y, N)
                    if not (s, N // s) in answer:
                        answer.add((N // s, s))

        return answer

    # num = 89755
    for item in num:
        base_len = trunc(math.exp(sqrt(log(item) * log(log(item)))))
        B = test_solovei(int(round(sqrt(base_len))), False)
        if len(B) == 0:
            B = [2]
        ans = list(factor(item, B))
        if ans:
            yield ans
        else:
            yield False


def printWithTab(nn):
    if len(str(nn)) < 3:
        print nn, '\t\t',
    else:
        print nn, '\t',


def main():

    numbers = [561, 679, 99, 101, 7, 2001]
    print '\t\t\t\t\t',
    for nn in numbers:
        printWithTab(nn)
    print
    for f in test_wilson, test_ferma, test_solovei2, test_miller_rabin, test_karmaikla, test_polinom, test_luke, test_poklingtona, test_factor_ferma, test_dixsona:
        for item in f(numbers):
            print item, '\t',
        print


main()

# test_yakobi()
