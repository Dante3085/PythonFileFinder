
import sys
import subprocess
from pathlib import Path


def get_search_item():
    return sys.argv[1]


def get_starting_directories():
    return sys.argv[2:]


search_item = get_search_item()
starting_directories = get_starting_directories()
possible_search_items_paths = []

for starting_directory in starting_directories:
    directory = Path(starting_directory)
    if not directory.exists():
        print(f"Given starting_directory \"{starting_directory}\" does not exist.")
        continue

    # search_item_paths = list(directory.rglob(f"*{search_item}*"))

    counter = 0
    for item in directory.rglob(f"*{search_item}*"):
        possible_search_items_paths.append(item.absolute())
        print(f"Press {counter} to open explorer at {possible_search_items_paths[-1]}.")
        counter += 1

    '''if len(search_item_paths) > 0:
        subprocess.Popen(f'explorer /select, {search_item_paths[0].absolute()}')'''

print("Give one of the above indices or type \"exit\" to quit the program.")
while True:
    user_input = input()
    if user_input.upper() == "EXIT":
        break

    user_input = int(user_input)
    if user_input < 0 or user_input >= len(possible_search_items_paths):
        print(f"Given index{user_input} is invalid. Use one of the above ones.")
        continue
    subprocess.Popen(f'explorer /select, {possible_search_items_paths[user_input].absolute()}')