import os
import sys
import shutil
import platform
import time
import random
import datetime
import hashlib

# ===============================
#      STORAGE CONFIG
# ===============================
SYSTEM = platform.system()

def make_paths(name: str = None):
    if SYSTEM == "Windows":
        rootpath = os.environ.get('USERPROFILE')
    else:
        rootpath = os.path.expanduser("~")

    if name is None:
        return rootpath

    root = os.path.join(rootpath, name)
    os.makedirs(root, exist_ok=True)
    return root

ROOT_PATH = make_paths()
USERS_BASE = os.path.join(ROOT_PATH, "users")
SYSTEM_PATH = os.path.join(ROOT_PATH, "system")
CTRL_PASSWORD_FILE = os.path.join(SYSTEM_PATH, "control_password.txt")
INSTALL_FLAG = os.path.join(SYSTEM_PATH, "installed.txt")
NAME_FILE = os.path.join(SYSTEM_PATH, "SystemComputerName.txt")
CID_FILE = os.path.join(SYSTEM_PATH, "SystemComputerID.id")

MAX_STORAGE = 15 * 1024 * 1024

def get_folder_size(path):
    total = 0
    for root, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            if os.path.exists(fp):
                total += os.path.getsize(fp)
    return total

def has_space(extra_bytes=0):
    used = get_folder_size(USER_PATH)
    return (used + extra_bytes) <= MAX_STORAGE

os.makedirs(USERS_BASE, exist_ok=True)
os.makedirs(SYSTEM_PATH, exist_ok=True)
os.path.exists(NAME_FILE)
os.path.exists(CID_FILE)

# ===============================
#          VARIABLES
# ==============================
CURRENT_USER = None
USER_PATH = None
current_dir = ROOT_PATH

# ===============================
#          ERRORS
# ===============================
class FileMoveError(Exception):
    pass

class RenameError(Exception):
    pass

class ReplaceError(Exception):
    pass

# ===============================
#          LICENSE AGREEMENT
# ===============================
def license_agreement():
    """Display the license agreement and ask for acceptance."""
    print("\n=== PyTextOS License Agreement ===\n")
    print("""
PyTextOS - End User License Agreement (EULA)

1. Usage
PyTextOS is provided as a personal, and educational
operating syatem. You may use, modify, and experiment
with the system freely. 

2. Responsibility
You are responsible for any data created, modified,
or deleted within PyTextOS. The developers are not
responsible or liable for any data loss.

3. Warranty
PyTextOS is provided "as is", without any guarantees
of performance, stability, or fitness for any purpose.
Damaging your syatem where it cannot be repaired will
void the warranty.

4. Restrictions
You may not use PyTextOS for harmful, illegal, or
malicious activities. Do no redistribute an exact
copy of the source code. You can distribute the
hardware that is running this OS.

5. Data Storage
All files are stored locally on your device within
the PyTextOS directory and will not interfere with
your other non-PyTextOS files.

6. Data Collection
PyTextOS does not collect any personal information
and files from the user.

7. Termination
Failure to follow this agreement may result in loss
of access to your data.

----------------------------------------

Type 'accept' to agree or 'decline' to cancel installation.
""")
    while True:
        choice = input(">>> ").strip().lower()
        if choice == "accept":
            print("[OK] License accepted.\n")
            return True
        elif choice == "decline":
            print("[SYSTEM] Installation cancelled.")
            os.system('cls' if os.name == 'nt' else 'clear')
            time.sleep(4)
            return False
        else:
            print("Please type 'accept' or 'decline'.")

