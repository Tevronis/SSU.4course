import random
import sys

count = 100
if len(sys.argv) > 1:
    count = int(sys.argv[1])

to_write = ''
for i in range(100):
    to_write += str(random.randint(2, 40)) + ' '
with open('CONST.dat', 'w') as f:
    f.write(to_write)
