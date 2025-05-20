import os
import shutil
from datetime import datetime as dt
import tkinter as tk
from tkinter import filedialog, messagebox

# all types of file, Capital bcz Constant Variable for whole program
FILE_TYPES = {
    "Images" : ['.png','.jpg','.jpeg','.gif'],
    "Audios" : ['.mp3','.ogg','.wav'],
    "Videos" : ['.mp4','.mkv','.mov'],
    "Documents" : ['.pdf','.docx','.xlsx','.ppt','.txt'],
    "Compressed" : ['.zip','.rar'],
    "Scripts" : ['.py','.html','.js','.bat'],
    "Program" : ['.exe']
}

def organize_file(folder_path, status_label):
    """ function to organize files in selected forlder."""
    
    if folder_path.strip() == "":
        messagebox.showwarning("Warning","Please select a folder first.")
        return
    
    if not os.path.exists(folder_path):
        messagebox.showerror("Error!","This folder does not exist. Please enter correct folder path.")
        return
    
    if os.path.isfile(folder_path):
        messagebox.showerror("Error!","This Selected Path is not a folder.")
        return

    files = os.listdir(folder_path)

    if not files:
        messagebox.showerror("Empty!","Selected Folder is empty.")
    count = 0
    log_file = os.path.join(folder_path, "log.txt")
    for file_name in files:
        if file_name == "log.txt":
            continue

        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path):
            ext = os.path.splitext(file_path)[1].lower()
            moved = False
            for folder, extentions in FILE_TYPES.items():
                if ext in extentions:
                    os.makedirs(os.path.join(folder_path, folder), exist_ok=True)
                    shutil.move(file_path, os.path.join(folder_path, folder, file_name))
                    moved = True
                    count += 1
                    break
            
            if not moved:
                os.makedirs(os.path.join(folder_path, "Others"), exist_ok=True)
                shutil.move(file_path, os.path.join(folder_path, "Others",file_name))
                count += 1
            
            with open(log_file, 'a', encoding="UTF-8") as log:
                        log.write(f"{file_name} -> |{folder if moved else "Others"}| at {dt.now()}\n")

    status_label.config(text=f"✅ Organize: {count} files !")

def browse_folder(entry_box):
    folder_selected = filedialog.askdirectory()
    entry_box.delete(0, tk.END)
    entry_box.insert(0, folder_selected)

def undo_files(folder_path, status_label):
    if not os.path.exists(folder_path):
         messagebox.showerror("Error","Selected Folder does not exists")
         return
    log_file = os.path.join(folder_path,'log.txt')
    with open(log_file, 'r', encoding="UTF-8") as f:
         lines = f.readlines()
    if not lines:
        messagebox.showerror("Empty","Log file is empty. Nothing to undo.")
        return
    last_line = lines[-1]
    file_name = last_line.split("->")[0].strip()
    folder = last_line.split("->")[1].split("at")[0].strip().strip('|')
    source = os.path.join(folder_path, folder, file_name)
    destination = os.path.join(folder_path, file_name)
    shutil.move(source, destination)
    status_label.config(text=f"Undo {file_name} -> |{folder}|.")

    with open(log_file, 'w', encoding='UTF-8') as f:
         f.writelines(lines[:-1])


def main():
    root = tk.Tk()
    root.title("File Organizer")
    root.geometry("400x300")
    root.resizable(False, False)

    tk.Label(root, text="Select folder to organize", font=("Arial",12)).pack(pady=10)

    entry_box = tk.Entry(root, width=40)
    entry_box.pack()

    tk.Button(root, text="Browse", command=lambda: browse_folder(entry_box)).pack(pady=5)

    status_label = tk.Label(root, text="", font=("Arial",10))
    status_label.pack(pady=10)

    tk.Button(
        root, text="Organize File", fg="black", bg="#4CAF50",
        command=lambda: organize_file(entry_box.get(), status_label)
    ).pack(pady=5)

    tk.Button(root, text="Unod last moved", bg="red", fg="white", command=lambda:undo_files(entry_box.get(),status_label)).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()