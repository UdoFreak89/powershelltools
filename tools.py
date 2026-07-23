#!/usr/bin/env python3
"""
Terminal Challenge Toolkit - Hub pro terminal-only challenge
Spust: python tools.py
"""

import os
import sys
import subprocess
import json
import datetime
from pathlib import Path

TOOLS_DIR = Path(__file__).parent / "tools"
CONFIG_FILE = Path(__file__).parent / "config.json"

# Default config
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
╔══════════════════════════════════════════════════╗
║       TERMINAL CHALLENGE TOOLKIT                 ║
║       Vše přes terminál, žádné GUI!              ║
╚══════════════════════════════════════════════════╝
    """)

def print_menu():
    print("📁 SOUBORY A ADRESÁŘE:")
    print("   1. ls/list     - Seznam souborů")
    print("   2. find        - Hledat soubory")
    print("   3. tree        - Stromová struktura")
    print("   4. diff        - Porovnat soubory")
    print()
    print("📝 POZNÁMKY:")
    print("   5. note        - Vytvořit/číst poznámku")
    print("   6. notes       - Seznam poznámek")
    print("   7. todo        - Správa úkolů")
    print()
    print("🖥️  SYSTÉM:")
    print("   8. sysinfo     - Info o systému")
    print("   9. processes   - Běžící procesy")
    print("  10. disk        - Využití disku")
    print("  11. network     - Síťové info")
    print()
    print("🔧 NÁSTROJE:")
    print("  12. edit        - Upravit soubor v terminálu")
    print("  13. ide         - Terminal IDE (VS Code v terminálu)")
    print("  14. search      - Hledat ve souborech (grep)")
    print("  15. history     - Historie příkazů")
    print("  16. calc        - Kalkulačka")
    print("  17. color       - Změnit barvu terminálu")
    print("  18. battle      - AI Battle (dvě AI debatují)")
    print()
    print("  0. quit         - Konec")
    print()

def cmd_ls():
    path = input("Cesta (Enter = aktuální): ").strip() or "."
    try:
        items = list(Path(path).iterdir())
        print(f"\n📂 {Path(path).absolute()}\n")
        for item in sorted(items, key=lambda x: x.name.lower()):
            prefix = "📁" if item.is_dir() else "📄"
            size = ""
            if item.is_file():
                size = f" ({item.stat().st_size:,} B)"
            print(f"  {prefix} {item.name}{size}")
        print(f"\n{len(items)} položek")
    except Exception as e:
        print(f"Chyba: {e}")

def cmd_find():
    pattern = input("Vzor (např. *.py): ").strip()
    root = input("Kde hledat (Enter = .): ").strip() or "."
    try:
        matches = list(Path(root).rglob(pattern))
        print(f"\n🔍 Nalezeno {len(matches)} souborů:\n")
        for m in matches[:50]:
            print(f"  {m}")
        if len(matches) > 50:
            print(f"  ... a dalších {len(matches) - 50}")
    except Exception as e:
        print(f"Chyba: {e}")

def cmd_tree():
    path = input("Cesta (Enter = .): ").strip() or "."
    max_depth = input("Max hloubka (Enter = 3): ").strip() or "3"
    try:
        subprocess.run(["tree", "/F", "/A", path], shell=True)
    except:
        print("tree není dostupný, zkuste: dir /s /b")

def cmd_diff():
    f1 = input("Soubor 1: ").strip()
    f2 = input("Soubor 2: ").strip()
    try:
        subprocess.run(["diff", f1, f2])
    except FileNotFoundError:
        # Windows fallback
        subprocess.run(["fc", f1, f2])

def cmd_note():
    notes_dir = Path(load_config()["notes_dir"])
    notes_dir.mkdir(exist_ok=True)
    
    print("1. Nová poznámka")
    print("2. Číst poznámku")
    choice = input("Volba: ").strip()
    
    if choice == "1":
        name = input("Název: ").strip()
        if not name:
            return
        if not name.endswith(".txt"):
            name += ".txt"
        note_file = notes_dir / name
        print(f"Píši do: {note_file}")
        print("Ukonči zadáním 'END' na novém řádku:")
        
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        
        with open(note_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print("✅ Uloženo!")
    
    elif choice == "2":
        name = input("Název poznámky: ").strip()
        if not name.endswith(".txt"):
            name += ".txt"
        note_file = notes_dir / name
        if note_file.exists():
            print(f"\n--- {note_file.name} ---\n")
            print(note_file.read_text(encoding="utf-8"))
        else:
            print("❌ Poznámka nenalezena")

def cmd_notes():
    notes_dir = Path(load_config()["notes_dir"])
    if not notes_dir.exists():
        print("Žádné poznámky")
        return
    
    notes = list(notes_dir.glob("*.txt"))
    print(f"\n📝 Poznámky ({len(notes)}):\n")
    for note in sorted(notes, key=lambda x: x.stat().st_mtime, reverse=True):
        mtime = datetime.datetime.fromtimestamp(note.stat().st_mtime)
        print(f"  📄 {note.name}  ({mtime.strftime('%d.%m.%Y %H:%M')})")

def cmd_todo():
    todo_file = Path(load_config()["notes_dir"]) / "todo.txt"
    todo_file.parent.mkdir(exist_ok=True)
    
    print("1. Přidat úkol")
    print("2. Zobrazit úkoly")
    print("3. Odebrat splněný")
    choice = input("Volba: ").strip()
    
    if choice == "1":
        task = input("Úkol: ").strip()
        if task:
            with open(todo_file, "a", encoding="utf-8") as f:
                f.write(f"[ ] {task}\n")
            print("✅ Přidáno!")
    
    elif choice == "2":
        if todo_file.exists():
            print("\n📋 TODO:\n")
            print(todo_file.read_text(encoding="utf-8"))
        else:
            print("Žádné úkoly")
    
    elif choice == "3":
        if todo_file.exists():
            lines = todo_file.read_text(encoding="utf-8").splitlines()
            for i, line in enumerate(lines, 1):
                print(f"  {i}. {line}")
            num = input("Číslo k odebrání: ").strip()
            try:
                idx = int(num) - 1
                if 0 <= idx < len(lines):
                    removed = lines.pop(idx)
                    todo_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
                    print(f"✅ Odebráno: {removed}")
            except ValueError:
                print("Neplatné číslo")

def cmd_sysinfo():
    import platform
    import psutil
    print("\n🖥️  SYSTÉM:\n")
    print(f"  OS:           {platform.system()} {platform.release()}")
    print(f"  Verze:        {platform.version()}")
    print(f"  Počítač:      {platform.node()}")
    print(f"  Procesor:     {platform.processor()}")
    print(f"  Python:       {platform.python_version()}")
    
    mem = psutil.virtual_memory()
    print(f"\n💾 PAMĚŤ:")
    print(f"  Celkem:       {mem.total // (1024**3)} GB")
    print(f"  Využito:      {mem.percent}%")
    print(f"  Volno:        {mem.available // (1024**3)} GB")
    
    cpu = psutil.cpu_percent(interval=1)
    print(f"\n⚡ CPU:          {cpu}%")

def cmd_processes():
    import psutil
    procs = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            procs.append(proc.info)
        except:
            pass
    
    procs.sort(key=lambda x: x['memory_percent'] or 0, reverse=True)
    print(f"\n🔄 TOP PROCESY (z {len(procs)} celkem):\n")
    print(f"  {'PID':>6}  {'CPU%':>5}  {'MEM%':>6}  Název")
    print("  " + "-" * 50)
    for p in procs[:15]:
        print(f"  {p['pid']:>6}  {p['cpu_percent'] or 0:>5.1f}  {p['memory_percent'] or 0:>6.1f}  {p['name']}")

def cmd_disk():
    import psutil
    print("\n💿 DISKY:\n")
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            bar_len = 30
            used = int(usage.percent / 100 * bar_len)
            bar = "█" * used + "░" * (bar_len - used)
            print(f"  {part.device:6}  {part.mountpoint:4}")
            print(f"         [{bar}] {usage.percent}%")
            print(f"         {usage.used // (1024**3)} GB / {usage.total // (1024**3)} GB\n")
        except:
            pass

def cmd_network():
    import psutil
    print("\n🌐 SÍŤ:\n")
    addrs = psutil.net_if_addrs()
    stats = psutil.net_io_counters()
    print(f"  Celkem odesláno:    {stats.bytes_sent // (1024**2):,} MB")
    print(f"  Celkem přijato:     {stats.bytes_recv // (1024**2):,} MB")
    print(f"  Balíčky odeslány:   {stats.packets_sent:,}")
    print(f"  Balíčky přijaty:    {stats.packets_recv:,}")
    print(f"\n  Rozhraní:")
    for name, addrs_list in addrs.items():
        for a in addrs_list:
            if a.family.name == 'AF_INET':
                print(f"    {name}: {a.address}")

def cmd_edit():
    config = load_config()
    file = input("Soubor: ").strip()
    editor = config.get("editor", "notepad")
    print(f"Otevírám {file} v {editor}...")
    subprocess.run([editor, file])

def cmd_search():
    pattern = input("Regex/vzor: ").strip()
    path = input("Cesta (Enter = .): ").strip() or "."
    try:
        result = subprocess.run(
            ["rg", pattern, path, "-n", "--color", "never"],
            capture_output=True, text=True
        )
        if result.stdout:
            print(result.stdout)
        else:
            print("Nic nenalezeno")
    except FileNotFoundError:
        print("rg není dostupný, zkuste: findstr /s /n " + pattern + " " + path)

def cmd_history():
    hist_file = Path(os.environ.get("USERPROFILE", ".")) / ".bash_history"
    if not hist_file.exists():
        hist_file = Path(os.environ.get("USERPROFILE", ".")) / ".zsh_history"
    
    # PowerShell history
    ps_hist = Path(os.environ.get("USERPROFILE", ".")) / "AppData/Roaming/Microsoft/Windows/PowerShell/PSReadLine/ConsoleHost_history.txt"
    if ps_hist.exists():
        lines = ps_hist.read_text(encoding="utf-8", errors="ignore").splitlines()
        print(f"\n📜 Posledních 30 příkazů:\n")
        for line in lines[-30:]:
            print(f"  {line}")
    else:
        print("Historie nenalezena")

def cmd_calc():
    print("Kalkulačka (zadej příkaz, Enter = spočítej)")
    print("  Operace: + - * / ** // %")
    while True:
        expr = input(">>> ").strip()
        if expr.lower() in ("quit", "exit", "q"):
            break
        try:
            result = eval(expr)
            print(f"  = {result}")
        except Exception as e:
            print(f"  Chyba: {e}")

def cmd_color():
    print("Barvy terminálu:")
    print("1. Bílý (default)")
    print("2. Zelený (Matrix)")
    print("3. Červený (Hacker)")
    print("4. Žlutý (Retro)")
    print("5. Cyan (Cyber)")
    choice = input("Volba: ").strip()
    
    colors = {
        "1": "0F",  # White on Black
        "2": "0A",  # Green on Black
        "3": "0C",  # Red on Black
        "4": "0E",  # Yellow on Black
        "5": "0B",  # Cyan on Black
    }
    
    color = colors.get(choice, "0F")
    if os.name == "nt":
        os.system(f"color {color}")
    else:
        print("(funguje pouze na Windows)")

def cmd_ide():
    file = input("Soubor (Enter = nový): ").strip() or None
    print("Spouštím Terminal IDE...")
    ide_path = Path(__file__).parent / "terminal_ide.py"
    cmd = ["python", str(ide_path)]
    if file:
        cmd.append(file)
    subprocess.run(cmd)

def cmd_battle():
    print("Spouštím AI Battle...")
    battle_path = Path(__file__).parent / "ai_battle.py"
    subprocess.run(["python", str(battle_path)])

def main():
    while True:
        clear()
        print_header()
        print_menu()
        
        choice = input("👉 Volba: ").strip()
        
        if choice == "0" or choice.lower() == "quit":
            print("\n👋 Ahoj! Hodně štěstí s challenge!\n")
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
            cmd_ide()
        elif choice == "14":
            cmd_search()
        elif choice == "15":
            cmd_history()
        elif choice == "16":
            cmd_calc()
        elif choice == "17":
            cmd_color()
        elif choice == "18":
            cmd_battle()
        else:
            print("Neplatná volba!")
        
        input("\n⏎ Enter pro pokračování...")

if __name__ == "__main__":
    main()
