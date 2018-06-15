import random
from functools import reduce
from operator import mul

import dist


class Bi(dist.Dist):
    PARAMS = ['a', 'b']

    def __init__(self, params, values):
        super().__init__(params, values)
        self.p = self.get_param_p1(float, rnd=random.random)
        assert 0 < self.p < 1
        self.n = self.get_param_p2(rng=[100, 500])
        self.normalize_values()

    def modification(self):
        result = []
        f = []
        for y in range(self.n):
            y_new = 0
            for k in range(0, y + 1):
                y_new += Bi.ncr(self.n, k) * pow(self.p, k) * pow(1 - self.p, self.n - k)
            f.append(y_new)

        for value in self.values:
            for idx, fy in enumerate(f):
                if value <= fy:
                    result.append(idx)
                    break
        return result

    @staticmethod
    def ncr(n, r):
        r = min(r, n - r)
        result = reduce(mul, range(n, n - r, -1), 1) // reduce(mul, range(1, r + 1), 1)
        return result

    @staticmethod
    def info():
        return """
bi
Биномиальное распределение (Метод обратной функции)
Аргументы: p, n (Вероятность и точность)
assert 0 < p < 1
"""