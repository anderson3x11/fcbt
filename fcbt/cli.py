import os
from datetime import date
from getpass import getpass
from fcbt.storage import save_vault, load_vault
from fcbt.models import Vault, Entry

VAULT_FILE = "vault.dat"

print("FIRST CITY BANK AND TRUST")
print("==========================")
password = getpass("Enter your password : ")
if os.path.exists("vault.dat"): 
    print("Vault found !")
    vault = load_vault(password, VAULT_FILE)
else:
    print("No vault found, creating a new one...")
    vault = Vault(entries=[])

print("Welcome to your vault !")

while True:
    print("\nWhat do you want to do ?")
    print("[1] Find a password")
    print("[2] Add an entry")
    print("[3] Modify an entry")
    print("[4] Delete an entry")
    print("[5] Change master password")
    print("[6] Leave")

    choice = input("> ")

    if choice == "1":
        search = input("Service to search : ").lower()
        results = [e for e in vault.entries if search in e.service.lower()]
        if not results:
            print("No entry found.")
        else:
            for i, e in enumerate(results):
                print(f"\n--- {e.service} ---")
                print(f"  Login    : {e.login}")
                print(f"  Password : {e.password}")
                print(f"  Notes    : {e.notes}")
                print(f"  Created  : {e.created_at}")
                print(f"  Updated  : {e.updated_at}")
    elif choice == "2":
        service = input("Service : ")
        login = input("Login : ")
        pwd = input("Password (leave empty to generate) : ")
        if pwd == "":
            from fcbt.generator import generate_password
            pwd = generate_password()
            print(f"Generated password : {pwd}")
        notes = input("Notes : ")
        today = date.today().strftime("%Y-%m-%d")
        entry = Entry(
            service=service,
            login=login,
            password=pwd,
            notes=notes,
            created_at=today,
            updated_at=today,
        )
        vault.entries.append(entry)
        print(f"Entry for '{service}' added !")
    elif choice == "3":
        search = input("Service to modify : ").lower()
        results = [e for e in vault.entries if search in e.service.lower()]
        if not results:
            print("No entry found.")
        else:
            for i, e in enumerate(results):
                print(f"[{i}] {e.service} ({e.login})")
            idx = int(input("Entry number to modify : "))
            if 0 <= idx < len(results):
                entry = results[idx]
                print("Leave empty to keep current value.")
                new_login = input(f"Login ({entry.login}) : ")
                new_pwd = input(f"Password ({entry.password}) : ")
                new_notes = input(f"Notes ({entry.notes}) : ")
                if new_login:
                    entry.login = new_login
                if new_pwd:
                    entry.password = new_pwd
                if new_notes:
                    entry.notes = new_notes
                entry.updated_at = date.today().strftime("%Y-%m-%d")
                print(f"Entry for '{entry.service}' updated !")
            else:
                print("Invalid number.")
    elif choice == "4":
        search = input("Service to delete : ").lower()
        results = [e for e in vault.entries if search in e.service.lower()]
        if not results:
            print("No entry found.")
        else:
            for i, e in enumerate(results):
                print(f"[{i}] {e.service} ({e.login})")
            idx = int(input("Entry number to delete : "))
            if 0 <= idx < len(results):
                entry = results[idx]
                confirm = input(f"Delete '{entry.service}' ? (y/n) : ")
                if confirm.lower() == "y":
                    vault.entries.remove(entry)
                    print(f"Entry for '{entry.service}' deleted !")
                else:
                    print("Cancelled.")
            else:
                print("Invalid number.")
    elif choice == "5":
        current = getpass("Current master password : ")
        if current != password:
            print("Wrong password.")
        else:
            new_pwd = getpass("New master password : ")
            confirm = getpass("Confirm new master password : ")
            if new_pwd == confirm:
                password = new_pwd
                print("Master password changed ! Will be applied on save.")
            else:
                print("Passwords don't match.")
    elif choice == "6":
        save_vault(vault, password, VAULT_FILE)
        print("Vault saved. Goodbye !")
        break
    else:
        print("Invalid choice, try again.")