import json
import os
from Durlabh.encryption import fernet as ft
DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding='UTF-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print('[!] Error: data.json is corrupted or empty. Resetting file....')
        return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding='UTF-8') as f:
        json.dump(data, f, indent=4)

def add_password(website, username, password):
    data = load_data()
    encrypted_password = ft.encrypt(password.encode()).decode()
    data[website] = {
        "username": username,
        "password": encrypted_password
    }
    save_data(data)
    print(f"[✔] Password saved for '{website}'.")

def view_passwords():
    data = load_data()
    if not data:
        print("[!] No passwords saved.")
        return

    websites = list(data.keys())
    print("\n===== SAVED WEBSITES =====")
    for i, site in enumerate(websites, 1):
        print(f"{i}. {site}")

    while True:
        choice = input("\nEnter number to view details (or 'b' to go back): ").strip()
        if choice.lower() == 'b':
            return
        
        if not choice.isdigit():
            print("[!] Please enter a valid number.")
            continue

        index = int(choice)
        if 1 <= index <= len(websites):
            website = websites[index - 1]
            creds = data[website]
            print(f"\n🌐 {website}")
            print(f"   👤 Username: {creds['username']}")
            try:
                decrypted_password = ft.decrypt(creds["password"].encode()).decode()
                print(f"   🔑 Password: {decrypted_password}")
            except Exception:
                print("   🔒 Could not decrypt (corrupted or wrong key)")
                break
        else:
            print("[!] Invalid Selection.")
    return data

def delete_passwords():
    data = view_passwords()
    delete_input = input("Enter Website name to delete: ").strip().title()
    if delete_input in data:
        confirm = input(f"Are you sure you want to delete {delete_input}? (y/n): ").strip().lower()
        if confirm == 'y':
            del data[delete_input]
            save_data(data)
            print(f"[X] Password for '{delete_input}' deleted.")
        else:
            print('[i] Deletion cancelled.')
    else:
        print(f"[!] Website : {delete_input} not found")

def menu():
    while True:
        print("\n===== PASSWORD MANAGER =====")
        print("1. Add New Password")
        print("2. View Saved Passwords")
        print("3. Delete Saved Passwords")
        print("4. Exit")
        choice = input("Enter choice (1/2/3/4): ")

        if choice == "1":
            website = input("Website: ").strip()
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            add_password(website.title(), username, password)

        elif choice == "2":
            view_passwords()

        elif choice == "3":
            delete_passwords()

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("[!] Invalid option. Try again.")

if __name__ == "__main__":
    menu()
