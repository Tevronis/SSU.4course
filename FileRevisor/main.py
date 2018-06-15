import json
import os
import sys
#
from sysfile import Sysfile
import properties
from utils import disable_file_system_redirection

js_c = None


def open_file(file):
    with open(file, 'r') as file:
        properties.js = json.load(file)


def close_file(file):
    with open(file, 'w') as file:
        json.dump(properties.js, file)


def dfs(path):
    if os.path.isfile(path):
        file = Sysfile(path)
        file.serialization()
    elif os.path.isdir(path):
        if properties.path != path:
            file = Sysfile(path)
            file.serialization()
        for item in os.listdir(path):
            try:
                dfs(path + '\\' + item)
            except:
                continue


def create_default_json(path, dump):
    w = {}
    ww = path.split('\\')
    for idx, name in enumerate(path.split('\\')[::-1]):
        p = []
        for i in range(len(ww) - idx):
            p.append(ww[i])
        for i in range(len(p)):
            if len(p) == 1:
                p[i] += '\\'
        n_path = '\\'.join(map(str, p))
        s = Sysfile(n_path)
        w = {name: {"isdir": s.isdir, "f_size": s.size, "hash": s.hash, "last_modification": s.mod,
                    "creation": s.creation, "last_open": s.open,
                    "subfiles": w}}
    with open(dump, 'w') as file:
        file.write(json.dumps(w))


def compare(path):
    if os.path.isfile(path):
        pass
    elif os.path.isdir(path):
        try:
            on_disk = os.listdir(path)
        except PermissionError:
            print("Permission error to file: {} ".format(path))
            return
        js = js_c
        for name in path.split('\\'):
            js = js[name]['subfiles']
        on_dump = js

        for name in on_disk:
            if not (name in on_dump):
                print('Появился новый файл: ' + path + '\\' + name)
            else:
                s = Sysfile(path + '\\' + name)
                s.comp(on_dump[name])
                try:
                    compare(path + '\\' + name)
                except:
                    continue

        for name in on_dump:
            if not (name in on_disk):
                print('Был удален файл: ' + path + '\\' + name)


def main():
    print(sys.argv[1])
    while True:
        mod = input('Создание слепка или сравнение [1/2]: ')
        dump = input('Введите название слепка: ')
        if mod == '1':
            create_default_json(sys.argv[1], dump)
            open_file(dump)
            with disable_file_system_redirection():
                dfs(sys.argv[1])
            close_file(dump)
            break
        elif mod == '2':
            with open(dump, 'r') as file:
                global js_c
                js_c = json.load(file)
            with disable_file_system_redirection():
                compare(sys.argv[1])
            break


main()
