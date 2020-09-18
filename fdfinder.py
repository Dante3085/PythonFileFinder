
import sys
import subprocess
import itertools
from pathlib import Path
'''
TODO:
1. Make search_item and starting_directories fuzzy.
   (Similar strings will also be searched)
'''


search_item = sys.argv[1]
starting_directories = sys.argv[2:]

for starting_directory in starting_directories:
    paths = list(Path(starting_directory).rglob(f"*{search_item}*"))
    if len(paths) > 0:
        subprocess.Popen(f'explorer /select, {paths[0].absolute()}')