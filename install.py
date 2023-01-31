#!/usr/bin/env python3
from contextlib import suppress
from os import environ,path,pathsep,remove,getcwd
from shutil import copy

def add_to_path(file_path):
    checkedpaths = []
    for dir in environ['PATH'].split(pathsep):
        checkedpaths.append(dir)
        with suppress(OSError):
            with open(path.join(dir, 'test.txt'), 'w') as f:
                f.write('')
            remove(path.join(dir, 'test.txt'))
            copy(file_path, f'{dir}/seek')
            print(f"Copied {file_path} to {dir}")
            return
    print(f"No writeable directories found in $PATH {':'.join(str(v) for v in checkedpaths)}")

def setup():
    # Replace the path with the path to your script file
    script_file = f"{getcwd()}/seek.py"
    add_to_path(script_file)

if __name__ == '__main__':
    setup()
