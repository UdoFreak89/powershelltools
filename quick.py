#!/usr/bin/env python3
"""
Quick Notes - Rychlé poznámky příkazem
Použití:
  python quick.py add "Název" "Text poznámky"
  python quick.py list
  python quick.py read "Název"
  python quick.py del "Název"
"""

import sys
from pathlib import Path
import datetime

NOTES_DIR = Path.home() / "terminal-notes"
NOTES_DIR.mkdir(exist_ok=True)

def add(name, content):
    f = NOTES_DIR / f"{name}.txt"
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"✅ Uloženo: {f}")

def list_notes():
    notes = sorted(NOTES_DIR.glob("*.txt"), key=lambda x: x.stat().st_mtime, reverse=True)
    print(f"\n📝 {len(notes)} poznámek:\n")
    for n in notes:
        mt = datetime.datetime.fromtimestamp(n.stat().st_mtime)
        print(f"  📄 {n.stem:30}  {mt.strftime('%d.%m %H:%M')}")

def read(name):
    f = NOTES_DIR / f"{name}.txt"
    if f.exists():
        print(f"\n--- {name} ---\n")
        print(f.read_text(encoding="utf-8"))
    else:
        print(f"❌ {name} nenalezena")

def delete(name):
    f = NOTES_DIR / f"{name}.txt"
    if f.exists():
        f.unlink()
        print(f"✅ Smazána: {name}")
    else:
        print(f"❌ {name} nenalezena")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Použití: python quick.py [add|list|read|del] [název] [text]")
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    
    if cmd == "add" and len(sys.argv) >= 4:
        add(sys.argv[2], sys.argv[3])
    elif cmd == "add" and len(sys.argv) == 3:
        # Interactive add
        print(f"Píši poznámku '{sys.argv[2]}' (END = konec):")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        add(sys.argv[2], "\n".join(lines))
    elif cmd == "list":
        list_notes()
    elif cmd == "read" and len(sys.argv) >= 3:
        read(sys.argv[2])
    elif cmd == "del" and len(sys.argv) >= 3:
        delete(sys.argv[2])
    else:
        print("Neplatný příkaz")
