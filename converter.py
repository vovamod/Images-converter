import os
from os import listdir
from pathlib import Path
from PIL import Image
from tqdm import tqdm
import concurrent.futures
import yaml

def load_config():
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
    return config

config = load_config()
input_dir = config['input_dir']
output_dir = config['output_dir']
input_file_format = config['input_file_format']
output_file_format = config['output_file_format']


class Converter:
    """
    This class converts files from one format to another.
    """

    def __init__(self):
        """
        Initializes variables and directories locations.
        """
        self.input_directory = Path.cwd() / input_dir
        self.output_directory = Path.cwd() / output_dir
        self.error_list = []

    def dir_check(self):
        """
        Checks if directory exists, if not creates one and looks for files with specific format from config.yml "ft_1" (filetype_1).
        """
        self.input_directory.mkdir(parents=True, exist_ok=True)
        self.output_directory.mkdir(parents=True, exist_ok=True)
        files = [f for f in self.input_directory.iterdir() if f.is_file() and input_file_format in f.name]
        self.convert(files)

    def convert_file(self, file_path, output_directory):
        """
        Convert file function, gets a file location and make a img var from PIL Image module then convert it
        """
        try:
            with Image.open(file_path) as img:
                img.load()
                file_name = os.path.basename(file_path).replace(input_file_format, output_file_format)
                output_path = os.path.join(output_directory, file_name)
                img.save(output_path)
        except (IOError, OSError) as e:
            self.error_list.append(file_path)
            print(f"Error converting {file_path}: {str(e)}")

    def convert(self, files):
        """
        Convert function which will call convert_file and use multiple threads in System which are available
        """
        if len(files) == 0:
            print(f'\nEXCEPTION!!!\n\nFolder {input_dir} is empty, no {input_file_format} files were found!')
        else:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.convert_file, os.path.join(self.input_directory, file), self.output_directory) for file in files]
                for _ in tqdm(concurrent.futures.as_completed(futures), desc='Converting', unit='files', total=len(futures)):
                    pass
        self.error_check()

    def error_check(self):
        """
        Performs error check if any were found during converting and notifies user with list of files which were not converted properly due to some unknown error.
        """
        if len(self.error_list) > 0:
            print(f"\nAmount of errors while trying to convert files is {len(self.error_list)}\n"
                  f"List of files which were not converted:")
            print(*self.error_list, sep='\n')
        input("\nPress any key to close application...")


if __name__ == "__main__":
    main = Converter()
    main.dir_check()
