
import subprocess
import argparse

from pathlib import Path


class FdFinder:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Find files or directories and open Windows explorer")

        parser.add_argument("-r", "--recursive", action="store_true",
                            help="If this option is specified, all subdirectories are searched recursively "
                                 "for the search_item.")
        parser.add_argument("-o", "--open", action="store_true",
                            help="If this option is given and the given search_item is a file and it has been found,"
                                 "the search_item is opened with it's default application.")
        parser.add_argument("-m", "--max", metavar="m", default=-1, type=int,
                            help="Maximum number of search_item candidates the program will search for.")
        parser.add_argument("search_item", metavar="s", type=str, nargs=1, help="File or directory to be searched for")
        parser.add_argument("search_directories", metavar="d", type=str, nargs="*",
                            help="List of directories the search will start from", default=["."])

        args = parser.parse_args()

        self.__recursive = args.recursive
        self.__open = args.open
        self.__max = int(args.max)
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

            if self.__max == -1:
                index_counter = 0

                if self.__recursive:
                    for item in directory.rglob(f"{self.__search_item}"):
                        paths.append(item.absolute())
                        print(f"Press {index_counter} to open explorer at {paths[-1]}.")
                        index_counter += 1
                else:
                    for item in directory.glob(f"{self.__search_item}"):
                        paths.append(item.absolute())
                        print(f"Press {index_counter} to open explorer at {paths[-1]}.")
                        index_counter += 1
            else:
                index_counter = 0

                if self.__recursive:
                    for item in directory.rglob(f"{self.__search_item}"):
                        paths.append(item.absolute())
                        print(f"Press {index_counter} to open explorer at {paths[-1]}.")
                        index_counter += 1
                        if index_counter == self.__max:
                            break
                else:
                    for item in directory.glob(f"{self.__search_item}"):
                        paths.append(item.absolute())
                        print(f"Press {index_counter} to open explorer at {paths[-1]}.")
                        index_counter += 1
                        if index_counter == self.__max:
                            break

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

            if self.__open:
                subprocess.Popen(f'explorer /run,{self.__search_item_paths[user_input].absolute()}')
            else:
                subprocess.Popen(f'explorer /select,{self.__search_item_paths[user_input].absolute()}')