# This file contains custom dialog boxes

import tkinter as tk

def show_undo_dialog():

    if hasattr(show_undo_dialog, "win") and show_undo_dialog.win.winfo_exists():
        show_undo_dialog.win.lift()
        main.root.bell()
        shake_window(show_undo_dialog.win)
        return

    win = tk.Toplevel()
    show_undo_dialog.win = win
    win.title("Undo Options")
    win.geometry("300x150")
    # win.transient()
    # win.grab_set()

    tk.Label(win, text="Choose Undo Option:", font=("Arial",12)).pack(pady=10)

    options = ["Undo Last", "Undo All"]
    selected = tk.StringVar(value='None')

    tk.OptionMenu(win, selected, *options).pack(pady=5)

    def on_ok():
        handle_choice(selected.get())
        win.destroy()

    tk.Button(win, text='OK', width=10, command=on_ok).pack(side="left", padx=30, pady=10)
    tk.Button(win, text="Cancel", width=10, command=win.destroy).pack(side='right', padx=30, pady=10)

def handle_choice(choice):
    if choice == "Undo Last":
        print("Undo Last")
    elif choice == "Undo All":
         print("Undo All")

def shake_window(win):

    x, y = win.winfo_x(), win.winfo_y()
    delta = 2
    for _ in range(2):
        win.geometry(f"+{x + delta}+{y}")
        win.update()
        win.after(10)
        win.geometry(f"+{x - delta}+{y}")
        win.update()
        win.after(10)

    win.geometry(f"+{x}+{y}")

def main():
    root = tk.Tk()
    main.root = root
    root.title("File Organizer")
    root.geometry("400x300")
    root.resizable(False, False)

    tk.Label(root, text="Select folder to organize", font=("Arial",12)).pack(pady=10)

    entry_box = tk.Entry(root, width=40)
    entry_box.pack()

    tk.Button(root, text="Browse").pack(pady=5)

    status_label = tk.Label(root, text="", font=("Arial",10))
    status_label.pack(pady=10)

    tk.Button(
        root, text="Organize File", fg="black", bg="#4CAF50"
    ).pack(pady=5)

    tk.Button(root, text="Unod last moved", bg="red", fg="white", command=lambda: show_undo_dialog()).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()