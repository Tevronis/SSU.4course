import shutil

from obfuscator.obfuscator import Obfuscator


def obfuscator(file):
    shutil.copyfile(file, 'original.cpp')
    scr = Obfuscator(file)

    scr.concatBlocks()
    scr.renameVariables()
    scr.concatBlocks()
    scr.renameGlobalVariables()
    scr.renameFunctions()
    # GOTO:
    scr.generateGoto()
    scr.generateGoto()
    scr.generateGoto()

    with open('main.cpp', 'w') as f:
        f.write(scr.text)


def main():
    obfuscator("samples/test6.cpp")


if __name__ == "__main__":
    main()
