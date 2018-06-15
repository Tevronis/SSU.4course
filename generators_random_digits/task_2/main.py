# coding=utf-8
import argparse
import random
import sys

from dist import st, tr, ex, nr, gm, ln, ls, bi

DEFAULT_LEN = 10000

DIST_DICT = {'st': st.St, 'tr': tr.Tr, 'ex': ex.Ex, 'nr': nr.Nr, 'gm': gm.Gm,
             'ln': ln.Ln, 'ls': ls.Ls, 'bi': bi.Bi}


def handle_gen(args):
    if '--d' in args:
        gen_name = args[args.index('--d') + 1]
        print('Выбрано распределение {}'.format(gen_name) + '\n')
        return gen_name

    gen_name = random.choice(list(DIST_DICT.keys()))
    print('Случайно выбрано распределение {}'.format(gen_name) + '\n')
    return gen_name


def init_parser(parser, gen_name):
    params = DIST_DICT[gen_name].PARAMS

    for param_name in params:
        parser.add_argument('--{}'.format(param_name), type=str)


def handle_windows_style():
    args = sys.argv[1:]
    for idx, arg in enumerate(args):
        if '/' in arg:
            arg = arg.replace('/', '--')
            if ':' in arg:
                args.insert(idx + 1, arg[arg.index(':') + 1:])
                arg = arg[:arg.index(':')]
            args[idx] = arg

    return args


def parse_args():
    args = handle_windows_style()
    gen_name = handle_gen(args)

    parser = argparse.ArgumentParser()
    parser.add_argument('--d', type=str, default='st')
    parser.add_argument('--fi', type=str, default='input')
    parser.add_argument('--fo', type=str, default='rnd.dat')
    parser.add_argument('--h', type=str)
    parser.add_argument('--gui', action='store_true', default=True)

    init_parser(parser, gen_name)

    return gen_name, parser.parse_args(args)


def hist(items, name):
    try:
        import matplotlib.pyplot as plt
        plt.hist(items, 50)
        plt.title(name)
        plt.grid(True)
        plt.show()
    except:
        pass


def main():
    name, parser = parse_args()
    print(name, parser)
    in_file = open(parser.fi, 'r')
    out_file = open(parser.fo, 'w')
    inread = list(map(int, in_file.read().split()))

    dist = DIST_DICT[name]
    if not (parser.h is None):
        print(dist.info())
        return
    dist = dist(parser, inread)

    items = dist.modification()

    for idx, item in enumerate(items):
        out_file.write(str(item) + '\n')

    if parser.gui:
        hist(items, name)

    out_file.close()


if __name__ == '__main__':
    main()
