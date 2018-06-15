import dist
import cmath


class Nr(dist.Dist):
    PARAMS = ['a', 'b']  # nu && sigma

    def __init__(self, params, values):
        super().__init__(params, values)
        self.a = self.get_param_p1()
        self.b = self.get_param_p2()
        assert self.a < self.b
        self.normalize_values()

    def modification(self):
        result = []
        f = lambda U1, U2: self.a + self.b * cmath.sqrt(-2 * cmath.log(1 - U1)) * cmath.cos(2 * cmath.pi * U2)
        s = lambda U1, U2: self.a + self.b * cmath.sqrt(-2 * cmath.log(1 - U1)) * cmath.sin(2 * cmath.pi * U2)
        for idx in range(0, len(self.values), 2):
            result.append(f(self.values[idx], self.values[idx + 1]).real)
            result.append(s(self.values[idx], self.values[idx + 1]).real)
        return result

    @staticmethod
    def info():
        return """
nr
Нормальное распределение (Метод Бокса-Мюллера)
Аргументы: a, b
assert a < b
"""