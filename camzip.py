from cam_zipper import CamZipper
import os.path
from os import path
import sys
import shutil
from file_directory_utils import FileDirectoryUtils
import zipfile


def main(args):
    # Set source to first argument
    if (len(args) < 2):
        raise Exception(f"Source path is required.")
    else:
        source = args[1]
        if not os.path.isdir(source):
            raise Exception(f"Source is not a directory: {source}")

    # Set optional destination path to second argument
    if (len(args) >= 3):
        destination = args[2]
        if not os.path.isdir(destination):
            raise Exception(f"Destination is not a directory: {destination}")

    # If not provided, default destination is one directory up from source
    else:
        destination = os.path.dirname(source)

    if (len(args) >= 4):
        ignore_file = args[3]
        if not os.path.isfile(ignore_file):
            raise Exception(f"Ignore file is not a file: {ignore_file}")
    else:
        ignore_file = f"{source}/.cam_ignore"
        if not os.path.exists(ignore_file):
            open(ignore_file, 'w')
            print("New .cam_ignore file created. Update with file/directory \
                names you'd like to exclude here: " + ignore_file)

    # Create destination directory to store copy of items to zip
    temp_destination = str(destination) + "/cam_temp"
    if (path.exists(temp_destination)):
        shutil.rmtree(temp_destination)
        print("Deleting pre-existing cam_temp directory.")
    os.mkdir(temp_destination)
    print("Creating new cam_temp directory.")

    # Clean up items
    cz = CamZipper(source, temp_destination, ignore_file)
    cz.clean_zip_to_destination()

    # Zip the directory
    source_parent = os.path.dirname(source)
    source_file_name = source.split('/')[-1]
    os.chdir(source_parent)
    shutil.make_archive(source_file_name, 'zip', root_dir="cam_temp")

    # Delete temporary directory
    shutil.rmtree(temp_destination)


main(sys.argv)