# ===============================
#          INSTALLER
# ===============================
def installer():
    """Full installation flow for PyTextOS."""
    print("PyTextOS is loading boot files...")
    time.sleep(1)
    print("Preparing installer...")
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Starting PyTextOS installation setup...\n")
    time.sleep(1)
    print("Loading system installer...")
    time.sleep(20)
    print("Initializing directories...")
    time.sleep(30)
    os.makedirs(USERS_BASE, exist_ok=True)
    print("Formatting root...")
    progress_bar(1, 23)
    print("\nPartitioning root...")
    progress_bar(4, 25)

    print("The root folder is where your system lives.")
    while True:
        location = input("Name your root folder: ")
        if location:
            make_paths(location)
            print("Path created!")
            break
        else:
            print("[ERROR] Enter a name: ")
    os.system('cls' if os.name == 'nt' else 'clear')
    pc_name = input("Name your computer: ").strip()
    confirm_name = input("Confirm your computer name: ")
    if confirm_name == pc_name:
        name_file(pc_name)
    else:
        if not pc_name:
            print("[ERROR] PLease enter a computer name")
        if not confirm_name == pc_name:
            print("[ERROR] Names do not match")

    while not license_agreement():
        print("\nYou must accept the license to install PyTextOS.\n")
        time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== PyTextOS Account Setup ===")
    users = []
    print("\nCreate an account for who will use this PyTextOS")

    while len(users) < 10:
        username = input(f"Create user {len(users)+1}/8: ").strip()
        if username == "":
            if len(users) == 0:
                print("[ERROR] You must create at least one user.")
            elif len(users) == 1:
                print("Account created:")
            else:
                print("Accounts created:")
            if len(users) > 1:
                for acc in users:
                    print(f"— {acc}")
        if username in users or os.path.exists(os.path.join(USERS_BASE, username)):
            print("[ERROR] Account already exists")
            continue
        users.append(username)

    for user in users:
        os.makedirs(os.path.join(USERS_BASE, user), exist_ok=True)
        print("")

    for user in users:
        password = input(f"Create a password for {user}: ").strip()
        with open(get_password_file(user), "w") as f:
            f.write(hash_password(password))
        print(f"[OK] Password was set for '{user}'")
    print("\n=== Set control password for account management ===\n")

    while True:
        ctrl_pass = input("Enter your control panel password: ").strip()
        confirm_pass = input("Confirm your control panel password: ").strip()
        if confirm_pass == ctrl_pass:
            with open(CTRL_PASSWORD_FILE, "w") as f:
                f.write(hash_password(ctrl_pass))
            print("[OK] Control password set")
            break
        else:
            print("[ERROR] Passwords do not match")

    print("\nPyTextOS is preparing your system...")
    progress_bar(1, 34)
    print("Finalizing setup...")
    progress_bar(5, 23)

    mark_installed()
    print("\n[SYSTEM] Installation complete!\n")
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')
    input("Your PyTextOS is ready to use!\nPress any key to continue...")

# ===============================
#          HELPERS
# ===============================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_password_file(username):
    user_data_path = os.path.join(SYSTEM_PATH, "UserData")
    os.makedirs(user_data_path, exist_ok=True)
    return os.path.join(user_data_path, f"password_{username}.usdt")

def list_users():
    return sorted(os.listdir(USERS_BASE))

def mark_installed():
    open(INSTALL_FLAG, "w").close()

def is_installed():
    return os.path.exists(INSTALL_FLAG)

def name_file(name):
    with open(NAME_FILE, "w") as f:
        f.write(name)

def read_name():
    with open(NAME_FILE, "r") as f:
        data = f.read()
    return data

def read_id():
    with open(CTRL_PASSWORD_FILE, "r") as f:
        data = f.read()
    with open(CID_FILE, "w") as f:
        f.write(data)
    return data

def progress_bar(min_time, max_time):
    if min_time > max_time:
        total_time = random.uniform(max_time, min_time)
        return
    total_time = random.uniform(min_time, max_time)
    steps = 20
    delay = total_time / steps
    for i in range(steps + 1):
        filled = int((i / steps) * 10)
        bar = "#" * filled + "—" * (10 - filled)
        percent = int((i / steps) * 100)
        sys.stdout.write(f"\r{bar} {percent}%")
        sys.stdout.flush()
        time.sleep(delay)

