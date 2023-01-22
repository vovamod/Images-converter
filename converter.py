# Importing modules
import os
from time import sleep as w
from os import listdir as ld
from os.path import isfile, join
from PIL import Image
from progress.bar import Bar
import cfg as c


# Creating class Converter
class Converter:

    # Initializing variables and directories locations
    def __init__(self):
        self.in_dir = (str(os.getcwd()) + f'/{c.dir_1}/')
        self.ou_dir = (str(os.getcwd()) + f'/{c.dir_2}/')
        self.error_list = []

    # Checking if directory exist, if not creating one and looking for files with specific format from cfg.py "ft_1" (filetype_1)
    def dir_check(self):
        try:
            os.mkdir(c.dir_1)
        except FileExistsError:
            pass
        try:
            os.mkdir(c.dir_2)
        except FileExistsError:
            pass
        raw_files = [f for f in ld(self.in_dir) if isfile(join(self.in_dir, f))]
        files = [x for x in raw_files if c.ft_1 in x]
        Converter.convert(self, self.in_dir, self.ou_dir, files)

    # Launching bar. Looking if directory is empty. If yes, notifying user and closing program. Otherwise, converting file from format a to b
    def convert(self, io, ou, f):
        bar = Bar('Processing', max=len(f))
        if len(f) == 0:
            print('EXCEPTION\nFolder DDS is empty, no DDS files were found!')
            w(5)
        else:
            for convert_f in f:
                path_1 = io + convert_f
                path_2 = ou + convert_f
                try:
                    with Image.open(path_1) as img:
                        img.load()
                        img.save(path_2.replace(c.ft_1, "") + c.ft_2)
                        img.close()
                        bar.next()
                except:
                    self.error_list.append(path_1)
                    bar.next()
                    pass
        bar.finish()
        Converter.error_check(self)

    # Performing error check if any were found during converting and notifying user with list of files which were not converted properly due to some unknown error
    def error_check(self):
        if len(self.error_list) > 0:
            print(f"\nAmount of errors while trying to convert files is {len(self.error_list)}\nMaybe files were corrupted or unsupported compression type was detected\nList of files which were not converted:")
            print(*self.error_list, sep='\n')
        else:
            pass
        input("\nPress any key to close application...")


# Run the script
if __name__ == "__main__":
    main = Converter()
    main.dir_check()
