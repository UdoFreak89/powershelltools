#!/usr/bin/env python3
"""
FILE TOOL - Simplified file operations in terminal
Copy, move, rename, delete, search - all in one command.
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
|  Copy, move, search, batch ops    |
+====================================+
    """)

def print_help():
    print("""
USAGE:
  ft <command> <source> <dest>

COMMANDS:
  cp, copy      Copy file/folder
  mv, move      Move file/folder
  rm, del       Delete file/folder
  ren           Rename file
  ls            List directory contents
  find          Search for files
  size          File/folder size
  tree          Tree structure
  md            Create directory
  touch         Create empty file
  info          File info
  batch         Batch operations

EXAMPLES:
  ft cp file.py backup.py           Copy file
  ft cp file.py backup/             Copy to folder
  ft cp -r old_dir/ new/            Copy entire folder
  ft mv file.py archive/            Move file
  ft rm old_bak*.bak               Delete files
  ft ren old.py new.py             Rename
  ft ls                            List current dir
  ft ls ~/Documents                List Documents
  ft find *.py                     Find Python files
  ft find *.py ~/projects          Find in other dir
  ft size ./project                Folder size
  ft tree                          Tree structure
  ft md new_folder                 Create folder
  ft touch empty.txt               Create file
  ft info file.py                  File details
  ft batch cp *.py backup/         Copy all .py to folder
  ft batch rm *.bak                Delete all .bak
    """)

def cmd_copy(args):
    if len(args) < 2:
        print("Usage: ft cp <source> <dest>")
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
        print(f"Error: {src} does not exist!")
        return
    
    try:
        if src_path.is_dir():
            if recursive:
                if dst_path.exists():
                    dst_path = dst_path / src_path.name
                shutil.copytree(src_path, dst_path)
                print(f"Folder copied: {src} -> {dst}")
            else:
                print("To copy a folder use: ft cp -r <folder> <dest>")
        else:
            if dst_path.is_dir():
                dst_path = dst_path / src_path.name
            shutil.copy2(src_path, dst_path)
            print(f"File copied: {src} -> {dst}")
    except Exception as e:
        print(f"Error: {e}")

def cmd_move(args):
    if len(args) < 2:
        print("Usage: ft mv <source> <dest>")
        return
    
    src = args[0]
    dst = args[1]
    
    src_path = Path(src)
    dst_path = Path(dst)
    
    if not src_path.exists():
        print(f"Error: {src} does not exist!")
        return
    
    try:
        if dst_path.is_dir():
            dst_path = dst_path / src_path.name
        shutil.move(str(src_path), str(dst_path))
        print(f"Moved: {src} -> {dst}")
    except Exception as e:
        print(f"Error: {e}")

def cmd_delete(args):
    if len(args) < 1:
        print("Usage: ft rm <file>")
        return
    
    for pattern in args:
        matches = list(Path(".").glob(pattern))
        if not matches:
            print(f"Not found: {pattern}")
            continue
        
        for path in matches:
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                    print(f"Folder deleted: {path}")
                else:
                    path.unlink()
                    print(f"File deleted: {path}")
            except Exception as e:
                print(f"Error deleting {path}: {e}")

def cmd_rename(args):
    if len(args) < 2:
        print("Usage: ft ren <old> <new>")
        return
    
    src = Path(args[0])
    dst = Path(args[1])
    
    if not src.exists():
        print(f"Error: {args[0]} does not exist!")
        return
    
    try:
        src.rename(dst)
        print(f"Renamed: {args[0]} -> {args[1]}")
    except Exception as e:
        print(f"Error: {e}")

def cmd_list(args):
    path = Path(args[0]) if args else Path(".")
    
    if not path.exists():
        print(f"Error: {path} does not exist!")
        return
    
    print(f"\nContents: {path.absolute()}\n")
    
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
    
    print(f"\n{count} items, total {human_size(total_size)}")

