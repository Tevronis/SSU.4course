# -*- coding: utf-8 -*-
from polinom import Polinom


def main():
    p1 = Polinom.ReadPolinom(4)
    p2 = Polinom.ReadPolinom(4)

    print "Сложение: " + str(p1 + p2)

    print "Деление: " + str(p1 / p2)

    print "Остаток от деления: " + str(p1 % p2)

    p3 = [Polinom(0, [])]
    Polinom.Gcd(p1, p2, p3)
    print "НОД: " + str(p3[0])

    print "Значение при x = 3: " + str(p1.CalcValueByGorner(3))

    roots = Polinom.SearchRoots(p2, -10000, 10000)
    for i in roots:
        print "Корни: " + str(i) + " "

    print

main()