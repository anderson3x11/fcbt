import os
from datetime import date
from getpass import getpass
from fcbt.storage import save_vault, load_vault
from fcbt.models import Vault, Entry
from fcbt.generator import generate_password

VAULT_FILE = "vault.dat"

# -- Colors --
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print(f"""{YELLOW}{BOLD}
    ╔══════════════════════════════════════╗
    ║     FIRST CITY BANK AND TRUST        ║
    ║          Password Manager            ║
    ╚══════════════════════════════════════╝{RESET}
    """)

def success(msg):
    print(f"\n  {GREEN}[+]{RESET} {msg}")

def error(msg):
    print(f"\n  {RED}[-]{RESET} {msg}")

def info(msg):
    print(f"\n  {CYAN}[*]{RESET} {msg}")

def prompt_bar():
    print(f"  {DIM}{'─' * 40}{RESET}")

def show_menu(entry_count):
    print(f"  {DIM}Vault: {entry_count} entries{RESET}\n")
    print(f"  {YELLOW}1{RESET}  Search")
    print(f"  {YELLOW}2{RESET}  Add entry")
    print(f"  {YELLOW}3{RESET}  Modify entry")
    print(f"  {YELLOW}4{RESET}  Delete entry")
    print(f"  {YELLOW}5{RESET}  Change master password")
    print(f"  {YELLOW}6{RESET}  Quit")
    print()

def show_entry(e):
    print(f"  {BOLD}{e.service}{RESET}")
    print(f"    Login    : {CYAN}{e.login}{RESET}")
    print(f"    Password : {GREEN}{e.password}{RESET}")
    if e.notes:
        print(f"    Notes    : {e.notes}")
    print(f"    {DIM}Created {e.created_at} | Updated {e.updated_at}{RESET}")

def separator():
    print(f"  {DIM}{'─' * 40}{RESET}")

def main():
    # -- Start --
    clear()
    banner()

    if os.path.exists(VAULT_FILE):
        while True:
            password = getpass(f"  {BOLD}Master password :{RESET} ")
            try:
                vault = load_vault(password, VAULT_FILE)
                success("Vault unlocked.")
                break
            except Exception:
                error("Wrong password. Try again.")
    else:
        print(f"  {DIM}No vault found.{RESET}\n")
        create = input(f"  Create a new vault ? (y/n) : ").strip().lower()
        if create != "y":
            print()
            success("Goodbye !")
            print()
            return
        print()
        while True:
            password = getpass(f"  {BOLD}Choose a master password :{RESET} ")
            confirm = getpass(f"  {BOLD}Confirm master password :{RESET} ")
            if password == confirm:
                break
            error("Passwords don't match. Try again.")
        vault = Vault(entries=[])
        success("New vault created.")

    input(f"\n  {DIM}Press Enter to continue...{RESET}")

    # -- Main loop --
    while True:
        clear()
        banner()
        show_menu(len(vault.entries))

        prompt_bar()
        choice = input(f"  {BOLD}>{RESET} ")

        if choice == "1":
            separator()
            search = input("  Service to search : ").lower()
            results = [e for e in vault.entries if search in e.service.lower()]
            if not results:
                error("No entry found.")
            else:
                print()
                for e in results:
                    show_entry(e)
                    print()

        elif choice == "2":
            separator()
            service = input("  Service : ")
            login = input("  Login : ")
            pwd = input(f"  Password {DIM}(empty to generate){RESET} : ")
            if pwd == "":
                pwd = generate_password()
                info(f"Generated : {GREEN}{pwd}{RESET}")
            notes = input("  Notes : ")
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
            success(f"'{service}' added.")

        elif choice == "3":
            separator()
            search = input("  Service to modify : ").lower()
            results = [e for e in vault.entries if search in e.service.lower()]
            if not results:
                error("No entry found.")
            else:
                print()
                for i, e in enumerate(results):
                    print(f"  {YELLOW}[{i}]{RESET} {e.service} ({e.login})")
                idx = int(input(f"\n  Entry number : "))
                if 0 <= idx < len(results):
                    entry = results[idx]
                    print(f"  {DIM}Leave empty to keep current value.{RESET}")
                    new_login = input(f"  Login ({entry.login}) : ")
                    new_pwd = input(f"  Password ({entry.password}) : ")
                    new_notes = input(f"  Notes ({entry.notes}) : ")
                    if new_login:
                        entry.login = new_login
                    if new_pwd:
                        entry.password = new_pwd
                    if new_notes:
                        entry.notes = new_notes
                    entry.updated_at = date.today().strftime("%Y-%m-%d")
                    success(f"'{entry.service}' updated.")
                else:
                    error("Invalid number.")

        elif choice == "4":
            separator()
            search = input("  Service to delete : ").lower()
            results = [e for e in vault.entries if search in e.service.lower()]
            if not results:
                error("No entry found.")
            else:
                print()
                for i, e in enumerate(results):
                    print(f"  {YELLOW}[{i}]{RESET} {e.service} ({e.login})")
                idx = int(input(f"\n  Entry number : "))
                if 0 <= idx < len(results):
                    entry = results[idx]
                    confirm = input(f"  {RED}Delete '{entry.service}' ? (y/n){RESET} : ")
                    if confirm.lower() == "y":
                        vault.entries.remove(entry)
                        success(f"'{entry.service}' deleted.")
                    else:
                        info("Cancelled.")
                else:
                    error("Invalid number.")

        elif choice == "5":
            separator()
            current = getpass(f"  Current password : ")
            if current != password:
                error("Wrong password.")
            else:
                new_pwd = getpass("  New password : ")
                confirm = getpass("  Confirm new password : ")
                if new_pwd == confirm:
                    password = new_pwd
                    success("Master password changed.")
                else:
                    error("Passwords don't match.")

        elif choice == "6":
            save_vault(vault, password, VAULT_FILE)
            clear()
            banner()
            success("Vault saved. Goodbye !")
            print()
            break

        else:
            error("Invalid choice.")

        input(f"\n  {DIM}Press Enter to continue...{RESET}")


if __name__ == "__main__":
    main()
