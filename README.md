# PyTextOS

A lightweight, educational, and command‑line operating system written in Python.  
PyTextOS simulates an OS environment with account management, file operations, scripting, and built‑in apps like a calculator and Tic‑Tac‑Toe.

---

## Features
- Multi‑account system (up to 8 accounts)
- Passwords stored with SHA‑256 hashing (`.usdt` files)
- Control panel for account creation, deletion, formatting, and password changes
- File operations: `mkdir`, `cd`, `del`, `txt`, `write`, `append`, `read`, `move`, `rename`, `rep`
- System commands: `uptime`, `datetime`, `about`, `cls`, `restart`, `exit`
- Built‑in apps:
  - Calculator (`calc`)
  - Tic‑Tac‑Toe (`tictactoe`)
- Command scripting with `.cmd` files
- Tree view of directories (`tree`)
- Storage limit simulation (15 MB per user)

---

## Installation
Run the installer to set up PyTextOS:

```bash
python PyTextOS.py
```

The installer will:
1. Initialize system directories (`users`, `system`)
2. Ask for a root folder name
3. Set computer name and ID
4. Require acceptance of the license agreement
5. Create up to 8 user accounts with passwords
6. Set a control panel password
7. Finalize installation

---

## 🔑 License Agreement
PyTextOS is provided as a **personal and educational operating system**.  
You may use, modify, and experiment freely, but redistribution of the exact source code is restricted.

> “PyTextOS is provided *as is*, without any guarantees of performance, stability, or fitness for any purpose.”

---

## Usage
After installation, log in with your account:

```bash
python PyTextOS.py
```

### Example Commands
```bash
dir             # list items in directory
cd <path>       # change directory
mkdir <name>    # create folder
txt <name>      # create blank text file
write <name>    # overwrite file contents
append <name>   # add text to file
read <name>     # print file contents
del <item>      # delete file/folder
calc            # open calculator
tictactoe       # play Tic-Tac-Toe
mkcmd <file>    # create a .cmd script
run <file.cmd>  # execute a .cmd script
tree            # show directory tree
about           # system info
uptime          # show system uptime
```

---

## Example `.cmd` Script
```cmd
echo Hello World
mkdir test_folder
cd test_folder
txt notes
write notes
:cmd.end
```

---

## System Info Example
Running `about` displays:

```
======== PyTextOS System Info ========
OS Name: PyTextOS
OS Version: 1.0
OS RAM: 16 KB
=========== SESSION INFO =============
Current Location: /
Total items in current directory: 3
System boot time: 1716012345.0
System uptime: 00:12:34
Time now: 11:45:00
======================================
```


## Contributing
Pull requests are welcome!  
For major changes, please open an issue first to discuss what you would like to change.


---

## License
See the included **EULA** in the installer.  
PyTextOS is for **educational and personal use only**.
```