# ===============================
#          ACCOUNT CONTROL PANEL
# ===============================
def acc_ctrl_panel():
    """Control panel to manage user accounts."""
    if os.path.exists(CTRL_PASSWORD_FILE):
        entered = input("Enter control password: ").strip()
        saved = open(CTRL_PASSWORD_FILE).read().strip()
        if hash_password(entered) != saved:
            print("[ERROR] Access denied")
            return

    while True:
        users = list_users()
        print("\n--- User Account Control Panel ---")
        if not users:
            print("\nNo Accounts found.")
        else:
            print("\nUser accounts:")
            for i, user in enumerate(users, start=1):
                print(f"  [{i}] {user}")

        print("\nOptions:")
        print("c - create user")
        print("q - quit")
        choice = input("Select user or option: ").strip()

        if choice == "q":
            break

        elif choice == "c":
            new_user = input("Enter new username: ").strip()
            if not new_user or os.path.exists(os.path.join(USERS_BASE, new_user)):
                print("[ERROR] Invalid or existing username")
                continue
            if len(os.listdir(USERS_BASE)) > 8:
                print("[ERROR] Too many accounts. You can only have a maximum of 8 accounts.")
            os.makedirs(os.path.join(USERS_BASE, new_user))
            password = input("Enter new password: ").strip()
            with open(get_password_file(new_user), "w") as f:
                f.write(hash_password(password))
            print(f"[SYSTEM] Account '{new_user}' created!")

        elif choice.isdigit():
            idx = int(choice)-1
            if not (0 <= idx < len(users)):
                print("[ERROR] Invalid selection")
                continue
            target = users[idx]
            print(f"\nSelected account: {target}")
            print("What will you do with this account?")
            print("d - delete")
            print("f - format (deletes user files)")
            print("c - change password")
            print("b - back")
            action = input("Action: ").strip()
            path = os.path.join(USERS_BASE, target)

            if action == "d":
                confirm = input(f"Delete '{target}'? (y/n): ").lower()
                if confirm == "y":
                    shutil.rmtree(path)
                    pw_file = get_password_file(target)
                    if os.path.exists(pw_file):
                        os.remove(pw_file)
                    print(f"[OK] '{target}' deleted!")

            elif action == "f":
                confirm = input(f"Format ALL files of '{target}'? (y/n): ").lower()
                if confirm == "y":
                    shutil.rmtree(path)
                    os.makedirs(path)
                    print(f"[SYSTEM] '{target}' formatted!")

            elif action == "c":
                new_pass_word = input("Enter new password: ").strip()
                confirm_pass = input(f"Confirm action? (y/n): ").lower()
                if confirm_pass == "y":
                    if new_pass_word:
                        with open(get_password_file(target), "w") as f:
                            f.write(hash_password(new_pass_word))
                        print("Password changed")

                    else:
                        print("[ERROR] Please enter a password")

            elif action == "b":
                continue

            else:
                print("[ERROR] Invalid action")

        else:
            print("[ERROR] Invalid input")

# ===============================
#          LOGIN
# ===============================
def login():
    global USER_PATH, CURRENT_USER
    users = list_users()
    print("\nAccounts:")
    for i, u in enumerate(users, start=1):
        print(f"  {i}. {u}")

    while True:
        choice = input("\nSelect account: ").strip()
        if choice.isdigit():
            username = users[int(choice)-1]
        else:
            username = choice

        USER_PATH = os.path.join(USERS_BASE, username)
        pw_file = get_password_file(username)
        CURRENT_USER = username

        login_msgs = [
            f"Welcome back, {CURRENT_USER}!",
            f"Hey, {CURRENT_USER}! How is your day?",
            f"Hi, {CURRENT_USER}. Lets start!",
            f"Hello, {CURRENT_USER}. Ready to browse your files?",
            f"{CURRENT_USER}! Nice to see you back here!",
            f"Its you again, {CURRENT_USER}!",
            "Its you again! Hows it going?",
        ]
        msg = random.choice(login_msgs)
        print(msg)

        for _ in range(3):
            pw = input("Enter your password: ")
            if hash_password(pw) == open(pw_file).read():
                print("[OK] Login successful\n")
                return username, USER_PATH
            else:
                print("[ERROR] Incorrect password")

# ===============================
#          SHELL + APPS
# ===============================
OS_START = time.time()

