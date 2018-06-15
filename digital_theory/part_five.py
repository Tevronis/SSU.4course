from sympy import Poly, Symbol, rem


# algorith Berlicamp for find some razlojenie na polinoms

def field(polynomial, p):
    for i in range(len(polynomial)):
        polynomial[i] = ((polynomial[i] + p) % p + p) % p
    return polynomial


def inverse(p):
    found = True
    inv = {}
    for x in range(0, p):
        if x == 0:
            inv[x] = 0
        else:
            l = 1
            while (l * x) % p != 1 and l != p:
                l += 1
            if l == p:
                found = False
            inv[x] = l
    return inv, found


def pdf(p0, p1):
    c = [p0[i] for i in range(len(p0))]
    d = [p1[i] for i in range(len(p1))]
    m = len(c) - 1
    n = len(d) - 1
    if m < n:
        return [0]
    q = [0 for i in range(0, m - n + 1)]
    for k in range(0, m - n + 1):
        q[k] = c[k] // d[0]
        for j in range(k, n + k + 1):
            c[j] -= q[k] * d[j - k]
    try:
        idx = next(x[0] for x in enumerate(c) if x[1] > 0 or x[1] < 0)
        r = [c[i] for i in range(idx, len(c))]
        return r
    except:
        return [0]


def getCoeffs(polynomial, p, n):
    coeffs = polynomial.all_coeffs()
    for i in range(len(coeffs)):
        coeffs[i] = int(coeffs[i])
        coeffs[i] = ((coeffs[i] + p) % p + p) % p
    while len(coeffs) < n:
        coeffs.insert(0, 0)
    return coeffs


def constructMatrice(polynomial, p):
    q = []
    n = len(polynomial) - 1
    for deg in range(0, n):
        x = Symbol('x')
        r = rem(x ** (p * deg), Poly.from_list(polynomial, gens=x))
        r_rev = getCoeffs(r, p, n)
        r_rev.reverse()
        r_rev[deg] -= 1
        r_rev = field(r_rev, p)
        q.append(r_rev)
    return q


def subs(q, x, str_ind, col_ind, p):
    n = len(q)
    new_q = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        new_q[i][col_ind] = ((q[i][col_ind] * x) % p + p) % p
    for j in range(n):
        for i in range(n):
            if j != col_ind:
                new_q[i][j] = (q[i][j] + new_q[i][col_ind] * q[str_ind][j]) % p
    return new_q


def nullSpace(q, p):
    n = len(q)
    r = 0
    c = [-1 for i in range(n)]
    vecs = []
    for h in range(n):
        flag = False
        for j in range(n):
            if q[h][j] != 0 and c[j] < 0:
                flag = True
                x = inv[q[h][j]]
                x = ((-x + p) % p + p) % p
                new_q = subs(q, x, h, j, p)
                c[j] = h
                q = new_q
                break
        if not flag:
            r += 1
            b = [0 for i in range(n)]
            for i in range(n):
                flag = False
                for k in range(n):
                    if c[k] == i and i > 0:
                        b[i] = q[h][k]
                        flag = True
                if flag:
                    continue
                if i == h:
                    b[i] = 1
            b.reverse()
            idx = next(x[0] for x in enumerate(b) if x[1] > 0)
            new_b = [b[i] for i in range(idx, len(b))]
            vecs.append(new_b)
    return vecs, r


ans = []
cnt = 1


def berlekamp(polynomial, p, inv):
    def normalize(polynomial, inv_num, p):
        for i in range(len(polynomial)):
            polynomial[i] = (polynomial[i] * inv_num) % p
        return polynomial

    def extGcd(p0, p1, p):
        from numpy import poly1d
        while poly1d(p1) != poly1d([0.]):
            rem = pdf(p0, p1)
            rem = field(rem, p)
            rem = normalize(rem, inv[rem[0]], p)
            p0 = p1
            p1 = rem
        return p0

    def findMulti(polynomial, b, r, idx, p):
        global cnt
        if cnt == r:
            ans.append(polynomial)
            return
        if idx == r:
            ans.append(polynomial)
            return
        last_ind = len(b[idx]) - 1
        x = b[idx][last_ind]
        multipliers = []
        for s in range(0, p):
            b[idx][last_ind] -= s
            b[idx] = field(b[idx], p)
            res = extGcd(polynomial, b[idx], p)
            if len(res) > 1:
                multiply = [res[i] for i in range(len(res))]
                multipliers.append(multiply)
            b[idx][last_ind] = x
        if len(multipliers) == 0:
            ans.append(polynomial)
            return
        cnt += len(multipliers) - 1
        for x in multipliers:
            findMulti(x, b, r, idx + 1, p)

    polynomial = normalize(polynomial, inv[polynomial[0]], p)
    q = constructMatrice(polynomial, p)
    b, r = nullSpace(q, p)
    if r == 1:
        print(polynomial)
        return
    findMulti(polynomial, b, r, 1, p)
    for x in ans:
        print(x)


polynomial = list(map(int, input().split()))
p = int(input())

inv, found = inverse(p)

if not found:
    print("No find reverse number for some numbers in field {}".format(p))
else:
    berlekamp(polynomial, p, inv)

# 2 4 8 5 3
# 5
