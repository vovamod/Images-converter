import os
from time import sleep as w
from os import listdir as ld
from os.path import isfile, join
from PIL import Image
from progress.bar import Bar
import cfg as c


class Main:
    def __init__(self):
        self.in_dir = (str(os.getcwd()) + f'/{c.dir_1}/')
        self.ou_dir = (str(os.getcwd()) + f'/{c.dir_2}/')
        self.error_list = []
        Main.dir_check(self)

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
        Main.dds_convert(self, self.in_dir, self.ou_dir, files)

    def dds_convert(self, io, ou, f):
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
                        # os.remove(path_1)
                except:
                    self.error_list.append(path_1)
                    bar.next()
                    pass
        bar.finish()
        Main.error_check(self, f)

    def error_check(self, files):
        if len(self.error_list) > 0:
            print(f"Amount of errors while trying to convert files is {len(self.error_list)} out of {len(files)}\nMaybe files were corrupted or unsupported compression type was detected\nList of files which were not converted:")
            print(*self.error_list, sep='\n')

        else:
            pass


if __name__ == "__main__":
    Main()
