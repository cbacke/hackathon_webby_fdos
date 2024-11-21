#!/usr/bin/env python3

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
FILETREE_ROOT = PROJECT_ROOT / 'filetree'

def main():
    with open(PROJECT_ROOT / 'input/directory_paths.txt') as f:
        for line in f:
            rel_dirpath = line.strip()[2:]
            abs_dirpath = FILETREE_ROOT / rel_dirpath
            abs_dirpath.mkdir(parents=True, exist_ok=True)
    with open(PROJECT_ROOT / 'input/file_paths.txt') as f:
        for line in f:
            rel_filepath = line.strip()[2:]
            abs_filepath = FILETREE_ROOT / rel_filepath
            abs_filepath.touch(exist_ok=True)

if __name__ == '__main__':
    main()
