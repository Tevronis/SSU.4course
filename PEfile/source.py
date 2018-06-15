import os
import pefile
import json

file = open('dlls.json')
file2 = open('dlls2.json')
json_o = ''
json_p = ''
for line in file:
    json_o += line
for line in file2:
    json_p += line
a = json.loads(json_o)
b = json.loads(json_p)
dlls = {}
dlls2 = {}

for item in b:
    lis = []
    for i in b[item]:
        lis.append(i)
    dlls[item] = lis

for item in a:
    lis = []
    for i in a[item]:
        lis.append(i['name'])
    dlls[item] = lis

outfile = open('out.txt', 'w')


def getNameDLL(x):
    l = len(str(x))
    result = str(x)[2:l - 1]
    return result


def walk(dir):
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):

            outfile.write(path + '\n')
            m = ['exe', 'EXE']
            if not path.split('.')[-1] in m:
                continue
            try:
                pe = pefile.PE(path)
            except:
                continue

            print(path)
            pe.parse_data_directories()

            try:
                for entry in pe.DIRECTORY_ENTRY_IMPORT:
                    # print(entry.dll)

                    outfile.write(str(entry.dll) + '\n')
                    for imp in entry.imports:
                        # print(getNameDLL(imp.name))
                        outfile.write('\t' + hex(imp.address) + ' ' + str(imp.name) + '\n')
                        try:
                            a = getNameDLL(imp.name)
                            b = dlls[getNameDLL(entry.dll)]
                            if a in b:
                                print('***Attention! This program use function ', imp.name)
                                break
                        except:
                            pass
            except:
                pass

        else:
            walk(path)


def walk2(dir):
    path = dir
    outfile.write(path + '\n')
    try:
        pe = pefile.PE(path)
    except:
        print('error')

    print(path)
    pe.parse_data_directories()

    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        print(entry.dll)

        outfile.write(str(entry.dll) + '\n')
        for imp in entry.imports:
            print('\t' + getNameDLL(imp.name))
            outfile.write('\t' + hex(imp.address) + ' ' + str(imp.name) + '\n')


path = os.getcwd()
walk('C:\Windows\System32')
#walk2(r"""C:\Windows\System32\ftp.exe""")
