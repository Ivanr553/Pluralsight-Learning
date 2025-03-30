import os, fnmatch, shutil
from datetime import datetime
from pathlib import Path

def list_dir(path):
    for file in os.listdir(path):
        print(file)
        

def ends_with(path, search):
    for file in os.listdir(path):
        if file.endswith(search):
            print(file)


def starts_with(path, search):
    for file in os.listdir(path):
        if file.startswith(search):
            print(file)


def match(path, search):
    for file in os.listdir(path):
        if fnmatch.fnmatch(file, search):
            print(file)


def get_date(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%d %b %Y')


def get_file_attrs(path):
    with os.scandir(path) as dir:
        for file in dir:
            if file.is_file():
                info = file.stat()
                print(f'Modified {get_date(info.st_mtime)} {file.name}')


def traverse(path):
    for folder, dirs, files, in os.walk(path):
        print('Folder: ', folder)
        for file in files:
            print(f'File: {file}')
        for dir in dirs:
            print(f'Dir: {dir}')


def copy_file(src, dst):
    shutil.copy(src, dst)

def copy_dir(src, dst):
    shutil.copytree(src, dst)

def move_file(src, dst):
    shutil.move(src, dst)

def move_dir(src, dst):
    shutil.move(src, dst)

def remove_file(path):
    os.remove(path)

def remove_dir(path):
    shutil.rmtree(path)


def rename_file(path, destination):
    file = Path(path)
    new_file = file.with_name(destination)
    os.rename(path, new_file)
    
def rename_file_2(path, destination):
    file = Path(path)
    file.rename(destination)


def main():
    traverse("./test_folder")

main()