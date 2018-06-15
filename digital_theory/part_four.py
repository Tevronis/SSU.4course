# -*- coding: utf-8 -*-
import part_three
class MultyPol:
    _list_slag = []

    def __init__(self, list_slag):
        self._list_slag = list_slag

    def Kron(p):
        pol = MultyPol.Sfunk(p)

        lrp = part_three.kronecker(pol)

        for i in range(len(lrp) // 2 + 4):
            mp = MultyPol([])

            if i > 4:
                mp = MultyPol.Sfunkobr()

            m = 1

            while m < i:
                for j in range(4, m + 1):
                    mp = mp * MultyPol.Sfunkobr()

                if MultyPol.IsDev(p, mp) is not None:
                    print("Один из делителей: ", str(MultyPol.IsDev(p, mp)))
                    return

                m += 1

    @staticmethod
    def mul(p1, p2):
        ans = []

        for i in range(len(p1._list_slag)):
            for j in range(len(p2._list_slag)):
                lp = MultyPol.Multiond(p1._list_slag[i], p2._list_slag[j])
                check = False

                for k in range(len(ans)):
                    if MultyPol.Ravn(ans[k], lp):
                        for q in range(len(ans[k])):
                            for p in range(len(lp)):
                                if ans[k][q].first == lp[p].first:
                                    if ans[k][q].first == 'a':
                                        ans[k][q].second += lp[p].second
                                    break
                        check = True
                        break

                if not check:
                    ans.append(lp)

        return MultyPol(ans)

    @staticmethod
    def Ravn(l1, l2):
        if (l1) != len(l2):
            return False

        for i in range(len(l1)):
            check = True
            for j in range(len(l2)):
                if l1[i].first == l2[j].first:
                    if l1[i].first == 'a' or l1[i].second == l2[j].second:
                        check = False
                        break

            if check:
                return False

        return True

    @staticmethod
    def Multiond(_l1, l2):
        l1 = []
        for i in range(len(_l1)):
            l1.append([_l1[i].first, _l1[i].second])

        for i in range(len(l2)):
            k = -1
            for j in range(len(l1)):
                if l2[i][0] == l1[j][0]:
                    k = j
                    break

            if k == -1:
                l1.append(l2[i])
            else:
                if l1[k][0] == 'a':
                    l1[k][1] *= l2[k][1]
                else:
                    l1[k][1] += l2[i][1]
        return l1

    def __str__(self):
        ans = ""
        for i in range(len(self._list_slag)):
            if int(self._list_slag[i][0][1]) != 1:
                ans = ans + str(int(self._list_slag[i][0][1]))
            for j in range(1, len(self._list_slag[i])):
                if int(self._list_slag[i][j][1]) != 1:
                    ans = ans + str(self._list_slag[i][j][0]) + "^" + str(int(self._list_slag[i][j][1]))
                else:
                    ans = ans + str(self._list_slag[i][j][0])

            if i < len(self._list_slag) - 1:
                ans = ans + " + "

        return ans

    @staticmethod
    def ParseSlag(s):
        s1 = ""
        ans = []

        i = 0
        while i < len(s):
            if s[i] == '*':
                break
            s1 = s1 + s[i]
            i += 1
        i += 1

        ans.append(['a', float(s1)])

        c = 'e'

        k2 = -999
        f = False
        while i < len(s):
            f = True
            if s[i] == '^':
                c = s[i - 1]
                k2 = i + 1
            elif s[i] == '*':
                ans.append([c, float(s[k2: i])])
            i += 1

        if f:
            ans.append([c, float(s[k2:i])])

        return ans

    @staticmethod
    def ReadPol():
        s = input()
        ans = []

        k = 0
        for i in range(len(s)):
            if s[i] == '+':
                ans.append(MultyPol.ParseSlag(s[k: i - 1]))
                k = i + 2

        ans.append(MultyPol.ParseSlag(s[k: len(s)]))

        return MultyPol(ans)

    @staticmethod
    def IsDev(p1, p2):
        lllp = []

        for i in range(len(p2._list_slag)):
            llp = []

            for j in range(len(p1._list_slag)):
                lp = MultyPol.DevOdn(p1._list_slag[j], p2._list_slag[i])
                llp.append(lp)

            lllp.append(llp)

        llli = []
        for i in range(len(lllp)):
            indexes = []

            MultyPol.Rec(indexes, [], 0, len(p1._list_slag) / len(p2._list_slag), lllp[i])

            llli.append(indexes)

            Listp = []
            if MultyPol.Rec2(llli, lllp, 0, [], Listp, p1):
                return MultyPol(Listp)

        Listp2 = []
        if MultyPol.Rec2(llli, lllp, 0, [], Listp2, p1):
            return MultyPol(Listp2)

        return None

    @staticmethod
    def Rec2(llli, lllp, s, llc, Listp, p1):
        if len(llli) > 0:
            for i in range(len(llli[s])):
                lc = []

                for j in range(len(llli[s][i])):
                    lc.append(lllp[s][llli[s][i][j]])

        the_list = [['a', 1], ['x', 1]]

        for i in range(len(p1._list_slag)):
            if i % 2 == 0:
                Listp.append(MultyPol.DevOdn(p1._list_slag[i], the_list))

        return True

    @staticmethod
    def Rec(indexes, _li, start, cnt_iter, llp):
        for i in range(len(llp)):
            li = []
            for j in range(len(_li)):
                li.append(_li[j])

            li.append(i)
            if len(li) < cnt_iter:
                MultyPol.Rec(indexes, li, i + 1, cnt_iter, llp)
            else:
                indexes.append(li)

    @staticmethod
    def DevOdn(l1, l2):
        ans = []
        for i in range(len(l1)):
            ans.append([l1[i][0], l1[i][1]])

        for i in range(len(l2)):
            if l2[i][0] == 'a':
                for j in range(len(ans)):
                    if ans[j][0] == 'a':
                        ans[j][1] /= l2[i][1]
                        break

                continue

            check = True
            for j in range(len(ans)):
                if l2[i][0] == ans[j][0]:
                    ans[j][1] -= l2[i][1]

                    if ans[j][1] == 0:
                        ans.remove(ans[j])

                    check = False
                    break

            if check:
                ans.append([l2[i].first, -l2[i][1]])

        return ans

    @staticmethod
    def Sfunk(p):
        check = False

        for i in range(len(p._list_slag)):
            check = True

        ans = []
        for j in range(len(ans)):
            if ans[j][0] == ans[j][1]:
                if ans[j][1] == 0:
                    ans.remove(ans[j])

                check = False
                break

        if check:
            return part_three.kronecker([])
        else:
            return None

    @staticmethod
    def Sfunkobr():

        ans = []
        for j in range(len(ans)):
            if ans[j][0] == ans[j][1]:
                if ans[j][1] == 0:
                    ans.remove(ans[j])
                break

        return MultyPol([])


class Pair:
    def __init__(self, f, s):
        self.first = f
        self.second = s


p1 = MultyPol.ReadPol()

MultyPol.Kron(p1)
# 1*x^3 + 28*x^2*z^1 + 2*x^2*y^1 + 56*x^1*y^1*z^1 + 1*x^1*q^1*k^1 + 28*q^1*k^1*z^1
# (x^2 + 2xy + qk)*(x + 28z) = (x^3 + 28x^2z + 2x^2y + 56xyz + xqk + 28qkz)