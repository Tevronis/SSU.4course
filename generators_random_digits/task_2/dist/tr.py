import dist


class Tr(dist.Dist):
    PARAMS = ['a', 'b']

    def __init__(self, params, values):
        super().__init__(params, values)
        self.a = self.get_low_interval()
        self.b = self.get_high_interval()
        assert self.a < self.b
        self.normalize_values()

    def modification(self):
        return [self.a + self.b * (self.values[idx] + self.values[idx + 1] - 1)
                for idx in range(0, len(self.values) - 1)]

    @staticmethod
    def info():
        return """
tr
Треугольное распределение
Аргументы: a, b
assert a < b
Используемая формула: Y = a + b(U1 + U2 -1)
"""