import random

for i in range(100):
    with open('CONST.dat', 'w') as f:
        f.write(random.randint(2, 40))
