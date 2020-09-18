
import sys
import subprocess
import itertools
from pathlib import Path

search_item = sys.argv[1]
starting_directories = sys.argv[2:]

for starting_directory in starting_directories:
    paths = list(Path(starting_directory).rglob(f"*{search_item}*"))
    if len(paths) > 0:
        subprocess.Popen(f'explorer /open, {paths[0].absolute()}')