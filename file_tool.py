#!/usr/bin/env python3
"""
FILE TOOL - Zjednoduseni prace se soubory v terminalu
Kopirovani, presouvani, prejmenovani, mazani, hledani - vse jednim prikazem.
"""

import os
import sys
import shutil
import fnmatch
from pathlib import Path
from datetime import datetime

VERSION = "1.0.0"

def human_size(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}TB"

def print_banner():
    print("""
+====================================+
|        FILE TOOL v1.0              |
|   Kopirovani, presouvani, hledani  |
+====================================+
    """)

def print_help():
    print("""
POUZITI:
  ft <prikaz> <zdroj> <cil>

PRIKAZY:
  cp, copy      Kopiruj soubor/slozku
  mv, move      Presun soubor/slozku
  rm, del       Smaz soubor/slozku
  ren           Prejmenuj soubor
  ls            Zobraz obsah slozky
  find          Hledej soubory
  size          Velikost souboru/slozky
  tree          Stromova struktura
  md            Vytvor slozku
  touch         Vytvor prazdny soubor
  info          Info o souboru
  batch         Hromadne operace

PRIKLADY:
  ft cp soubor.py backup.py           Kopiruj soubor
  ft cp soubor.py zaloha/             Kopiruj do slozky
  ft cp -r stara_nova/ nova/          Kopiruj celou slozku
  ft mv soubor.py archiv/             Presun soubor
  ft rm stare_bak*.bak               Smaz soubory
  ft ren stary.py novy.py            Prejmenuj
  ft ls                               Zobraz aktualni slozku
  ft ls ~/Documents                   Zobraz Documents
  ft find *.py                        Hledej Python soubory
  ft find *.py ~/projekty             Hledej v jine slozce
  ft size ./projekt                   Velikost slozky
  ft tree                             Stromova struktura
  ft md nova_slozka                   Vytvor slozku
  ft touch prazdny.txt                Vytvor soubor
  ft info soubor.py                   Detaily o souboru
  ft batch cp *.py backup/            Kopiruj vsechny .py do slozky
  ft batch rm *.bak                   Smaz vsechny .bak
    """)

def cmd_copy(args):
    if len(args) < 2:
        print("Pouziti: ft cp <zdroj> <cil>")
        return
    
    src = args[0]
    dst = args[1]
    recursive = "-r" in args
    if recursive:
        args.remove("-r")
        src = args[0]
        dst = args[1]
    
    src_path = Path(src)
    dst_path = Path(dst)
    
    if not src_path.exists():
        print(f"Chyba: {src} neexistuje!")
        return
    
    try:
        if src_path.is_dir():
            if recursive:
                if dst_path.exists():
                    dst_path = dst_path / src_path.name
                shutil.copytree(src_path, dst_path)
                print(f"Slozka zkopirovana: {src} -> {dst}")
            else:
                print("Pro kopirovani slozky pouzij: ft cp -r <slozka> <cil>")
        else:
            if dst_path.is_dir():
                dst_path = dst_path / src_path.name
            shutil.copy2(src_path, dst_path)
            print(f"Soubor zkopirovan: {src} -> {dst}")
    except Exception as e:
        print(f"Chyba: {e}")

def cmd_move(args):
    if len(args) < 2:
        print("Pouziti: ft mv <zdroj> <cil>")
        return
    
    src = args[0]
    dst = args[1]
    
    src_path = Path(src)
    dst_path = Path(dst)
    
    if not src_path.exists():
        print(f"Chyba: {src} neexistuje!")
        return
    
    try:
        if dst_path.is_dir():
            dst_path = dst_path / src_path.name
        shutil.move(str(src_path), str(dst_path))
        print(f"Presunuto: {src} -> {dst}")
    except Exception as e:
        print(f"Chyba: {e}")

