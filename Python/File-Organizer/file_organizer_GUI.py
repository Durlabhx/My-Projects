import os
import shutil
from datetime import datetime as dt
import tkinter as tk
from tkinter import filedialog, messagebox
from Widgets.dialogs import show_undo_dialog

FILE_TYPES = {
    "Images": ['.png', '.jpg', '.jpeg', '.gif'],
    "Audios": ['.mp3', '.ogg', '.wav'],
    "Videos": ['.mp4', '.mkv', '.mov'],
    "Documents": ['.pdf', '.docx', '.xlsx', '.ppt', '.txt'],
    "Compressed": ['.zip', '.rar'],
    "Scripts": ['.py', '.html', '.js', '.bat'],
    "Program": ['.exe']
}

def organize_file(folder_path, status_label):
    if folder_path.strip() == "":
        messagebox.showwarning("Warning", "Please select a folder first.")
        return

    if not os.path.exists(folder_path):
        messagebox.showerror("Error", "This folder does not exist.")
        return

    if os.path.isfile(folder_path):
        messagebox.showerror("Error", "The selected path is not a folder.")
        return

    files = os.listdir(folder_path)
    if not files:
        messagebox.showerror("Empty!", "Selected folder is empty.")
        return

    log_file = os.path.join(folder_path, "log.txt")
    file_summary = {}
    count = 0

    for file_name in files:
        if file_name == "log.txt":
            continue

        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path):
            ext = os.path.splitext(file_path)[1].lower()
            moved = False
            for folder, extensions in FILE_TYPES.items():
                if ext in extensions:
                    os.makedirs(os.path.join(folder_path, folder), exist_ok=True)
                    shutil.move(file_path, os.path.join(folder_path, folder, file_name))
                    moved = True
                    count += 1
                    file_summary[folder] = file_summary.get(folder, 0) + 1
                    break

            if not moved:
                os.makedirs(os.path.join(folder_path, "Others"), exist_ok=True)
                shutil.move(file_path, os.path.join(folder_path, "Others", file_name))
                count += 1
                file_summary["Others"] = file_summary.get("Others", 0) + 1

            with open(log_file, 'a', encoding="UTF-8") as log:
                log.write(f"{file_name} -> |{folder if moved else 'Others'}| at {dt.now()}\n")

    summary = f"✅ Organized: {count} files!\n"
    for category, num in file_summary.items():
        summary += f"  - {category}: {num}\n"

    status_label.config(text=summary.strip(), fg="green")

def browse_folder(entry_box):
    folder_selected = filedialog.askdirectory()
    # folder_name = folder_selected.split('/')[-1]
    entry_box.delete(0, tk.END)
    entry_box.insert(0, folder_selected)

def undo_files(folder_path, user_option, status_label):
    if not os.path.exists(folder_path):
        messagebox.showerror("Error", "Selected folder does not exist.")
        return

    log_file = os.path.join(folder_path, 'log.txt')
    if not os.path.exists(log_file):
        messagebox.showerror("Error", "No log file found.")
        return

    with open(log_file, 'r', encoding="UTF-8") as f:
        lines = f.readlines()

    if not lines:
        messagebox.showerror("Empty", "Log file is empty.")
        return

    lines_to_keep = lines[:]
    count = 0

    if user_option == "undo_last":
        last_line = lines[-1]
        file_name = last_line.split('->')[0].strip()
        folder = last_line.split('->')[1].split('at')[0].strip().strip('|')
        source = os.path.join(folder_path, folder, file_name)
        destination = os.path.join(folder_path, file_name)

        shutil.move(source, destination)
        lines_to_keep.remove(last_line)
        status_label.config(text=f"♻️ Undone: {file_name} from '{folder}'", fg="blue")
    else:
        for line in reversed(lines):
            file_name = line.split("->")[0].strip()
            folder = line.split("->")[1].split("at")[0].strip().strip('|')
            source = os.path.join(folder_path, folder, file_name)
            destination = os.path.join(folder_path, file_name)

            shutil.move(source, destination)
            lines_to_keep.remove(line)
            count += 1
        status_label.config(text=f"♻️ Undone: {count} files moved back!", fg="blue")

    with open(log_file, 'w', encoding='UTF-8') as f:
        f.writelines(lines_to_keep)

def handle_choice(choice, folder_path, status_label):
    if choice == "Undo Last":
        user_option = "undo_last"
    elif choice == "Undo All":
        user_option = "undo_all"
    else:
        return
    undo_files(folder_path, user_option, status_label)

def main():
    root = tk.Tk()
    root.title("🗂️ File Organizer")
    root.geometry("450x350")
    root.resizable(False, False)

    tk.Label(root, text="Select folder to organize", font=("Arial", 12)).pack(pady=(15, 5))

    entry_box = tk.Entry(root, width=45)
    entry_box.pack()

    tk.Button(root, text="Browse Folder", command=lambda: browse_folder(entry_box)).pack(pady=5)

    status_label = tk.Label(root, text="", font=("Arial", 10), justify="left")
    status_label.pack(pady=10)

    tk.Button(
        root, text="✅ Organize Files", fg="white", bg="#4CAF50",
        width=20, command=lambda: organize_file(entry_box.get(), status_label)
    ).pack(pady=5)

    tk.Button(
        root, text="↩️ Undo Files", bg="red", fg="white",
        width=20, command=lambda: show_undo_dialog(lambda choice: handle_choice(choice, entry_box.get(), status_label))
    ).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
