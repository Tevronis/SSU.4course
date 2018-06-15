# -*- coding: utf-8 -*-

import collections
import cmath
from functools import cmp_to_key

from utils import byteToChar, charToByte, node

chastota = collections.defaultdict(int)
dlina_text = 0

table = {}
table_decode = {}


def cmp(x, y):
    if x == y:
        return 0
    if chastota[x] == chastota[y]:
        return 1 if x < y else -1
    return 1 if chastota[x] < chastota[y] else -1


def fano():
    def fanoCreateTable(s, code):
        if len(s) == 1:
            table[s] = code
            table_decode[code] = s
            return
        weight = 0
        for item in s:
            weight += chastota[item]
        left = ""
        right = ""
        c_left = 0
        c_right = weight
        for i, item in enumerate(s):
            if c_left + chastota[item] < c_right - chastota[item]:
                c_left += chastota[item]
                c_right -= chastota[item]
                left += item
            elif c_right - c_left > c_left + chastota[item] - c_right + chastota[item]:
                left += item
                break
        for item in s:
            if item not in left:
                right += item
        fanoCreateTable(left, code + '0')
        fanoCreateTable(right, code + '1')

    alph = [x for x in chastota.keys()]
    alph = sorted(alph, key=cmp_to_key(cmp))
    fanoCreateTable(alph, '')


nodes = []


def haffman(nodes):
    def haffmanCreateTable(nodes):
        if len(nodes) == 1:
            return nodes[0]

        nodes = sorted(nodes, key=cmp_to_key(node.cmp))

        n1 = nodes[-1]
        nodes.pop()
        n2 = nodes[-1]
        nodes.pop()

        n3 = node(None, n1.x + n2.x, n1, n2)
        for item in nodes:
            print(item.x, end=' ')
        print()
        nodes.append(n3)
        return haffmanCreateTable(nodes)

    def dfs(current, code):
        if current.left is None or current.right is None:
            sett = ''
            for i in code:
                sett += str(i)
            table[current.ch] = sett
            table_decode[sett] = current.ch
            return
        code.append(0)
        dfs(current.left, code)
        code[-1] = 1
        dfs(current.right, code)
        code.pop()

    alph = [x for x in chastota.keys()]
    alph = sorted(alph, key=cmp_to_key(cmp))
    for item in alph:
        nodes.append(node(item, chastota[item], None, None))
    root = haffmanCreateTable(nodes)

    code = []
    dfs(root, code)

    for k, v in table.items():
        print(k, v)


def shanon():
    global dlina_text
    abs_chast = {k: v / dlina_text for k, v in chastota.items()}
    nodes = [node(ch, fr) for ch, fr in abs_chast.items()]
    nodes = sorted(nodes, key=cmp_to_key(node.cmp_rev))
    s = 0

    for item in nodes:
        code = ''
        e = cmath.log(item.x) / cmath.log(2)
        ll = -round(e.real - 0.5)

        w = s
        for i in range(ll):
            w *= 2
            if w >= 1:
                code += '1'
                w -= 1
            else:
                code += '0'
        table[item.ch] = code
        table_decode[code] = item.ch
        s += item.x
        # print(code)


def main():
    global dlina_text
    text = ''
    in_file = open('input.txt', encoding='utf-8')
    for line in in_file:
        for l in line:
            chastota[l] += 1
            dlina_text += 1
            text += l

    # fano()
    # haffman(nodes)
    shanon()

    out_file = open("output.txt", 'w', encoding='utf-8')
    mas = ''
    mos = ''
    for l in text:
        mas += table[l]
        mos += table[l]
        if len(mas) >= 8:
            out_file.write(byteToChar(mas[:8]))
            mas = mas[8:]
    while len(mas) != 8:
        mas += '0'
        if len(mas) == 8:
            out_file.write(byteToChar(mas))

    # decode:
    print('decode:')
    out_file.close()
    in_file = open('output.txt', encoding='utf-8')
    out_file = open('decode.txt', 'w', encoding='utf-8')

    mas = ''
    for line in in_file:
        for l in line:
            mas += charToByte(l)
    e = ''
    for i in mos:
        e += i
        if e in table_decode:
            out_file.write(table_decode[e])
            e = ''


main()
