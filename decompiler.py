import os
from multiprocessing import Process
from time import sleep as w
from os import listdir
from os.path import isfile, join
from wand import image
from progress.bar import Bar


def dir():
    global files, input_dir, output_dir
    input_dir = (str(os.getcwd()) + '/DDS/')
    output_dir = (str(os.getcwd()) + '/PNG/')
    try:
        os.mkdir("DDS")
        os.mkdir("PNG")
    except FileExistsError:
        pass
    raw_files = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]
    files = [x for x in raw_files if ".dds" in x]
    return input_dir, output_dir, files


def dds_converter():
    bar = Bar('Processing', max=len(files))
    if len(files) == 0:
        print('EXCEPTION\nFolder DDS is empty, no DDS files were found!')
        w(5)
    else:
        for decompile_dds in files:
            path_dds = input_dir + decompile_dds
            path_png = output_dir + decompile_dds
            bar.next()
            with image.Image(filename=path_dds) as img:
                img.compression = "no"
                img.save(filename=(path_png + ".png"))
    bar.finish()


if __name__ == "__main__":
    dir()
    dds_converter()
