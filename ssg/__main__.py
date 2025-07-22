import os
import sys
import shutil
from shutil import copyfile
from ssg.utils import export_content_to_public

cwd = os.path.realpath(os.getcwd())
public_path = os.path.realpath(os.path.join(cwd, "public"))
static_path = os.path.realpath(os.path.join(cwd, "static"))

def copy_dir_all(src, dst):
    list_contents = os.listdir(src)
    if list_contents == []:
        return
    for item in list_contents:
        current = os.path.join(src, item)
        destination = os.path.join(dst, item)
        if os.path.isfile(current):
            copyfile(current, destination)
        if os.path.isdir(current):
            os.makedirs(destination, exist_ok=True)
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
    args = sys.argv
    basepath = None
    if len(args) > 1:
        basepath=args[1]
    export_content_to_public(basepath=basepath)

if __name__ == "__main__":
    main()
