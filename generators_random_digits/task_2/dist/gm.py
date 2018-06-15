import cmath
from functools import reduce

import dist


class Gm(dist.Dist):
    PARAMS = ['a', 'b', 'k']

    def __init__(self, params, values):
        super().__init__(params, values)
        self.a = self.get_low_interval()
        self.b = self.get_high_interval()
        assert self.a < self.b
        self.k = self.get_gamma_k()
        assert self.k > 0, 'Значение k должно быть положительно'
        self.normalize_values()

    def modification(self):
        result = []
        for idx in range(0, len(self.values) - self.k):
            iln = reduce(lambda x, y: x * y, self.values[idx: idx + self.k])
            item = self.a - self.b * cmath.log(iln).real
            result.append(item)
        return result

    def get_gamma_k(self):
        if self.params.k is None:
            result = 1  # default value
        else:
            result = int(self.params.k)
        return result

    @staticmethod
    def info():
        return """
gm
Гамма-распределение
Аргументы: a, b, k
assert a < b
assert k > 0
Используемая формула: Y = a - b*ln((1-U1)*(1-U2)..(1-Uk))
"""