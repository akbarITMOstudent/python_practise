import os
import shutil
import inquirer
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.DEBUG,
    filename = "mylog.log",
    format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt = '%H:%M:%S'
)

main_path = 'C:/Users/akbar/Downloads'

extensions = {
    'video': ['mp4', 'mov', 'avi', 'mkv', 'wmv', '3gp', '3g2', 'mpg', 'mpeg', 'm4v', 'h264', 'flv', 'rm', 'swf', 'vob'],
    'data': ['sql', 'sqlite', 'sqlite3', 'csv', 'dat', 'db', 'log', 'mdb', 'sav', 'tar', 'xml'],
    'audio': ['mp3', 'wav', 'ogg', 'flac', 'aif', 'mid', 'midi', 'mpa', 'wma', 'wpl', 'cda'],
    'image': ['jpg', 'png', 'bmp', 'ai', 'psd', 'ico', 'jpeg', 'ps', 'svg', 'tif', 'tiff'],
    'archive': ['zip', 'rar', '7z', 'z', 'gz', 'rpm', 'arj', 'pkg', 'deb'],
    'documents': ['pdf', 'txt', 'doc', 'docx', 'rtf', 'tex', 'wpd', 'odt'],
    '3d': ['stl', 'obj', 'fbx', 'dae', '3ds', 'iges', 'step'],
    'presentation': ['pptx', 'ppt', 'pps', 'key', 'odp'],
    'spreadsheet': ['xlsx', 'xls', 'xlsm', 'ods'],
    'font': ['otf', 'ttf', 'fon', 'fnt'],
    'gif': ['gif'],
    'exe': ['exe'],
    'bat': ['bat'],
    'apk': ['apk']
}

ext_to_category = {ext.lower(): category for category, ext_list in extensions.items() for ext in ext_list}


def create_folders(base_path, folder_names):
    for folder in folder_names:
        target_dir = os.path.join(base_path, folder)
        os.makedirs(target_dir, exist_ok=True)


def sort_files(folder_path):
    for entry in os.scandir(folder_path):
        if entry.is_file():
            ext = os.path.splitext(entry.name)[1].lstrip('.').lower()
            
            category = ext_to_category.get(ext)
            if category:
                dest_dir = os.path.join(folder_path, category)
                dest_file = os.path.join(dest_dir, entry.name)
                
                print(f'Moving {entry.name} -> {category}/')
                
                try:
                    shutil.move(entry.path, dest_file)
                except Exception as e:
                    print(f'Error moving {entry.name}: {e}')


def remove_empty_folders(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir_name in dirs:
            dir_to_check = os.path.join(root, dir_name)
            if not os.listdir(dir_to_check):
                print(f'Deleting empty folder: {dir_name}')
                os.rmdir(dir_to_check)


if __name__ == "__main__":
    create_folders(main_path, extensions.keys())
    sort_files(main_path)
    remove_empty_folders(main_path)
actions = ["Search", "Sort"]

question = [
    inquirer.List(
        "choose_action",
        message="What you want to do?",
        choices=actions,
    )
]
answer = inquirer.prompt(question)
print(f"\nYou choose: {answer['choose_action']}")

