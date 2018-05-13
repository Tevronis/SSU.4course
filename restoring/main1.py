import os
from time import sleep, time

import psutil

FILE = 'main2.exe'
CUR_FILE = 'main1.exe'


def timeout():
    sleep(7)
    print("Подождал 7 сек")
    return True


def write_data(file_name, data1, data2, name1, name2):
    print('Созраняем данные с разделителем: {} {} в файл {}'.format(name1, name2, file_name))
    with open(file_name, 'bw') as f:
        f.write(data1)  # first file

        towrite = '1[]1'.encode('utf-8') + name1.encode('utf-8')
        f.write(bytes(towrite))
        f.write(data1)  # second file

        towrite = '1[]2'.encode('utf-8') + name2.encode('utf-8')
        f.write(bytes(towrite))
        f.write(data2)  # third file


def stick_files(file1, file2, FILENAME_STICK):
    with open(file1, 'rb') as f:
        file = f.read()

    with open(file2, 'rb') as f:
        file_add = f.read()
    print(file1[-5])
    print(file2[-5])
    write_data(FILENAME_STICK, file, file_add, file1[-5], file2[-5])


def unstick_files(FILENAME_STICK_):
    print('Start unstick files {}'.format(FILENAME_STICK_))
    with open(FILENAME_STICK_, 'rb') as f:
        stick = f.read()

    eof1 = stick.find(bytes('1[]1'.encode('utf-8')))
    eof2 = stick.find(bytes('1[]2'.encode('utf-8')))
    file_name1 = 'temp' + chr(int(stick[eof1 + 4])) + '.exe'
    file_name2 = 'temp' + chr(int(stick[eof2 + 4])) + '.exe'
    for idx in range(5):
        print(chr(int(stick[eof1 + idx])), end='')
    print()
    print(file_name1)
    print(file_name2)
    print('index: ' + str(eof1))
    print('index: ' + str(eof2))

    # print('start of file1: {}'.format(chr(int(stick[eof1 + 5]))))
    # print('start of file2: {}'.format(chr(int(stick[eof2 + 5]))))
    file1 = stick[eof1+5:eof2]
    file2 = stick[eof2+5:]

    with open(file_name1, 'wb') as f:
        f.write(file1)
    with open(file_name2, 'wb') as f:
        f.write(file2)

    stick_files(file_name2, file_name1, FILE)
    os.remove(file_name1)
    os.remove(file_name2)


def exist_process():
    start_time = time()
    for num, proc in enumerate(psutil.process_iter()):
        if proc.name() == FILE:
            print("Время на поиск процесса {}".format(time() - start_time))
            return True
    print("Время на поиск процесса {}".format(time() - start_time))
    return False


def exist_file():
    print('Удален ли файл? {}'.format(FILE))
    return os.path.exists(FILE)


def restore_process():
    # proc = subprocess.Popen(FILE, shell=True, stdout=subprocess.PIPE)
    # out = proc.stdout.readlines()
    print('Пытаемся запустить процесс {}'.format(FILE))
    # os.system(FILE)
    os.startfile(FILE)
    #exec('{}'.format(FILE))
    print("Процесс {} восстановлен".format(FILE))


def restore_file():
    file = __file__[:-3] + '.exe'
    file = CUR_FILE
    print('Пытаемся восстановить {}'.format(FILE))
    unstick_files(file)
    print("Файл {} восстановлен".format(FILE))


def main():
    print("Start find {}".format(FILE))

    while timeout():
        if not exist_file():
            print("Файл {} удален".format(FILE))
            restore_file()
        if not exist_process():
            print("Процесс {} удален".format(FILE))
            restore_process()


if __name__ == '__main__':
    main()
