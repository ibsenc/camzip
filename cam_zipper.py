from queue import Queue
import os.path
from os import listdir
from shutil import copyfile


class CamZipper:
    """A class that transfers all nested files without ignored content."""
    def __init__(self, source, destination, ignore_file):
        """
        Initialize the CamZipper class.
        self, string, string, string -> None
        """
        self.source = source
        self.ignored_files_and_directories = set()
        self.populate_ignored_files_and_directories(ignore_file)
        self.parent_path = os.path.dirname(source)
        self.destination = destination
        self.queue = Queue()
        self.current = None

    def __repr__(self):
        """
        Return an informative string for debugging
        self -> None
        """
        return (f"{self.__class__.__name__}:"
                f"\n(source: {self.source})"
                f"\n(parent_path: {self.parent_path})"
                f"\n(destination: {self.destination})"
                f"\n(current file or directory: {self.current})"
                f"\n(queue: {self.queue})")

    def clean_zip_to_destination(self):
        """
        Copy all nested files to new dir without ignored content.
        self -> None
        """
        # Add source file to queue
        self.queue.enqueue(self.source)

        while(not self.queue.is_empty()):
            self.current = self.queue.dequeue()
            # If ignored, skip
            if(self.is_ignored(self.current)):
                continue

            new_path = self.current.replace(self.parent_path, self.destination)

            # If it is a directory, make directory in that destination
            if(os.path.isdir(self.current)):
                print("Making directory: " + new_path)
                os.mkdir(new_path)
                for child in listdir(self.current):
                    self.queue.enqueue(f"{self.current}/{child}")

            # If it is a file, copy file in that destination
            elif(os.path.isfile(self.current)):
                print(f"Copying file from {self.source} to {self.destination}")
                copyfile(self.current, new_path)

    def is_ignored(self, path):
        """
        Check if a file or directory is in the ignore file. Returns a boolean.
        self, string -> boolean
        """
        file_or_dir_name = path.split('/')[-1]
        if file_or_dir_name in self.ignored_files_and_directories:
            return True

    def populate_ignored_files_and_directories(self, ignore_file):
        """
        Add items in ignore file to a set of files to ignore
        self, string -> None
        """
        # Add .cam_ignore file to set of files to ignore
        self.ignored_files_and_directories.add(".cam_ignore")

        # For each file ignore_file, add to ignore set
        for line in open(ignore_file, 'r'):
            self.ignored_files_and_directories.add(line.strip())
