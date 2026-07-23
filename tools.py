#!/usr/bin/env python3
"""
Terminal Challenge Toolkit - Hub for terminal-only challenges
Run: python tools.py
"""

import os
import sys
import subprocess
import json
import datetime
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "config.json"

DEFAULT_CONFIG = {
    "editor": "notepad",
    "notes_dir": str(Path.home() / "terminal-notes"),
    "theme": "dark"
}

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    save_config(DEFAULT_CONFIG)
    return DEFAULT_CONFIG

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def print_header():
    print("""
+========================================================+
|       TERMINAL CHALLENGE TOOLKIT                       |
|   Everything through the terminal, no GUI needed!      |
+========================================================+
    """)

def print_menu():
    print("  FILES & DIRECTORIES:")
    print("    1. ls/list     - List files")
    print("    2. find        - Search for files")
    print("    3. tree        - Directory tree")
    print("    4. diff        - Compare files")
    print()
    print("  NOTES:")
    print("    5. note        - Create/read a note")
    print("    6. notes       - List notes")
    print("    7. todo        - Task manager")
    print()
    print("  SYSTEM:")
    print("    8. sysinfo     - System info")
    print("    9. processes   - Running processes")
    print("   10. disk        - Disk usage")
    print("   11. network     - Network info")
    print()
    print("  TOOLS:")
    print("   12. edit        - Open file in editor")
    print("   13. search      - Search in files (grep)")
    print("   14. history     - Command history")
    print("   15. calc        - Calculator")
    print("   16. color       - Change terminal color")
    print("   17. battle      - AI Battle (two AIs debate)")
    print("   18. sysmon      - System monitor (real-time)")
    print("   19. password    - Password generator")
    print("   20. hash        - Hash tool")
    print("   21. encode      - Encoder/Decoder")
    print("   22. timer       - Timer & Stopwatch")
    print("   23. json        - JSON tool")
    print("   24. net         - Network tool")
    print("   25. git         - Git helper")
    print("   26. filetool    - File operations")
    print()
    print("    0. quit         - Exit")
    print()

def cmd_ls():
    path = input("Path (Enter = current): ").strip() or "."
    try:
        items = list(Path(path).iterdir())
        print(f"\n  {Path(path).absolute()}\n")
        for item in sorted(items, key=lambda x: x.name.lower()):
            prefix = "[DIR] " if item.is_dir() else "[FILE]"
            size = ""
            if item.is_file():
                size = f" ({item.stat().st_size:,} B)"
            print(f"  {prefix} {item.name}{size}")
        print(f"\n  {len(items)} items")
    except Exception as e:
        print(f"Error: {e}")

def cmd_find():
    pattern = input("Pattern (e.g. *.py): ").strip()
    root = input("Where to search (Enter = .): ").strip() or "."
    try:
        matches = list(Path(root).rglob(pattern))
        print(f"\n  Found {len(matches)} files:\n")
        for m in matches[:50]:
            print(f"  {m}")
        if len(matches) > 50:
            print(f"  ... and {len(matches) - 50} more")
    except Exception as e:
        print(f"Error: {e}")

def cmd_tree():
    path = input("Path (Enter = .): ").strip() or "."
    try:
        subprocess.run(["tree", "/F", "/A", path], shell=True)
    except:
        print("tree not available, try: dir /s /b")

def cmd_diff():
    f1 = input("File 1: ").strip()
    f2 = input("File 2: ").strip()
    try:
        subprocess.run(["diff", f1, f2])
    except FileNotFoundError:
        subprocess.run(["fc", f1, f2])

