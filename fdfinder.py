
import sys
import subprocess
import argparse

from fdfinder_exceptions import MissingSearchItemError
from pathlib import Path


class FdFinder:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Find files or directories and open Windows explorer")

        parser.add_argument("-r", "--run")
        parser.add_argument("search_item", metavar="s", type=str, nargs=1, help="File or directory to be searched for")
        parser.add_argument("search_directories", metavar="d", type=str, nargs="*",
                            help="List of directories the search will start from", default=["."])

        args = parser.parse_args()

        self.__search_item = args.search_item[0]
        self.__starting_directories = args.search_directories
        self.__search_item_paths = self.__get_search_item_paths()

    def __get_search_item_paths(self):
        paths = []

        # Look for the search_item in every starting_directory
        for starting_directory in self.__starting_directories:
            directory = Path(starting_directory)
            if not directory.exists():
                print(f"Given starting_directory \"{starting_directory}\" does not exist.")
                continue

            counter = 0
            for item in directory.rglob(f"*{self.__search_item}*"):
                paths.append(item.absolute())
                print(f"Press {counter} to open explorer at {paths[-1]}.")
                counter += 1

        return paths

    def present_search_item_paths_to_user(self):
        if len(self.__search_item_paths) == 0:
            print(f"Couldn't find search_item \"{self.__search_item}\" "
                  f"in starting_directories {self.__starting_directories}")
            return

        print("Give one the above indices or type \"exit\" to quit the program.")
        while True:
            user_input = input()

            if user_input.upper() == "EXIT":
                break

            try:
                user_input = int(user_input)
            except ValueError as v:
                print(f"\"{user_input}\" is not an integer.")
                continue

            if user_input < 0 or user_input >= len(self.__search_item_paths):
                print(f"Given index \"{user_input}\" is invalid. Use one of the above indices.")
                continue

            subprocess.Popen(f'explorer /run,{self.__search_item_paths[user_input].absolute()}')
