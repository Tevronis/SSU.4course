import cmath
import dist


class Ln(dist.Dist):
    PARAMS = ['a', 'b']

    def __init__(self, params, values):
        super().__init__(params, values)
        l = dist.nr.Nr(params, values)
        self.values = l.modification()
        self.a = l.a
        self.b = l.b
        assert self.a < self.b
        self.normalize_values()

    def modification(self):
        return [self.a + cmath.exp(self.b * item).real for item in self.values]

    @staticmethod
    def info():
        return """
ln
Логнормальное распределение
Аргументы: a, b
assert a < b
Используемая формула: Y = a + exp(b - Z)
"""