board = [' ' for _ in range(9)]

def print_board():
    for i in range(0, 9, 3):
        print(f"{board[i]} | {board[i+1]} | {board[i+2]}")
        if i < 6:
            print("--+---+--")

def check_win(player):
    wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    return any(board[a] == board[b] == board[c] == player for a,b,c in wins)

def check_tie():
    return ' ' not in board

def play_game():
    current_player = 'X'
    while True:
        print_board()
        print("""
Board map:
0 1 2
3 4 5
6 7 8
""")
        move = int(input(f"Player {current_player}, enter move (0-8): "))
        if board[move] == ' ':
            board[move] = current_player
            if check_win(current_player):
                print_board()
                print(f"Player {current_player} wins!")
                break
            if check_tie():
                print_board()
                print("It's a tie!")
                break
            current_player = 'O' if current_player == 'X' else 'X'
        else:
            print("Spot taken, try again.")

def calc():
    print("\n--- Calculator ---")
    print("Commands:")
    print("A - Addition        S - Subtraction")
    print("M - Multiplication  D - Division")
    print("E - Exponent        Q - Exit the program") 
    while True:
        cmd = input("> ").strip().lower()
        if cmd in ("a", "s", "m", "d", "q"):
            if cmd == "q":
                return
            try:
                a = float(input("value 1: "))
                b = float(input("value 2: "))
            except ValueError:
                print("[ERROR] Please enter a number.")
                calc()
                return
            if cmd == "a":
                print(f"{a} plus {b} is {a + b}")
            elif cmd == "s":
                print(f"{a} minus {b} is {a - b}")
            elif cmd == "m":
                print(f"{a} times {b} is {a * b}")
            elif cmd == "d":
                if b == 0:
                    print("[ERROR] Cannot divide by zero.")
                else:
                    print(f"{a} divided by {b} is {a / b}")
        elif cmd == "e":
            try:
                base = float(input("Base: "))
                exp = float(input("Exponent: "))
                print(f"{base} to the power of {exp} is {base ** exp}")
            except ValueError:
                print("[ERROR] Invalid number")
        else:
            print("[ERROR] Invalid command")

def virtual_path(path):
    rel = os.path.relpath(path, USER_PATH)
    return "/" if rel == "." else "/" + rel

def tree(path, prefix=""):
    items = sorted(os.listdir(path))
    for i, item in enumerate(items):
        full = os.path.join(path, item)
        connector = "└── " if i == len(items)-1 else "├── "
        print(prefix + connector + item)
        if os.path.isdir(full):
            extension = "    " if i == len(items)-1 else "│   "
            tree(full, prefix + extension)

def execute_cmd_command(cmd):
    global current_dir

    if cmd == "dir":
        for i in os.listdir(current_dir):
            print(i)

    elif cmd.startswith("echo "):
        print(cmd[5:])

    elif cmd == "uptime":
        t = int(time.time() - OS_START)
        print(f"{t}s")

    elif cmd == "datetime":
        print(datetime.datetime.now())

    elif cmd.startswith("mkdir "):
        os.makedirs(os.path.join(current_dir, cmd[6:].strip()), exist_ok=True)

    elif cmd.startswith("cd"):
        parts = cmd.split(maxsplit=1)
        if len(parts) == 1:
            return

        path = parts[1]
        if path == "/":
            new_path = USER_PATH

        elif path == "..":
            new_path = os.path.dirname(current_dir)

        else:
            new_path = os.path.normpath(os.path.join(current_dir, path))

        try:
            if os.path.commonpath([USER_PATH, new_path]) != USER_PATH:
                print("[ERROR] Access denied")
                return
        except:
            print("[ERROR] Invalid path")
            return

        if os.path.isdir(new_path):
            current_dir = new_path

    elif cmd.startswith("del "):
        path = os.path.join(current_dir, cmd[4:])
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.exists(path):
            os.remove(path)

    elif cmd.startswith("read "):
        path = os.path.join(current_dir, cmd[5:] + ".txt")
        if os.path.exists(path):
            print(open(path).read())

    elif cmd == "about":
        print("PyTextOS version 1.p")
        print("PyTextOS CLI Environment 1.0")

    elif cmd == "exit":
        return "exit"

    else:
        print(f"[ERROR] Invalid cmd: {cmd}")

