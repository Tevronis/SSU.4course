class Generator:
    PARAMS = ''

    def gen(self):
        pass

    def __next__(self):
        return self.gen()

    def __validate(self):
        pass

    @staticmethod
    def info():
        return ''
