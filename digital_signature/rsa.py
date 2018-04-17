# coding=utf-8
from fractions import gcd

import sympy


class RSA:
    def __init__(self, length):
        self.p, self.q = self.__generatePrime(length)
        self.n = self.p * self.q
        self.f = (self.p - 1) * (self.q - 1)
        self.e = self.__generateE()
        self.d = self.__generateD()

    def getKeys(self):
        return (self.e, self.n), (self.d, self.n)

    @staticmethod
    def __encrypt_symbol(m, open_key):
        return pow(m, open_key[0], open_key[1])

    @staticmethod
    def __decrypt_symbol(c, secret_key):
        return pow(c, secret_key[0], secret_key[1])

    @staticmethod
    def encrypt(text, open_key):
        print("encrypt")
        result = []
        block = ""
        for symbol in text:
            sym = str(int(symbol) + 100)
            if int(block + sym) < open_key[1]:
                block += sym
            else:
                item = RSA.__encrypt_symbol(int(block), open_key)
                result.append(item)
                block = sym
        else:
            item = RSA.__encrypt_symbol(int(block), open_key)
            result.append(item)

        return ':'.join(map(str, result))

    @staticmethod
    def decrypt(crypt, secret_key):
        print("decrypt")
        crypt = crypt.split(":")
        ans = []
        for block in crypt:
            item = RSA.__decrypt_symbol(int(block), secret_key)
            for c in range(0, len(str(item)), 3):
                ans.append(int(str(item)[c:c + 3]) - 100)
        return ans

    def __generatePrime(self, length):
        print("generate q, p")
        a = sympy.randprime(2 ** (length - 1), 2 ** length)
        b = sympy.randprime(2 ** (length - 1), 2 ** length)
        return a, b

    def __generateE(self):
        print("generate e")
        # 17 257 65537
        result = 3
        for num in sympy.primerange(2, self.f):
            if gcd(num, self.f) == 1:
                result = num
                break
        return result

    def __generateD(self):
        print("generate d with f: {0} e: {1}".format(self.f, self.e))

        def gcd2(a, b):
            if a == 0:
                x = 0
                y = 1
                return x, y, b

            x1, y1, d = gcd2(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return x, y, d

        d, y, g = gcd2(self.e, self.f)
        d = (d % self.f + self.f) % self.f
        print(d)
        return d
