import os
import shutil
from shutil import copy2

cwd_of_main_py = os.path.dirname(os.path.realpath(__file__))
public_path = os.path.realpath(os.path.join(cwd_of_main_py, "../public"))
static_path = os.path.realpath(os.path.join(cwd_of_main_py, "../static"))

def copy_dir_all(src, dst):
    list_contents = os.listdir(src)
    if list_contents == []:
        return
    for item in list_contents:
        current = os.path.join(src, item)
        destination = os.path.join(dst, item)
        if os.path.isfile(current):
            copy2(current, destination)
        if os.path.isdir(current):
            os.mkdir(destination)
            copy_dir_all(current, destination)

def copy_static():
    if os.path.exists(public_path):
        if os.path.isfile(public_path):
            os.remove(public_path)
        elif os.path.isdir(public_path):
            shutil.rmtree(public_path)
        else:
            raise Exception("Error: unknown error in main. Trouble removing public path.")
    if not os.path.exists(public_path):
        os.mkdir(public_path)
    copy_dir_all(static_path, public_path)

def main():
    copy_static()

main()
