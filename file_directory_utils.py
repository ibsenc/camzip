import os
from shutil import copyfile
from os import listdir


class FileDirectoryUtils:

    @staticmethod
    def check_if_valid_dir(dir_path):
        if not os.path.isdir(dir_path):
            raise Exception(f"Not a valid directory: {dir_path}")

    @staticmethod
    def copy_file(source, destination):
        print(f"Copying file from {source} to {destination}")
        copyfile(source, destination)

    @staticmethod
    def make_directory(path):
        print("Making directory: " + path)
        os.mkdir(path)

    @staticmethod
    def get_children(path):
        return listdir(path)
