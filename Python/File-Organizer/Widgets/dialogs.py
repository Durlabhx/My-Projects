# Widgets/dialogs.py

import tkinter as tk
from tkinter import messagebox, ttk

def show_undo_dialog(callback):
    """Creates a modal undo option dialog box."""

    # Prevent multiple instances of the dialog
    if hasattr(show_undo_dialog, 'win') and show_undo_dialog.win.winfo_exists():
        show_undo_dialog.win.lift()
        show_undo_dialog.win.bell()
        shake_window(show_undo_dialog.win)
        return

    win = tk.Toplevel()
    show_undo_dialog.win = win  # Keep a reference to prevent duplicates

    win.title("Undo Options")
    win.geometry("320x160")
    win.resizable(False, False)
    win.grab_set()

    # --- Dialog Content ---
    tk.Label(win, text="Choose an undo option:", font=("Arial", 12)).pack(pady=(15, 5))

    options = ['Undo All', 'Undo Last']
    selected = tk.StringVar(value=options[1])

    combo_frame = tk.Frame(win)
    combo_frame.pack(pady=5)
    ttk.Label(combo_frame, text="Option: ").pack(side='left', padx=(10, 5))
    ttk.Combobox(combo_frame, textvariable=selected, values=options, state='readonly', width=18).pack(side='left')

    # --- Buttons ---
    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=15)

    def on_ok():
        if selected.get() not in options:
            messagebox.showerror("Error", "Please select an undo option.")
            return
        win.withdraw()
        win.after(50, lambda: [callback(selected.get()), win.destroy()])

    ttk.Button(btn_frame, text="OK", width=12, command=on_ok).pack(side='left', padx=10)
    ttk.Button(btn_frame, text="Cancel", width=12, command=win.destroy).pack(side='right', padx=10)

def shake_window(win):
    """Shake effect for already opened window."""
    x, y = win.winfo_x(), win.winfo_y()
    delta = 6
    for _ in range(4):
        win.geometry(f"+{x+delta}+{y}")
        win.update()
        win.after(30)
        win.geometry(f"+{x-delta}+{y}")
        win.update()
        win.after(30)
    win.geometry(f"+{x}+{y}")