def cmd_find(args):
    if not args:
        print("Usage: ft find <pattern> [path]")
        return
    
    pattern = args[0]
    root = Path(args[1]) if len(args) > 1 else Path(".")
    
    if not root.exists():
        print(f"Error: {root} does not exist!")
        return
    
    print(f"Searching for '{pattern}' in {root.absolute()}...\n")
    
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
        print(f"\nFound: {len(matches)} files")
    else:
        print("Nothing found")

def cmd_size(args):
    path = Path(args[0]) if args else Path(".")
    
    if not path.exists():
        print(f"Error: {path} does not exist!")
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
    
    print(f"{path}: {human_size(total)} ({count} files)")

def cmd_tree(args):
    path = Path(args[0]) if args else Path(".")
    
    if not path.exists():
        print(f"Error: {path} does not exist!")
        return
    
    def print_tree(p, prefix=""):
        items = sorted(p.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
        dirs = [i for i in items if i.is_dir()]
        files = [i for i in items if i.is_file()]
        
        for i, f in enumerate(files):
            print(f"{prefix}  {f.name}")
        
        for i, d in enumerate(dirs):
            is_last = (i == len(dirs) - 1) and not files
            connector = "\\--- " if is_last else "+--- "
            print(f"{prefix}{connector}{d.name}/")
            print_tree(d, prefix + ("    " if is_last else "|   "))
    
    print(f"{path.name}/")
    print_tree(path)

def cmd_mkdir(args):
    if not args:
        print("Usage: ft md <folder_name>")
        return
    
    for name in args:
        try:
            Path(name).mkdir(parents=True, exist_ok=True)
            print(f"Folder created: {name}")
        except Exception as e:
            print(f"Error: {e}")

def cmd_touch(args):
    if not args:
        print("Usage: ft touch <file_name>")
        return
    
    for name in args:
        try:
            Path(name).touch()
            print(f"File created: {name}")
        except Exception as e:
            print(f"Error: {e}")

def cmd_info(args):
    if not args:
        print("Usage: ft info <file>")
        return
    
    path = Path(args[0])
    
    if not path.exists():
        print(f"Error: {path} does not exist!")
        return
    
    stat = path.stat()
    
    print(f"\nInfo: {path}")
    print(f"  Type:        {'Folder' if path.is_dir() else 'File'}")
    print(f"  Size:        {human_size(stat.st_size)}")
    print(f"  Created:     {datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M')}")
    print(f"  Modified:    {datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')}")
    print(f"  Accessed:    {datetime.fromtimestamp(stat.st_atime).strftime('%Y-%m-%d %H:%M')}")
    
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
        print(f"  File type:   {types.get(ext, ext or 'Unknown')}")

def cmd_batch(args):
    if len(args) < 3:
        print("Usage: ft batch <cp|mv|rm> <pattern> <dest>")
        print("Example: ft batch cp *.py backup/")
        return
    
    action = args[0]
    pattern = args[1]
    target = Path(args[2]) if len(args) > 2 else None
    
    matches = list(Path(".").glob(pattern))
    
    if not matches:
        print(f"Not found: {pattern}")
        return
    
    print(f"Found {len(matches)} files\n")
    
    if action in ("cp", "copy"):
        if target:
            target.mkdir(parents=True, exist_ok=True)
        for m in matches:
            if m.is_file():
                dst = target / m.name if target else m
                shutil.copy2(m, dst)
                print(f"  Copied: {m.name}")
    
    elif action in ("mv", "move"):
        if target:
            target.mkdir(parents=True, exist_ok=True)
        for m in matches:
            if m.is_file():
                dst = target / m.name if target else m
                shutil.move(str(m), str(dst))
                print(f"  Moved: {m.name}")
    
    elif action in ("rm", "del"):
        for m in matches:
            try:
                if m.is_dir():
                    shutil.rmtree(m)
                else:
                    m.unlink()
                print(f"  Deleted: {m.name}")
            except Exception as e:
                print(f"  Error {m.name}: {e}")
    
    else:
        print(f"Unknown batch command: {action}")

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
        print(f"Unknown command: {cmd}")
        print("Use: ft --help")

if __name__ == "__main__":
    main()
