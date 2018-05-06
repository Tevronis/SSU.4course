import pefile

FILE = 'main_py.exe'

p = pefile.ResourceDirData()
pp = pefile.PE(FILE).get_resources_strings()
print(p)
