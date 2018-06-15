import random


class Dist:

    def __init__(self, params, values):
        self.params = params
        self.values = values
        self.a = None
        self.b = None

    def get_param_p1(self, type_=int, rng=None, rnd=random.randint):
        if rng is None:
            rng = [-20, 20]
        if self.params.a is None:
            if type_ == int:
                self.a = rnd(*rng)
            else:
                self.a = rnd()
        else:
            self.a = type_(self.params.a)
        print("Параметр p1 выбран: {}".format(self.a))
        return self.a

    def get_param_p2(self, type_=int, rng=None):
        if rng is None:
            rng = [1, 5]
        if self.params.b is None:
            self.b = random.randint(*rng)
        else:
            self.b = type_(self.params.b)
        print("Параметр p2 выбран: {}".format(self.b))
        return self.b

    def get_low_interval(self, type_=int):
        if self.params.a is None:
            self.a = random.randint(1, 500)
        else:
            self.a = type_(self.params.a)
        print("Параметр a: {}".format(self.a))
        return self.a

    def get_high_interval(self, type_=int):
        if self.params.b is None:
            self.b = random.randint(500, 1000)
        else:
            self.b = type_(self.params.b)
        print("Параметр b: {}".format(self.b))
        return self.b

    def normalize_values(self):
        self.values = [item / (max(self.values) + 1) for item in self.values]

    @staticmethod
    def info(self):
        pass