import hashlib
import os

import properties


def md5(path):
    if os.path.isdir(path):
        return 0
    try:
        hash_md5 = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except PermissionError:
        print('Permission error to file: {}'.format(path))
        return 0


class Sysfile:
    def __init__(self, path):
        self.name = path.split('\\')[-1]
        self.abspath = path
        if os.path.isdir(path):
            self.isdir = 1
        else:
            self.isdir = 0
        self.dir = path.split('\\')[:-1]
        self.hash = md5(path)
        self.size = os.path.getsize(path)
        self.mod = os.path.getmtime(path)
        self.creation = os.path.getctime(path)
        self.open = os.path.getatime(path)

    def comp(self, other):
        name = self.abspath
        args = ['У файла {} были изменены параметры:'.format(name)]
        if self.hash != other['hash']:
            args.append('hash,')
        if self.size != other['f_size']:
            args.append('size,')
        if self.mod != other['last_modification']:
            args.append('modification date,')
        if self.creation != other['creation']:
            args.append('creation date,')

        if len(args) > 1:
            for item in args:
                print(item, end=' ')
            print()

    def serialization(self):
        jss = properties.js
        for name in self.dir:
            jss = jss[name]['subfiles']
        jss[self.name] = {'isdir': self.isdir, 'f_size': self.size, 'hash': self.hash, 'last_modification': self.mod,
                          'creation': self.creation, 'last_open': self.open, 'subfiles': {}}
