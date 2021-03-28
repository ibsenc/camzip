import os.path
from os import path
from queue import Queue
from file_directory_utils import FileDirectoryUtils


class CamZipper:

    def __init__(self, source, destination, ignore_file):
        self.source = source
        self.ignored_files_and_directories = set()
        self.populate_ignored_files_and_directories(ignore_file)
        self.parent_path = os.path.dirname(source)
        self.destination = destination
        self.queue = Queue()
        self.current = None

    def __repr__(self):
        """Return an informative string for debugging"""
        return (f"{self.__class__.__name__}:"
                f"\n(source: {self.source})"
                f"\n(parent_path: {self.parent_path})"
                f"\n(destination: {self.destination})"
                f"\n(current file or directory: {self.current})"
                f"\n(queue: {self.queue})")

    def clean_zip_to_destination(self):
        # Add source file to queue
        self.queue.enqueue(self.source)
        while(not self.queue.is_empty()):

            self.current = self.queue.dequeue()
            # If ignored
            if(self.is_ignored(self.current)):
                continue

            new_path = self.current.replace(self.parent_path, self.destination)

            # If it is a directory, make directory in that destination
            if(os.path.isdir(self.current)):
                FileDirectoryUtils.make_directory(new_path)
                for child in FileDirectoryUtils.get_children(self.current):
                    self.queue.enqueue(f"{self.current}/{child}")

            # If it is a file, copy file in that destination
            elif(os.path.isfile(self.current)):
                FileDirectoryUtils.copy_file(self.current, new_path)

    def is_ignored(self, path):
        file_name = path.split('/')[-1]
        if file_name in self.ignored_files_and_directories:
            return True

    def populate_ignored_files_and_directories(self, ignore_file):
        self.ignored_files_and_directories.add(".cam_ignore")
        for line in open(ignore_file, 'r'):
            self.ignored_files_and_directories.add(line.strip())
