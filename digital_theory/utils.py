from fractions import gcd


def xor_arrays(a, b):
    if len(a) != len(b):
        print 'bad xor'
        exit()
    result = []
    for i in range(len(a)):
        result.append(a[i] ^ b[i])
    return result


def powModN(x, y, n):
    result = 1
    for i in range(y):
        result = (result * x) % n
    return result


def array_equal_0(x):
    for i in x:
        if i != 0:
            return False
    return True


def array_multi(arr):
    result = 1
    for item in arr:
        result *= item
    return result


def yakobi(a, b):
    if gcd(a, b) != 1:
        return 0
    r = 1

    if a < 0:
        a = -a
        if b % 4 == 3:
            r = -r

    def stuff(a, b, r):
        t = 0
        while a % 2 == 0:
            t += 1
            a /= 2
        if t % 2 == 1:
            if (b % 8) == 3 or (b % 8) == 5:
                r = -r

        if (a % 4) == (b % 4) == 3:
            r = -r
        c = a
        a = b % c
        b = c
        return a, b, r

    a, b, r = stuff(a, b, r)
    while a != 0:
        a, b, r = stuff(a, b, r)

    return r
