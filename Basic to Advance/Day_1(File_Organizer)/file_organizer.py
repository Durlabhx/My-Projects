import os
import shutil
from datetime import datetime

folder_path = input("Enter the full path of the folder to organize:\n(Leave empty for default Downloads folder)\n")

if folder_path.strip() == "":
    folder_path = os.path.join(os.path.expanduser("~"), "Downloads")

file_types = {
    'Images' : ['.jpg','.jpeg','.png','.gif'],
    'Vides' : ['.mp4','.mkv','.avi'],
    'Documents' : ['.pdf', '.docx','.txt'],
    'Music' : ['.mp3', '.wav'],
    'Scripts' : ['.py','.js','.html','.css']
}

for file_name in os.listdir(folder_path):
    if file_name == "log.txt":
        continue
    file_path = os.path.join(folder_path, file_name)

    if os.path.isfile(file_path):
        _, ext = os.path.splitext(file_name)

        moved = False
        for folder, extensions in file_types.items():
            if ext.lower() in extensions:
                target_folder = os.path.join(folder_path, folder)
                os.makedirs(target_folder, exist_ok=True)
                shutil.move(file_path, os.path.join(target_folder, file_name))
                print(f"Moved: {file_name} -> {folder}/")
                moved=True
                break

        if not moved:
            other_folder = os.path.join(folder_path, "Others")
            os.makedirs(other_folder, exist_ok=True)
            shutil.move(file_path, os.path.join(other_folder, file_name))
            print(f"Moved: {file_name} -> Others/")

        log_file = os.path.join(folder_path, "log.txt")
        with open(log_file, 'a', encoding="utf-8")as log:
            log.write(f"{file_name} -> {folder if moved else 'Others'} at {datetime.now()}\n")

def undo_last_move(folder_path):
    log_file=os.path.join(folder_path, 'log.txt')

    if not os.path.exists(log_file):
        print("No log file found. Cannot Undo.")
        return
    
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if not lines:
        print("Log is empty. Nothing to undo.")
        return 
    last_line = lines[-1]
    try:
        file_name=last_line.split("->")[0].strip()
        folder=last_line.split("->")[1].split('at')[0].strip()
        source=os.path.join(folder_path, folder, file_name)
        destination=os.path.join(folder_path, file_name)

        if os.path.exists(source):
            shutil.move(source, destination)
            print(f"MOved back: {file_name} from {folder}/ to main folder")

            #Remove last line from log
            with open(log_file, 'w', encoding='utf-8') as f:
                f.writelines(lines[:-1])
        else:
            print("File not found in expected location")

    except Exception as e:
        print("Error while undoing:", e)

undo = input("Do you want to undo last moved file (yes/no): ").lower()
if undo == "yes":
    undo_last_move(folder_path)
