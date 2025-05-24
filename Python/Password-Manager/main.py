import json
import os

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print('[!] Error: data.json is corrupted or empty. Resetting file....')
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_password(website, username, password):
    data = load_data()
    data[website] = {
        "username": username,
        "password": password
    }
    save_data(data)
    print(f"[✔] Password saved for '{website}'.")

def view_passwords():
    data = load_data()
    if not data:
        print("[!] No passwords saved.")
        return
    for website, creds in data.items():
        print(f"\n🌐 {website}")
        print(f"   👤 Username: {creds['username']}")
        print(f"   🔑 Password: {creds['password']}")

def menu():
    while True:
        print("\n===== PASSWORD MANAGER =====")
        print("1. Add New Password")
        print("2. View Saved Passwords")
        print("3. Exit")
        choice = input("Enter choice (1/2/3): ")

        if choice == "1":
            website = input("Website: ")
            username = input("Username: ")
            password = input("Password: ")
            add_password(website.title(), username, password)

        elif choice == "2":
            view_passwords()

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("[!] Invalid option. Try again.")

if __name__ == "__main__":
    menu()
