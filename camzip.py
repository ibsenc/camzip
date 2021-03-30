from cam_zipper import CamZipper
import os.path
from os import path
import shutil

DEFAULT_IGNORE_FILE = ".cam_ignore"
TEMP_DIR = "cam_temp"
DEFAULT_MESSAGE = "or press Enter to generate default"


def do_validate_and_set_source(source_string):
    """
    Validate user input and set source to valid input.
    string -> string
    """
    if (len(source_string) == 0):
        raise Exception(f"Source path is required.")
    else:
        source = source_string
        if not os.path.isdir(source):
            raise Exception(f"Source is not a directory: {source}")
    return source


def do_validate_and_set_destination(destination_string, source):
    """
    Validate user input and set optional destination path as input or default.
    string, string -> string
    """
    # If not provided, default destination is parent directory of source
    if (len(destination_string) == 0):
        destination = os.path.dirname(source)
    else:
        destination = destination_string
        if not os.path.isdir(destination):
            raise Exception(f"Destination is not a directory: {destination}")
    return destination


def do_validate_and_set_ignore(ignore_file_string, source):
    """
    Validate user input and set ignore file
    string, string -> string
    """
    if (len(ignore_file_string) == 0):
        ignore_file = f"{source}/{DEFAULT_IGNORE_FILE}"
        if not os.path.exists(ignore_file):
            open(ignore_file, 'w')
            print(f"New {DEFAULT_IGNORE_FILE} file created. Files/directories \
                 listed in file will not be included in the zip. \
                 Open {ignore_file} to update.")
    else:
        ignore_file = ignore_file_string
        if not os.path.isfile(ignore_file):
            raise Exception(f"Ignore file is not a file: {ignore_file}")
    return ignore_file


def do_create_temp_destination_dir(destination):
    """
    Create a temporary directory in destination location.
    string -> None
    """
    temp_destination = f"{destination}/{TEMP_DIR}"
    if (path.exists(temp_destination)):
        shutil.rmtree(temp_destination)
        print("Deleting pre-existing cam_temp directory.")
    os.mkdir(temp_destination)
    print("Creating new cam_temp directory.")
    return temp_destination


def do_zip_dir(source):
    """
    Create a zip file in temporary directory.
    """
    # Zip the directory
    # TODO: zip file [-2] to get parent dir?
    source_parent = os.path.dirname(source)
    source_file_name = source.split('/')[-1]
    os.chdir(source_parent)
    shutil.make_archive(source_file_name, 'zip', root_dir=TEMP_DIR)


def do_ask_to_zip_another():
    """
    Ask user if they would like to zip another directory and either restarts
    while loop or terminates the program.
    """
    response = input("Would you like to zip another directory? (y/n)").lower()
    if(response == "yes" or response == "y"):
        return
    else:
        exit


def main():

    while(True):
        # Ask for file/directory to zip
        source_input = (input("Enter source path: "))
        source = do_validate_and_set_source(source_input)

        # Ask for destination of the .zip file
        # TODO: change default destination to parent dir of source
        destination = (input(
            f"Enter destination path for zip file ({DEFAULT_MESSAGE}. Default = source): ")).strip()
        destination = do_validate_and_set_destination(destination, source)

        # Ask for ignore file
        ignore_file_input = (input(
            f"Enter path for ignore file ({DEFAULT_MESSAGE}.): ")).strip()
        ignore_file = do_validate_and_set_ignore(ignore_file_input, source)

        # Create destination directory to store copy of items to zip
        temp_destination = do_create_temp_destination_dir(destination)

        # Clean up items
        cz = CamZipper(source, temp_destination, ignore_file)
        cz.clean_zip_to_destination()

        # Zip the directory
        do_zip_dir(source)

        # Deletes temporary directory
        shutil.rmtree(temp_destination)

        print("Source file zipped successfully.")
        do_ask_to_zip_another()


main()
