import dist


class St(dist.Dist):
    PARAMS = ['a', 'b']

    def __init__(self, params, values):
        super().__init__(params, values)
        self.a = self.get_low_interval()
        self.b = self.get_high_interval()
        assert self.a < self.b
        self.normalize_values()

    def modification(self):
        return [self.b * item + self.a for item in self.values]

    @staticmethod
    def info():
        return """
st
Стандартное распределение
Аргументы: a, b
assert a < b
"""