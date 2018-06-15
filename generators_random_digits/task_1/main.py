# coding=utf-8
import argparse
import random
import sys

from generators import add, bbs, fparam, lc, lfsr, nfsr, rc4, rsa, mt

DEFAULT_LEN = 1000

GENS_DICT = {'lc': lc.Lc, 'add': add.Add, '5p': fparam.FParam, 'lfsr': lfsr.LFSR, 'nfsr': nfsr.NFSR,
             'mt': mt.Mt, 'rc4': rc4.RC4, 'rsa': rsa.RSAG, 'bbs': bbs.BBS}


def handle_gen(args):
    if '--g' in args:
        gen_name = args[args.index('--g') + 1]
        print('Выбран генератор {}'.format(gen_name) + '\n')
        return gen_name
    gen_name = random.choice(list(GENS_DICT.keys()))
    print('Случайно выбран генератор {}'.format(gen_name) + '\n')
    return gen_name


def init_parser(parser, gen_name):
    params = GENS_DICT[gen_name].PARAMS

    for param_name in params:
        parser.add_argument('--{}'.format(param_name), type=int)


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
    parser.add_argument('--g', type=str)
    parser.add_argument('--i', type=int, default=None)
    parser.add_argument('--n', type=int, default=DEFAULT_LEN)
    parser.add_argument('--f', type=str, default='rnd.dat')
    parser.add_argument('--h', type=str)
    parser.add_argument('--gui', type=bool, default=True)

    init_parser(parser, gen_name)

    return gen_name, parser.parse_args(args)


def plot(values):
    try:
        import matplotlib.pyplot as plt
        plt.figure()
        for idx, item in enumerate(values):
            plt.scatter(idx, item)
        plt.show()
    except:
        pass


def save_to_file(file_name, values):
    print('Значения сохранены в файл {}'.format(file_name))
    file = open(file_name, 'w')
    for item in values:
        file.write(str(item) + ' ')
    file.close()


def main():
    name, parser = parse_args()
    print(name, parser)
    n = parser.n

    generator = GENS_DICT[name]
    if not (parser.h is None):
        print(generator.info())
        return
    generator = generator(parser)

    values = []
    for idx in range(n):
        values.append(next(generator))

    save_to_file(parser.f, values)

    if parser.gui:
        plot(values)


main()

# регистр сдвига с обр лин связью 41
# пятипарам метод 45
# нелинейная комбинация РСЛОС 48
# вихрь мерсена 56
# алгоритм RC4 82
# RSA 83
# алгоритм ББШ 85
