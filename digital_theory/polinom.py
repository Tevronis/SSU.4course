# -*- coding: utf-8 -*-

class Polinom:
    def __init__(self, max_deg, coefficients, over_field=False, module=1):
        self._over_field = over_field
        self._coefficients = coefficients
        if over_field:
            for i in range(len(coefficients)):
                self._coefficients[i] = self._coefficients[i] % module

        self._max_degree = max_deg
        self._module = module

    def __add__(self, p2):
        if self._max_degree < p2._max_degree:
            self, p2 = p2, self

        coefficients = []
        for i in self._coefficients:
            coefficients.append(i)

        for i in range(len(p2._coefficients)):
            if self._over_field:
                coefficients[i] = (coefficients[i] + p2._coefficients[i]) % self._module
            else:
                coefficients[i] = coefficients[i] + p2._coefficients[i]

        return Polinom(self._max_degree, coefficients)

    def __div__(self, divider):
        q = []
        c = []

        for i in self._coefficients:
            c.append(i)
        for i in range(self._max_degree - divider._max_degree + 1):
            q.append(0)

        for k in range(self._max_degree - divider._max_degree, 0, -1):
            if self._over_field:
                q[k] = (c[k + divider._max_degree] / divider._coefficients[divider._max_degree]) % self._module
            else:
                q[k] = c[k + divider._max_degree] / divider._coefficients[divider._max_degree]

            for i in range(k + divider._max_degree - 1, k, -1):
                if self._over_field:
                    c[i] = (c[i] - q[k] * divider._coefficients[i - k]) % self._module
                else:
                    c[i] -= q[k] * divider._coefficients[i - k]

        return Polinom(self._max_degree - divider._max_degree + 1, q)

    def __mod__(self, divider):
        q = []
        c = []

        for i in self._coefficients:
            c.append(i)
        for i in range(self._max_degree - divider._max_degree + 1):
            q.append(0)

        for k in range(self._max_degree - divider._max_degree, 0, -1):
            if self._over_field:
                q[k] = (c[k + divider._max_degree] / divider._coefficients[divider._max_degree]) % self._module
            else:
                q[k] = c[k + divider._max_degree] / divider._coefficients[divider._max_degree]

            for i in range(k + divider._max_degree - 1, k, -1):
                if self._over_field:
                    c[i] = (c[i] - q[k] * divider._coefficients[i - k]) % self._module
                else:
                    c[i] -= q[k] * divider._coefficients[i - k]

        ans = []

        for i in range(divider._max_degree):
            ans.append(c[i])
        while len(ans) > 0 and ans[len(ans) - 1] == 0:
            ans.pop()

        return Polinom(len(ans) - 1, ans)

    @staticmethod
    def Gcd(pol1, pol2, res):
        ost = pol2
        val1 = pol1._max_degree
        val2 = pol2._max_degree
        l1 = []
        for i in pol1._coefficients:
            l1.append(i)
        l2 = []
        for i in pol2._coefficients:
            l2.append(i)
        l1.reverse()
        l2.reverse()

        p1 = Polinom(val1, l1)
        p2 = Polinom(val2, l2)

        if p1._max_degree < p2._max_degree:
            p1, p2 = p2, p1

        ostat = p1 % p2

        check = False
        for i in range(len(ostat._coefficients)):
            if ostat._coefficients[i] != 0:
                check = True
                break

        if not check:
            res[0] = ost
            return
        else:
            Polinom.Gcd(p2, ostat, res)

    def __str__(self):
        if len(self._coefficients) == 0:
            return ""
        elif len(self._coefficients) == 1:
            return str(self._coefficients[0])

        ans = ""
        if self._coefficients[-1] < 0:
            ans = "-"

        ans = ans + str(abs(self._coefficients[len(self._coefficients) - 1])) + "x^" + str(len(self._coefficients) - 1)
        for i in range(len(self._coefficients) - 2, 0, -1):
            if self._coefficients[i] != 0:
                if self._coefficients[i] < 0:
                    ans = ans + " - "
                else:
                    ans = ans + " + "
                ans = ans + str(abs(self._coefficients[i])) + "x^" + str(i);

        if self._coefficients[0] != 0:
            if self._coefficients[0] < 0:
                ans = ans + " - " + str(abs(self._coefficients[0]))
            else:
                ans = ans + " + " + str(abs(self._coefficients[0]))
        return ans

    @staticmethod
    def ReadPolinom(module=-1):
        degree = int(input())

        coeffs = map(int, (raw_input().split()))

        coeffs.reverse()

        if module == -1:
            return Polinom(degree, coeffs)
        else:
            return Polinom(degree, coeffs, True, module)

    def CalcValueByGorner(self, x):
        b = []
        for i in range(len(self._coefficients)):
            b.append(0)

        b[len(self._coefficients) - 1] = self._coefficients[-1]
        for i in range(len(self._coefficients) - 2, 0, -1):
            b[i] = self._coefficients[i] + b[i + 1] * x

        return b[0]

    @staticmethod
    def SearchRoots(p, start=-1, end=-1):
        if p._over_field:
            start = -p._module + 1
            end = p._module

        ans = []
        for i in range(start, end):
            if p.CalcValueByGorner(i) == 0:
                ans.append(i)

        return ans