def cmd_note():
    notes_dir = Path(load_config()["notes_dir"])
    notes_dir.mkdir(exist_ok=True)
    
    print("1. New note")
    print("2. Read note")
    choice = input("Choice: ").strip()
    
    if choice == "1":
        name = input("Name: ").strip()
        if not name:
            return
        if not name.endswith(".txt"):
            name += ".txt"
        note_file = notes_dir / name
        print(f"Writing to: {note_file}")
        print("Type 'END' on a new line when done:")
        
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        
        with open(note_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print("Saved!")
    
    elif choice == "2":
        name = input("Note name: ").strip()
        if not name.endswith(".txt"):
            name += ".txt"
        note_file = notes_dir / name
        if note_file.exists():
            print(f"\n--- {note_file.name} ---\n")
            print(note_file.read_text(encoding="utf-8"))
        else:
            print("Note not found")

def cmd_notes():
    notes_dir = Path(load_config()["notes_dir"])
    if not notes_dir.exists():
        print("No notes yet")
        return
    
    notes = list(notes_dir.glob("*.txt"))
    print(f"\n  Notes ({len(notes)}):\n")
    for note in sorted(notes, key=lambda x: x.stat().st_mtime, reverse=True):
        mtime = datetime.datetime.fromtimestamp(note.stat().st_mtime)
        print(f"  {note.name:30}  ({mtime.strftime('%Y-%m-%d %H:%M')})")

def cmd_todo():
    todo_file = Path(load_config()["notes_dir"]) / "todo.txt"
    todo_file.parent.mkdir(exist_ok=True)
    
    print("1. Add task")
    print("2. View tasks")
    print("3. Remove completed")
    choice = input("Choice: ").strip()
    
    if choice == "1":
        task = input("Task: ").strip()
        if task:
            with open(todo_file, "a", encoding="utf-8") as f:
                f.write(f"[ ] {task}\n")
            print("Added!")
    
    elif choice == "2":
        if todo_file.exists():
            print("\n  TODO:\n")
            print(todo_file.read_text(encoding="utf-8"))
        else:
            print("No tasks")
    
    elif choice == "3":
        if todo_file.exists():
            lines = todo_file.read_text(encoding="utf-8").splitlines()
            for i, line in enumerate(lines, 1):
                print(f"  {i}. {line}")
            num = input("Number to remove: ").strip()
            try:
                idx = int(num) - 1
                if 0 <= idx < len(lines):
                    removed = lines.pop(idx)
                    todo_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
                    print(f"Removed: {removed}")
            except ValueError:
                print("Invalid number")

def cmd_sysinfo():
    import platform
    import psutil
    print("\n  SYSTEM:\n")
    print(f"  OS:           {platform.system()} {platform.release()}")
    print(f"  Version:      {platform.version()}")
    print(f"  Computer:     {platform.node()}")
    print(f"  Processor:    {platform.processor()}")
    print(f"  Python:       {platform.python_version()}")
    
    mem = psutil.virtual_memory()
    print(f"\n  MEMORY:")
    print(f"  Total:        {mem.total // (1024**3)} GB")
    print(f"  Used:         {mem.percent}%")
    print(f"  Free:         {mem.available // (1024**3)} GB")
    
    cpu = psutil.cpu_percent(interval=1)
    print(f"\n  CPU:          {cpu}%")

def cmd_processes():
    import psutil
    procs = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            procs.append(proc.info)
        except:
            pass
    
    procs.sort(key=lambda x: x['memory_percent'] or 0, reverse=True)
    print(f"\n  TOP PROCESSES (of {len(procs)} total):\n")
    print(f"  {'PID':>6}  {'CPU%':>5}  {'MEM%':>6}  Name")
    print("  " + "-" * 50)
    for p in procs[:15]:
        print(f"  {p['pid']:>6}  {p['cpu_percent'] or 0:>5.1f}  {p['memory_percent'] or 0:>6.1f}  {p['name']}")

def cmd_disk():
    import psutil
    print("\n  DISKS:\n")
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            bar_len = 30
            used = int(usage.percent / 100 * bar_len)
            bar = "#" * used + "-" * (bar_len - used)
            print(f"  {part.device:6}  {part.mountpoint:4}")
            print(f"         [{bar}] {usage.percent}%")
            print(f"         {usage.used // (1024**3)} GB / {usage.total // (1024**3)} GB\n")
        except:
            pass

def cmd_network():
    import psutil
    print("\n  NETWORK:\n")
    addrs = psutil.net_if_addrs()
    stats = psutil.net_io_counters()
    print(f"  Total sent:     {stats.bytes_sent // (1024**2):,} MB")
    print(f"  Total received: {stats.bytes_recv // (1024**2):,} MB")
    print(f"  Packets sent:   {stats.packets_sent:,}")
    print(f"  Packets recv:   {stats.packets_recv:,}")
    print(f"\n  Interfaces:")
    for name, addrs_list in addrs.items():
        for a in addrs_list:
            if a.family.name == 'AF_INET':
                print(f"    {name}: {a.address}")

def cmd_edit():
    config = load_config()
    file = input("File: ").strip()
    editor = config.get("editor", "notepad")
    print(f"Opening {file} in {editor}...")
    subprocess.run([editor, file])

def cmd_search():
    pattern = input("Regex/pattern: ").strip()
    path = input("Path (Enter = .): ").strip() or "."
    try:
        result = subprocess.run(
            ["rg", pattern, path, "-n", "--color", "never"],
            capture_output=True, text=True
        )
        if result.stdout:
            print(result.stdout)
        else:
            print("Nothing found")
    except FileNotFoundError:
        print("rg not available, try: findstr /s /n " + pattern + " " + path)

def cmd_history():
    ps_hist = Path(os.environ.get("USERPROFILE", ".")) / "AppData/Roaming/Microsoft/Windows/PowerShell/PSReadLine/ConsoleHost_history.txt"
    if ps_hist.exists():
        lines = ps_hist.read_text(encoding="utf-8", errors="ignore").splitlines()
        print(f"\n  Last 30 commands:\n")
        for line in lines[-30:]:
            print(f"  {line}")
    else:
        print("History not found")

def cmd_calc():
    print("Calculator (enter expression, Enter = calculate)")
    print("  Operations: + - * / ** // %")
    while True:
        expr = input(">>> ").strip()
        if expr.lower() in ("quit", "exit", "q"):
            break
        try:
            result = eval(expr)
            print(f"  = {result}")
        except Exception as e:
            print(f"  Error: {e}")

def cmd_color():
    print("Terminal colors:")
    print("1. White (default)")
    print("2. Green (Matrix)")
    print("3. Red (Hacker)")
    print("4. Yellow (Retro)")
    print("5. Cyan (Cyber)")
    choice = input("Choice: ").strip()
    
    colors = {
        "1": "0F",
        "2": "0A",
        "3": "0C",
        "4": "0E",
        "5": "0B",
    }
    
    color = colors.get(choice, "0F")
    if os.name == "nt":
        os.system(f"color {color}")
    else:
        print("(Windows only)")

def cmd_battle():
    print("Starting AI Battle...")
    battle_path = Path(__file__).parent / "ai_battle.py"
    subprocess.run(["python", str(battle_path)])

def cmd_sysmon():
    print("Starting System Monitor...")
    sysmon_path = Path(__file__).parent / "sysmon.py"
    subprocess.run(["python", str(sysmon_path)])

def cmd_password():
    print("Starting Password Generator...")
    pw_path = Path(__file__).parent / "password_gen.py"
    subprocess.run(["python", str(pw_path)])

def cmd_hash():
    print("Starting Hash Tool...")
    hash_path = Path(__file__).parent / "hash_tool.py"
    subprocess.run(["python", str(hash_path)])

def cmd_encode():
    print("Starting Encoder/Decoder...")
    enc_path = Path(__file__).parent / "encoder.py"
    subprocess.run(["python", str(enc_path)])

def cmd_timer():
    print("Starting Timer...")
    timer_path = Path(__file__).parent / "timer.py"
    subprocess.run(["python", str(timer_path)])

def cmd_json():
    print("Starting JSON Tool...")
    json_path = Path(__file__).parent / "json_tool.py"
    subprocess.run(["python", str(json_path)])

def cmd_net():
    print("Starting Network Tool...")
    net_path = Path(__file__).parent / "net_tool.py"
    subprocess.run(["python", str(net_path)])

def cmd_git():
    print("Starting Git Helper...")
    git_path = Path(__file__).parent / "git_helper.py"
    subprocess.run(["python", str(git_path)])

def cmd_filetool():
    print("Starting File Tool...")
    ft_path = Path(__file__).parent / "file_tool.py"
    subprocess.run(["python", str(ft_path), "--help"])

def main():
    while True:
        clear()
        print_header()
        print_menu()
        
        choice = input(">> Choice: ").strip()
        
        if choice == "0" or choice.lower() == "quit":
            print("\nGoodbye! Good luck with the challenge!\n")
            break
        elif choice == "1":
            cmd_ls()
        elif choice == "2":
            cmd_find()
        elif choice == "3":
            cmd_tree()
        elif choice == "4":
            cmd_diff()
        elif choice == "5":
            cmd_note()
        elif choice == "6":
            cmd_notes()
        elif choice == "7":
            cmd_todo()
        elif choice == "8":
            cmd_sysinfo()
        elif choice == "9":
            cmd_processes()
        elif choice == "10":
            cmd_disk()
        elif choice == "11":
            cmd_network()
        elif choice == "12":
            cmd_edit()
        elif choice == "13":
            cmd_search()
        elif choice == "14":
            cmd_history()
        elif choice == "15":
            cmd_calc()
        elif choice == "16":
            cmd_color()
        elif choice == "17":
            cmd_battle()
        elif choice == "18":
            cmd_sysmon()
        elif choice == "19":
            cmd_password()
        elif choice == "20":
            cmd_hash()
        elif choice == "21":
            cmd_encode()
        elif choice == "22":
            cmd_timer()
        elif choice == "23":
            cmd_json()
        elif choice == "24":
            cmd_net()
        elif choice == "25":
            cmd_git()
        elif choice == "26":
            cmd_filetool()
        else:
            print("Invalid choice!")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