def execute_cmd_line(line):
    parts = [p.strip() for p in line.split(";") if p.strip()]
    for cmd in parts:
        if cmd.startswith("pause(") and cmd.endswith(")"):
            try:
                t = float(cmd[6:-1])
                time.sleep(t)
            except:
                print("[ERROR] Invalid pause. Please enter a number")
            continue
        result = execute_cmd_command(cmd)
        if result == "exit":
            return "exit"

def run_cmd_script(path):
    global current_dir

    with open(path, "r") as f:
        lines = f.readlines()
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("//"):
            i += 1
            continue

        if line.startswith("["):
            block = []
            if line == "[":
                i += 1
                while i < len(lines) and lines[i].strip() != "]":
                    block.append(lines[i].strip())
                    i += 1
                i += 1
                repeat_line = lines[i-1].strip()

            else:
                content, repeat = line.split("]")
                content = content[1:]
                repeat = int(repeat.strip())
                block = [content]
                for _ in range(repeat):
                    for b in block:
                        execute_cmd_line(b)
                i += 1
                continue

            if lines[i-1].strip().startswith("]"):
                try:
                    repeat = int(lines[i-1].strip()[1:])
                except:
                    print("[ERROR] Invalid loop count")
                    return

            else:
                repeat = 1

            for _ in range(repeat):
                for b in block:
                    execute_cmd_line(b)
            continue
        execute_cmd_line(line)
        i += 1

def help_menu():
    print("""
HELP MENU

Here are the list of commands you can use in PyTextOS.

COMMAND          DESCRIPTION
dir / ls         list items in directory
cd <path>        change directory
mkdir <name>     create a folder
del <item>       delete item
txt <name>       create blank text file
write <name>     overwrite contents of a file
read <name>      print text file
append <name>    add text to a file
echo <text>      echo text
uptime           show how long system is running
datetime         display date and time
about            display system information
cls              clear screen
restart          restart
exit             shutdown PyTextOS
calc             calculator
mkcmd            create a .cmd file
run <file.cmd>   execute a .cmd file

SCRIPT COMMANDS:
dir         exit    about
echo        mkdir   read
uptime      cd
datetime    del
""")

