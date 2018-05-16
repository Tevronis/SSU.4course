import math
from datetime import datetime

POLINOM = []
for num in map(int, open('CONST.dat').read().split()):
    POLINOM.append(num)


def create_keys(n):
    assert n < len(POLINOM)
    seed = datetime.now().second % 100 + 1
    polinom = POLINOM[:n]
    result = []
    start_value = seed
    KEY = n * seed
    for idx in range(n):
        KEY *= polinom[idx]
    KEY *= polinom[0] ** (start_value - 1)
    result.append((float(start_value), 0, n))
    print("SECRET KEY: ", KEY)
    for key_i in range(1, n):
        item = KEY
        for idx, val in enumerate(polinom[:n]):
            if idx != key_i:
                item //= val
        item //= n
        item //= seed
        to_set = math.log(item, polinom[key_i])
        result.append((to_set, key_i, n))

    return result


def restore_key(key):
    result = POLINOM[int(key[1])] ** key[0]
    for ip, pol in enumerate(POLINOM[:int(key[2])]):
        if ip != int(key[1]):
            result *= pol
    return int(str(int(result))[:7])


def crypt(text, key):
    secret_key = restore_key(key)
    result = []
    for item in text:
        result.append(item ^ secret_key)
    return result


def decrypt(text, key):
    secret_key = restore_key(key)
    result = []
    for item in text:
        result.append(item ^ secret_key)
    return result


def keys_mod():
    n = int(input('Сколько ключей сгенерировать?: '))
    keys = create_keys(n)
    for idx, key in enumerate(keys):
        with open('key_' + str(idx), 'w') as f:
            to_write = ' '.join(map(str, key))
            f.write(to_write)


def crypt_mod():
    file = input('Что шифруем?: ')
    key_file = input('Чьим ключом?: ')
    with open(key_file) as f:
        key = list(map(float, f.readline().split()))
    with open(file, 'rb') as f:
        text = f.read()
    text_crypt = crypt(text, key)
    with open('crypted_' + str(int(key[1])), 'w') as f:
        f.write(' '.join(map(str, text_crypt)))


def decrypt_mod():
    file = input('Какой файл расшифровываем?: ')
    key_file = input('Чьим ключом?: ')
    with open(file, 'rb') as f:
        text = list(map(int, f.read().split()))
    with open(key_file) as f:
        key = list(map(float, f.readline().split()))

    with open('file_' + str(int(key[1])), 'wb') as f:
        f.write(bytes(decrypt(text, key)))


def main():
    mod = int(input('Режим работы: 1 - создать n ключей\n2 - зашифровать одним из ключей\n3 - дешифровать одним из '
                    'ключей\n4 - просто прогон\n'))

    if mod == 1:
        keys_mod()
    if mod == 2:
        crypt_mod()
    if mod == 3:
        decrypt_mod()
    if mod == 4:
        keys_mod()
        crypt_mod()
        decrypt_mod()


if __name__ == '__main__':
    main()
