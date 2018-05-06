import os
import shutil

import pefile

FILENAME_IN = 'test1.exe'
FILENAME_ADD = 'test2.exe'
FILENAME_STICK = 'prog1.exe'


def write_data(file_name, data1, data2, name1, name2):
    with open(file_name, 'bw') as f:
        f.write(data1)  # first file

        towrite = 'eof1'.encode('utf-8') + name1.encode('utf-8')
        f.write(bytes(towrite))
        f.write(data1)  # second file

        towrite = 'eof2'.encode('utf-8') + name2.encode('utf-8')
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
    with open(FILENAME_STICK_, 'rb') as f:
        stick = f.read()

    eof1 = stick.find(bytes('eof1'.encode('utf-8')))
    eof2 = stick.find(bytes('eof2'.encode('utf-8')))
    file_name1 = 'temp' + chr(int(stick[eof1 + 4])) + '.exe'
    file_name2 = 'prog' + chr(int(stick[eof2 + 4])) + '.exe'
    print(file_name1)
    print(file_name2)
    print('index eof1: ' + str(eof1))
    print('index eof2: ' + str(eof2))

    file1 = stick[eof1+5:eof2]
    file2 = stick[eof2+5:]

    with open(file_name1, 'wb') as f:
        f.write(file1)
    with open(file_name2, 'wb') as f:
        f.write(file2)

    stick_files(file_name2, file_name1, file_name2)
    os.remove(file_name1)


def main():
    # stick_files(FILENAME_IN, FILENAME_ADD, FILENAME_STICK)

    unstick_files(FILENAME_STICK)


if __name__ == '__main__':
    main()
