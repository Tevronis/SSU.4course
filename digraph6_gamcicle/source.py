# coding=utf-8
import networkx as nx
import matplotlib.pyplot as plt

cnt = 0
cnt2 = 220


def saveGraph(nxg, graph, w):
    global cnt
    global cnt2
    nxg.clear()
    plt.subplot(221 + cnt2 % 4)
    plt.title(str(w))
    n = len(graph)
    for i in range(n):
        for j in range(n):
            if graph[i][j] == '1':
                nxg.add_edge(cnt + i, cnt + j)

    cnt2 += 1

    nx.draw_circular(nxg, node_color='#A0CBE2', node_size=15, width=0.6, with_labels=True, edge_color='m')


def readGraph(dir):
    with open(dir) as f:
        while True:
            ans = []

            s = f.readline()
            try:
                n = (ord(s[1]) - 63)
            except:
                break
            print(s)
            adds = ""
            for i in range(2, len(s)):
                a = ord(s[i]) - 63
                numb = bin(a)[2:]
                while len(numb) % 6 != 0:
                    numb = '0' + numb
                adds += numb
            adds = adds[:n * n]
            for i in range(0, len(adds), n):
                ans.append(adds[i: i + n])
            while len(ans[-1]) < n:
                ans[-1] += '0'

            yield ans


def intoDiGraph6(s, n):
    ans = "&" + chr(n + 63)
    while s.length() % 6 != 0:
        s += "0"
    for i in range(0, len(s), 6):
        r = int(s[i: i + 6], 2) + 63
        ans += chr(r)

    return ans


def readSimpleGraph():
    n = int(input())
    result = [[0 for y in range(n)] for x in range(n)]
    for i in range(n):
        inp = input()
        for j in range(n):
            result[i][j] = int(inp[j])
    return result


def solve(graph):
    n = len(graph)
    visited = [False] * n
    path = []

    def hamilton(curr):
        path.append(curr)
        if len(path) == n:
            if graph[path[0]][path[-1]] == '1':
                return True
            else:
                path.pop()
                return False
        visited[curr] = True

        for next in range(n):
            if graph[curr][next] == '1' and not visited[next]:
                if hamilton(next):
                    return True
        visited[curr] = False
        path.pop()

        return False

    for i in range(n):
        visited = [False] * n
        path = []

        if hamilton(i) and graph[path[-1]][i] == '1':
            return path


def main():
    g = nx.DiGraph()
    for gr in readGraph("input.txt"):
        w = solve(gr)
        if w is not None:
            saveGraph(g, gr, w)
            print(w)
        print('*******************************************')

    plt.savefig("anedge.pdf")


main()
