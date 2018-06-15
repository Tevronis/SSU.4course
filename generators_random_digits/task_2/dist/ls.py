import cmath
import dist


class Ls(dist.Dist):
    PARAMS = ['a', 'b']

    def __init__(self, params, values):
        super().__init__(params, values)
        self.a = self.get_low_interval()
        self.b = self.get_high_interval()
        assert self.a < self.b
        self.normalize_values()

    def modification(self):
        return [self.a + self.b * cmath.log(item / (1 - item)).real for item in self.values]

    @staticmethod
    def info():
        return """
ls
Логистическое распределение
Аргументы: a, b
assert a < b
Используемая формула: Y = a + b * ln(U / (1 - U))
"""