def main():
    global current_dir, USERS_BASE

    print(f"Welcome to PyTextOS, {CURRENT_USER}!")

    while True:
        cmd = input(f"{CURRENT_USER}@PyTextOS{virtual_path(current_dir)}> ").strip().lower()

        if not cmd:
            pass
        if cmd in ("dir", "ls"):
            print(f"\nContents of {virtual_path(current_dir)}:\n")
            for i in os.listdir(current_dir):
                tag = "[DIR]" if os.path.isdir(os.path.join(current_dir, i)) else "[FILE]"
                print(f"{i:21} {tag}")
            print("\n")

        elif cmd == "calc":
            calc()

        elif cmd == "help":
            help_menu()

        elif cmd == "tictactoe":
            play_game()

        elif cmd == "computer":
            print("Computer name:", read_name())
            print("Computer ID:", read_id())

        elif cmd == "about":
            os_name = "PyTextOS"
            os_version = "1.0"
            os_ram = "16 KB"
            content_count = len(os.listdir(current_dir))
            now = datetime.datetime.now()
            elapsed = int(time.time() - OS_START)
            hours = elapsed // 3600
            minutes = (elapsed % 3600) // 60
            seconds = elapsed % 60
            uptime = f"{hours:02}:{minutes:02}:{seconds:02}"

            print("======== PyTextOS System Info ========")
            print("OS Name:", os_name)
            print("OS Version:", os_version)
            print("OS RAM:", os_ram)
            print("=========== SESSION INFO =============")
            print(f"Current Location: {virtual_path(current_dir)}/")
            print("Total items in current directory:", content_count)
            print("System boot time:", OS_START)
            print("System uptime:", uptime)
            print("Time now:", now.strftime("%H:%M:%S"))
            print("======================================")

        elif cmd.startswith("echo "):
            text = cmd[5:]

            if text.endswith(" /u"):
                print(text[:-3].upper())

            elif text.endswith(" /l"):
                print(text[:-3].lower())

            elif text.endswith(" /s"):
                print(text[:-3].swapcase())

            else:
                print(text)

        elif cmd.startswith("mkcmd "):
            name = cmd.split(maxsplit=1)[1].strip()
            if not name.endswith(".cmd"):
                name += ".cmd"

            path = os.path.join(current_dir, name)
            print("=== COMMAND SCRIPT EDITOR ===")
            print("Enter your .cmd script. Type ':cmd.end' on a new line to finish.\n")
            lines = []

            while True:
                line = input()
                if line.strip() == ":cmd.end":
                    break
                lines.append(line)

            content = "\n".join(lines)
            if not has_space(len(content.encode())):
                print("[ERROR] Not enough storage")
                continue
            with open(path, "w") as f:
                f.write(content)
            print(f"[OK] Created {name}")

        elif cmd.startswith("cd"):
            parts = cmd.split(maxsplit=1)
            if len(parts) == 1:
                print(virtual_path(current_dir))
                continue
            path = parts[1]

            if path == "/":
                new_path = USER_PATH

            elif path == "..":
                new_path = os.path.dirname(current_dir)

            else:
                new_path = os.path.normpath(os.path.join(current_dir, path))

            try:
                if os.path.commonpath([USER_PATH, new_path]) != USER_PATH:
                    print("[ERROR] Access denied")
                    continue
            except:
                print("[ERROR] Invalid path")
                continue

            if os.path.isdir(new_path):
                current_dir = new_path
            else:
                print("[ERROR] Path not found")

        elif cmd.startswith("mkdir "):
            if not has_space(1024):
                print("[ERROR] Storage full!")
                continue
            os.makedirs(os.path.join(current_dir, cmd[6:]))

        elif cmd.startswith("txt "):
            if not has_space(1024):
                print("[ERROR] Storage full!")
                continue
            open(os.path.join(current_dir, cmd[4:] + ".txt"), "w").close()

        elif cmd.startswith("write "):
            path = os.path.join(current_dir, cmd[6:] + ".txt")
            if not os.path.exists(path):
                print("[ERROR] File not found")
                continue
            lines = []
            print("=== TEXT EDITOR ===")
            print("Type :save to exit\n")

            while True:
                line = input()
                if line == ":save":
                    break
                lines.append(line)

            content = "\n".join(lines) + "\n"
            if not has_space(len(content.encode())):
                print("[ERROR] Not enough storage!")
                continue
            open(path, "w").write(content)

        elif cmd.startswith("append "):
            path = os.path.join(current_dir, cmd[7:] + ".txt")
            if not os.path.exists(path):
                print("[ERROR] File not found")
                continue
            print("=== TEXT EDITOR ===")
            print("Type :save to exit\n")
            lines = []

            while True:
                line = input()
                if line == ":save":
                    break
                lines.append(line)
            content = "\n".join(lines) + "\n"

            if not has_space(len(content.encode())):
                print("[ERROR] Not enough storage!")
                continue
            with open(path, "a") as f:
                f.write(content)

        elif cmd.startswith("read "):
            path = os.path.join(current_dir, cmd[5:] + ".txt")
            if os.path.exists(path):
                print(open(path).read())

        elif cmd.startswith("del "):
            path = os.path.join(current_dir, cmd[4:])
            if os.path.isdir(path):
                shutil.rmtree(path)
            elif os.path.exists(path):
                os.remove(path)
            else:
                print("[ERROR] No path given")

        elif cmd == "tree":
            tree(current_dir)

        elif cmd in ("format", "rm -root -clear"):
            if input("Are you sure you want to format (y/n): ") == "y":
                shutil.rmtree(USER_PATH)
                os.makedirs(USER_PATH)
                current_dir = USER_PATH
                print("Format successful!")

        elif cmd == "uptime":
            t = int(time.time() - OS_START)
            print(f"{t//3600}h {(t%3600)//60}m {t%60}s")

        elif cmd == "datetime":
            print(datetime.datetime.now())

        elif cmd.startswith("move "):
            parts = cmd.split(maxsplit=2)
            if len(parts) < 3:
                print("[ERROR] Usage: move <source> <destination>")
                continue

            src = os.path.join(current_dir, parts[1])
            dst = os.path.join(current_dir, parts[2])
            if not os.path.exists(src):
                print("[ERROR] Source not found")
                continue

            try:
                if os.path.commonpath([USER_PATH, os.path.abspath(dst)]) != USER_PATH:
                    print("[ERROR] Access denied")
                    continue
            except:
                print("[ERROR] Invalid destination")
                continue

            if os.path.isdir(dst):
                dst = os.path.join(dst, os.path.basename(src))

            try:
                shutil.move(src, dst)
                print("[OK] Moved")
            except FileMoveError:
                print(f"[ERROR] Cound not move file")

        elif cmd.startswith("rename "):
            parts = cmd.split(maxsplit=2)
            if len(parts) < 3:
                print("[ERROR] Usage: rename <old> <new>")
                continue

            src = os.path.join(current_dir, parts[1])
            dst = os.path.join(current_dir, parts[2])
            if not os.path.exists(src):
                print("[ERROR] File not found")
                continue

            if os.path.exists(dst):
                print("[ERROR] Target already exists")
                continue

            try:
                os.rename(src, dst)
                print("[OK] Renamed", src, "to", dst)
            except RenameError:
                print("[ERROR] Could not rename file")

        elif cmd.startswith("rep "):
            parts = cmd.split(maxsplit=2)
            if len(parts) < 3:
                print("[ERROR] Usage: rep <source.txt> <target.txt>")
                continue

            src = os.path.join(current_dir, parts[1])
            dst = os.path.join(current_dir, parts[2])
            if not os.path.exists(src):
                print("[ERROR] Source file not found")
                continue

            if not os.path.exists(dst):
                print("[ERROR] Target file not found")
                continue

            try:
                data = open(src, "r").read()
                if not has_space(len(data.encode())):
                    print("[ERROR] Not enough storage")
                    continue
                with open(dst, "w") as f:
                    f.write(data)
                os.remove(src)
                print("[OK] Content moved successfully")
            except ReplaceError:
                print("[ERROR] Could not move content")

        elif cmd == "storage":
            used = get_folder_size(USER_PATH)
            print(f"Used space:{used/1024/1024:.2f} MB / 10 MB")
            print(f"{MAX_STORAGE - used/1024/1024:.2f} MB / 10 MB free space")

        elif cmd == "cls":
            os.system('cls' if os.name == "nt" else 'clear')

        elif cmd == "restart":
            return "switch_user"

        elif cmd == "exit":
            return "exit"

        elif cmd == "accounts":
            acc_ctrl_panel()

        elif cmd == "uptime":
            now = datetime.datetime.now()
            elapsed = int(time.time() - OS_START)
            hours = elapsed // 3600
            minutes = (elapsed % 3600) // 60
            seconds = elapsed % 60
            uptime = f"{hours:02}:{minutes:02}:{seconds:02}"
            print("Uptime:", uptime)

        elif cmd == "datetime":
            now = datetime.datetime.now()
            print(now.strftime("Date and time: %B-%d-%Y   %H:%M:%S %p"))

        else:
            print(f"[ERROR] Unknown command: {cmd.split()[0]}. Type 'help' of available commands")

# ===============================
#          BOOT
# ===============================
def boot():
    global CURRENT_USER, USER_PATH, current_dir
    if not is_installed():
        installer()
    print("Starting PyTextOS 1.0...")
    time.sleep(3)

    while True:
        CURRENT_USER, USER_PATH = login()
        current_dir = USER_PATH
        while True:
            result = main()
            if result == "exit":
                sys.exit()
            if result == "switch_user":
                break

if __name__ == "__main__":
    boot()