def cmd_delete(args):
    if len(args) < 1:
        print("Pouziti: ft rm <soubor>")
        return
    
    for pattern in args:
        matches = list(Path(".").glob(pattern))
        if not matches:
            print(f"Nenalezeno: {pattern}")
            continue
        
        for path in matches:
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                    print(f"Slozka smazana: {path}")
                else:
                    path.unlink()
                    print(f"Soubor smazan: {path}")
            except Exception as e:
                print(f"Chyba pri mazani {path}: {e}")

def cmd_rename(args):
    if len(args) < 2:
        print("Pouziti: ft ren <stary> <novy>")
        return
    
    src = Path(args[0])
    dst = Path(args[1])
    
    if not src.exists():
        print(f"Chyba: {args[0]} neexistuje!")
        return
    
    try:
        src.rename(dst)
        print(f"Prejmenovano: {args[0]} -> {args[1]}")
    except Exception as e:
        print(f"Chyba: {e}")

def cmd_list(args):
    path = Path(args[0]) if args else Path(".")
    
    if not path.exists():
        print(f"Chyba: {path} neexistuje!")
        return
    
    print(f"\nObsah: {path.absolute()}\n")
    
    items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
    
    total_size = 0
    count = 0
    
    for item in items:
        if item.is_dir():
            print(f"  [DIR]  {item.name}/")
        else:
            size = item.stat().st_size
            total_size += size
            print(f"  [FILE] {item.name:30} {human_size(size):>8}")
        count += 1
    
    print(f"\n{count} polozek, celkem {human_size(total_size)}")

def cmd_find(args):
    if not args:
        print("Pouziti: ft find <vzor> [cesta]")
        return
    
    pattern = args[0]
    root = Path(args[1]) if len(args) > 1 else Path(".")
    
    if not root.exists():
        print(f"Chyba: {root} neexistuje!")
        return
    
    print(f"Hledam '{pattern}' v {root.absolute()}...\n")
    
    matches = []
    for path in root.rglob("*"):
        if fnmatch.fnmatch(path.name.lower(), pattern.lower()):
            matches.append(path)
    
    if matches:
        for m in sorted(matches):
            size = ""
            if m.is_file():
                size = f" ({human_size(m.stat().st_size)})"
            print(f"  {m}{size}")
        print(f"\nNalezeno: {len(matches)} souboru")
    else:
        print("Nic nenalezeno")

def cmd_size(args):
    path = Path(args[0]) if args else Path(".")
    
    if not path.exists():
        print(f"Chyba: {path} neexistuje!")
        return
    
    if path.is_file():
        print(f"{path}: {human_size(path.stat().st_size)}")
        return
    
    total = 0
    count = 0
    for item in path.rglob("*"):
        if item.is_file():
            total += item.stat().st_size
            count += 1
    
    print(f"{path}: {human_size(total)} ({count} souboru)")

