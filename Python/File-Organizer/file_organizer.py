# merging undo_last_moved function and undo_all function in v0.2.1
# Adding fxn like validate folder path, ask folder path again if folder_path not exists

import os
import shutil
from datetime import datetime as dt

file_type = {
    "Images" : ['.jpg','.gif','.png','.jpeg'],
    "Musics" : ['.mp3','.wav','ogg'],
    "Vidoes" : ['.mp4', '.mkv','.mov'],
    "Documents" : ['.pdf','.xlsx','.docx','.txt','.ppt'],
    "Compressed" : ['.zip','.rar'],
    "Scripts" : [".py",".html",'.ahk','.js']
}
def welcome():
    user_path = input("Welcome to simple file organizer built in python.\nEnter the full path of folder to organize(leave empty for default folder 'Downloads':\n")
    return user_path

folder_path = welcome()

if folder_path.strip() == "":
    folder_path = os.path.join(os.path.expanduser("~"), "Downloads")

if os.path.exists(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name == "log.txt":
            continue

        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file_path)
            moved = False
            for folder, extention in file_type.items():
                if ext.lower() in extention:
                    os.makedirs(os.path.join(folder_path, folder), exist_ok=True)
                    destination = os.path.join(folder_path, folder, file_name)
                    shutil.move(file_path, destination)
                    print(f"Moved: {file_name} -> {folder}/\n")
                    moved = True
                    break

            if not moved:
                os.makedirs(os.path.join(folder_path,"Others"), exist_ok=True)
                destination = os.path.join(folder_path, 'Others', file_name)
                shutil.move(file_path, destination)
                print(f"Moved: {file_name} -> Others/\n")

            log_file = os.path.join(folder_path, "log.txt")
            with open(log_file, 'a', encoding='UTF-8') as log:
                log.write(f"{file_name} -> |{folder if moved else 'Others'}| at {dt.now()}\n")

            

else:
    print(f"Your folder path ({folder_path}), does not exists. Please enter a correct path.")
    welcome()

def undo_files(folder_path, undo_option):
    log_file = os.path.join(folder_path, "log.txt")
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='UTF-8') as f:
            lines = f.readlines()

        if not lines:
            print("Log file is empty. Nothing to undo.")
            return
        lines_to_keep = lines[:]
        if undo_option == "1":
            for line in reversed(lines):
                file_name = line.split("->")[0].strip()
                folder = line.split("->")[1].split("at")[0].strip().strip('|')
                source = os.path.join(folder_path, folder, file_name)
                destination = os.path.join(folder_path, file_name)
                shutil.move(source, destination)
                lines_to_keep.remove(line)
                print(f"Moved back: {file_name} to main folder.\n")
        elif undo_option == "2":
            last_line = lines[-1]
            file_name = last_line.split("->")[0].strip()
            folder = last_line.split("->")[1].split("at")[0].strip().strip('|')
            source = os.path.join(folder_path, folder, file_name)
            destination = os.path.join(folder_path, file_name)
            shutil.move(source, destination)
            print(f"Moved back: {file_name} to main folder.\n")
            lines_to_keep.remove(last_line)
        elif undo_option == "3":
            print("Thanks for using me. Have a good day.")
        else:
            print("Please choose a correct option (1, 2 or 3).")
        
        with open(log_file, 'w', encoding='UTF-8') as f:
            f.writelines(lines_to_keep)

    else:
        print("Log file does not exists at expected location. Cannot Undo.")

user_option = input("1. Undo all moved files\n2. Undo last moved file\n3. No Undo\nChoose option to undo: ")
undo_files(folder_path, user_option)