import argparse
import sys

import rsa

FILENAME_IN = 'test.jpg'


def init_vars():
    parser = argparse.ArgumentParser()
    parser.add_argument('-fin', nargs='?', default=FILENAME_IN)

    return parser.parse_args(sys.argv[1:])


def main():
    args = init_vars()
    dir = args.fin
    with open(dir, 'rb') as f:
        file = f.read()
    r = rsa.RSA(100)
    # print(list(map(int, file)))
    key_o, key_s = r.getKeys()
    cr = r.encrypt(file, key_s)
    with open(dir + '.crypt', 'w') as f:
        f.write(cr)

    with open(dir + '.crypt', 'r') as f:
        file = f.read()

    with open('decrypt_' + dir, 'bw') as f:
        to_write = r.decrypt(file, key_o)
        # print(to_write)
        to_write = bytes(to_write)
        f.write(to_write)


if __name__ == '__main__':
    main()