def cmd_tree(args):
    path = Path(args[0]) if args else Path(".")
    
    if not path.exists():
        print(f"Chyba: {path} neexistuje!")
        return
    
    def print_tree(p, prefix=""):
        items = sorted(p.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
        dirs = [i for i in items if i.is_dir()]
        files = [i for i in items if i.is_file()]
        
        for i, f in enumerate(files):
            print(f"{prefix}  {f.name}")
        
        for i, d in enumerate(dirs):
            is_last = (i == len(dirs) - 1) and not files
            connector = "└── " if is_last else "├── "
            print(f"{prefix}{connector}{d.name}/")
            print_tree(d, prefix + ("    " if is_last else "│   "))
    
    print(f"{path.name}/")
    print_tree(path)

def cmd_mkdir(args):
    if not args:
        print("Pouziti: ft md <nazev_slozky>")
        return
    
    for name in args:
        try:
            Path(name).mkdir(parents=True, exist_ok=True)
            print(f"Slozka vytvorena: {name}")
        except Exception as e:
            print(f"Chyba: {e}")

def cmd_touch(args):
    if not args:
        print("Pouziti: ft touch <nazev_souboru>")
        return
    
    for name in args:
        try:
            Path(name).touch()
            print(f"Soubor vytvoren: {name}")
        except Exception as e:
            print(f"Chyba: {e}")

def cmd_info(args):
    if not args:
        print("Pouziti: ft info <soubor>")
        return
    
    path = Path(args[0])
    
    if not path.exists():
        print(f"Chyba: {path} neexistuje!")
        return
    
    stat = path.stat()
    
    print(f"\nInformace o: {path}")
    print(f"  Typ:        {'Slozka' if path.is_dir() else 'Soubor'}")
    print(f"  Velikost:   {human_size(stat.st_size)}")
    print(f"  Vytvoren:   {datetime.fromtimestamp(stat.st_ctime).strftime('%d.%m.%Y %H:%M')}")
    print(f"  Upraven:    {datetime.fromtimestamp(stat.st_mtime).strftime('%d.%m.%Y %H:%M')}")
    print(f"  Pristup:    {datetime.fromtimestamp(stat.st_atime).strftime('%d.%m.%Y %H:%M')}")
    
    if path.is_file():
        ext = path.suffix.lower()
        types = {
            ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
            ".rs": "Rust", ".go": "Go", ".java": "Java",
            ".txt": "Text", ".md": "Markdown", ".json": "JSON",
            ".yaml": "YAML", ".yml": "YAML", ".xml": "XML",
            ".html": "HTML", ".css": "CSS", ".bat": "Batch",
            ".ps1": "PowerShell", ".sh": "Shell", ".sql": "SQL",
        }
        print(f"  Typ souboru: {types.get(ext, ext or 'Neznamy')}")

def cmd_batch(args):
    if len(args) < 3:
        print("Pouziti: ft batch <cp|mv|rm> <vzor> <cil>")
        print("Priklad: ft batch cp *.py backup/")
        return
    
    action = args[0]
    pattern = args[1]
    target = Path(args[2]) if len(args) > 2 else None
    
    matches = list(Path(".").glob(pattern))
    
    if not matches:
        print(f"Nenalezeno: {pattern}")
        return
    
    print(f"Nalezeno {len(matches)} souboru\n")
    
    if action in ("cp", "copy"):
        if target:
            target.mkdir(parents=True, exist_ok=True)
        for m in matches:
            if m.is_file():
                dst = target / m.name if target else m
                shutil.copy2(m, dst)
                print(f"  Kopirovano: {m.name}")
    
    elif action in ("mv", "move"):
        if target:
            target.mkdir(parents=True, exist_ok=True)
        for m in matches:
            if m.is_file():
                dst = target / m.name if target else m
                shutil.move(str(m), str(dst))
                print(f"  Presunuto: {m.name}")
    
    elif action in ("rm", "del"):
        for m in matches:
            try:
                if m.is_dir():
                    shutil.rmtree(m)
                else:
                    m.unlink()
                print(f"  Smazano: {m.name}")
            except Exception as e:
                print(f"  Chyba {m.name}: {e}")
    
    else:
        print(f"Neznamy prikaz batch: {action}")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h", "/?"):
        print_help()
        return
    
    if sys.argv[1] in ("--version", "-v"):
        print(f"file tool v{VERSION}")
        return
    
    cmd = sys.argv[1].lower()
    args = sys.argv[2:]
    
    commands = {
        "cp": cmd_copy, "copy": cmd_copy,
        "mv": cmd_move, "move": cmd_move,
        "rm": cmd_delete, "del": cmd_delete,
        "ren": cmd_rename,
        "ls": cmd_list, "dir": cmd_list,
        "find": cmd_find, "search": cmd_find,
        "size": cmd_size,
        "tree": cmd_tree,
        "md": cmd_mkdir, "mkdir": cmd_mkdir,
        "touch": cmd_touch,
        "info": cmd_info,
        "batch": cmd_batch,
    }
    
    if cmd in commands:
        commands[cmd](args)
    else:
        print(f"Neznamy prikaz: {cmd}")
        print("Pouzij: ft --help")

if __name__ == "__main__":
    main()
