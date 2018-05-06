import os
import sys

import psutil
import subprocess
import traceback
import pefile
from time import sleep, time

FILE = 'prog_1.exe'


def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    else:
        return os.path.join(os.path.abspath("."), relative)


def timeout():
    sleep(3)
    print("Подождал 3 сек")
    return True


def exist_process():
    start_time = time()
    for num, proc in enumerate(psutil.process_iter()):
        if proc.name() == FILE:
            print("Время на поиск процесса {}".format(time() - start_time))
            return True
    print("Время на поиск процесса {}".format(time() - start_time))
    return False


def exist_file():
    return os.path.exists(FILE)


def restore_process():
    proc = subprocess.Popen(FILE, shell=True, stdout=subprocess.PIPE)
    # out = proc.stdout.readlines()
    # os.system(FILE)
    print("Процесс {} восстановлен".format(FILE))


def restore_file():
    print("Файл {} восстановлен".format(FILE))


def main():
    print("Start")
    try:
        os.system('start {}'.format(resource_path("tmp.exe")))
        #with open(resource_path("1.txt")) as f:
        #    print(f.read())
    except:
        traceback.print_exc()
    while timeout():
        if not exist_file():
            print("Файл {} удален".format(FILE))
            restore_file()
        if not exist_process():
            print("Процесс {} удален".format(FILE))
            restore_process()


if __name__ == '__main__':
    main()
