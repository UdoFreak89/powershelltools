#!/usr/bin/env python3
"""
Terminal IDE CLI - Pridej do PATH a pouzivej odkudkoliv
Pouziti:
  glow                        Spusti editor (prazdny)
  glow soubor.py              Otevri soubor
  glow --install              Pridej do PATH (Windows)
  glow --uninstall            Odeber z PATH
  glow --version              Verze
  glow --help                 Napoveda
"""

import os
import sys
import shutil
from pathlib import Path

VERSION = "1.0.0"
SCRIPT_DIR = Path(__file__).parent.resolve()
IDE_SCRIPT = SCRIPT_DIR / "terminal_ide.py"
BATCH_FILE = SCRIPT_DIR / "glow.bat"

def print_banner():
    print("""
╔═══════════════════════════════════════════════════════╗
║              TERMINAL IDE - glow CLI                  ║
║              VS Code experience v terminalu           ║
╚═══════════════════════════════════════════════════════╝
    """)

def print_help():
    print("""
POUZITI:
  glow                           Otevri prazdny editor
  glow <soubor>                  Otevri soubor v editoru
  glow --install                 Nainstaluj do PATH (Windows)
  glow --uninstall               Odeber z PATH
  glow --status                  Zobraz stav instalace
  glow --version                 Zobraz verzi
  glow --help                    Zobraz tuto napovedu

PRIKLADY:
  glow main.py                   Otevri main.py
  glow C:\\projekt\\app.js       Otevri soubor na ceste
  glow --install                 Nastavi PATH aby fungovalo globalne

POZNAMKA:
  Po instalaci muzes glow pouzivat odkudkoliv v terminalu.
    """)

def install():
    """Pridej glow do PATH na Windows"""
    print("Instaluji glow do PATH...")
    
    bat_content = f'''@echo off
cd /d "{SCRIPT_DIR}"
python "{SCRIPT_DIR / "glow.py"}" %*
'''
    
    with open(BATCH_FILE, "w") as f:
        f.write(bat_content)
    
    print(f"  Vytvoreno: {BATCH_FILE}")
    
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_ALL_ACCESS)
        
        try:
            path_value, _ = winreg.QueryValueEx(key, "Path")
        except:
            path_value = ""
        
        if str(SCRIPT_DIR) not in path_value:
            new_path = str(SCRIPT_DIR) + ";" + path_value if path_value else str(SCRIPT_DIR)
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
            print(f"  PATH aktualizovan!")
            print(f"\n  !!! Ukonci a restartuj terminal aby se PATH aplikovalo !!!")
            print(f"  Potom muzes pouzivat: glow soubor.py")
        else:
            print(f"  Uz je v PATH!")
        
        winreg.CloseKey(key)
        
    except Exception as e:
        print(f"  Chyba pri nastaveni PATH: {e}")
        print(f"\n  Rucni instalace:")
        print(f"  1. Vytvor zkratku na {BATCH_FILE}")
        print(f"  2. Pridej {SCRIPT_DIR} do PATH")
    
    print("\nHotovo!")

def uninstall():
    """Odeber glow z PATH"""
    print("Odebiram glow z PATH...")
    
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_ALL_ACCESS)
        
        try:
            path_value, _ = winreg.QueryValueEx(key, "Path")
        except:
            print("PATH nenalezen")
            return
        
        paths = path_value.split(";")
        new_paths = [p for p in paths if p != str(SCRIPT_DIR) and p.strip()]
        
        if len(new_paths) < len(paths):
            new_path = ";".join(new_paths)
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
            print(f"  PATH aktualizovan!")
        else:
            print(f"  Glow nebyl v PATH nalezen")
        
        winreg.CloseKey(key)
        
    except Exception as e:
        print(f"  Chyba: {e}")
    
    # Smaz bat soubor (pokud existuje a neni to tento skript)
    try:
        if BATCH_FILE.exists() and BATCH_FILE != Path(__file__):
            BATCH_FILE.unlink()
            print(f"  Smazan: {BATCH_FILE}")
    except:
        pass
    
    print("\nHotovo!")
    print("Ukonci a restartuj terminal aby se zmena projevila.")

def check_status():
    """Zkontroluje stav instalace"""
    print("Stav instalace:\n")
    
    print(f"  Skript:  {IDE_SCRIPT}  [{'OK' if IDE_SCRIPT.exists() else 'CHYBI'}]")
    print(f"  Batch:   {BATCH_FILE}   [{'OK' if BATCH_FILE.exists() else 'NEEXISTUJE'}]")
    
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment")
        path_value, _ = winreg.QueryValueEx(key, "Path")
        winreg.CloseKey(key)
        
        in_path = str(SCRIPT_DIR) in path_value
        print(f"  V PATH:  {'ANO' if in_path else 'NE'}")
        
        if in_path:
            print(f"\n  Glow je nainstalovany! Muzes pouzivat: glow soubor.py")
        else:
            print(f"\n  Glow neni v PATH. Spust: glow --install")
    except:
        print(f"  V PATH:  Nelze zjistit")

def launch_editor(args):
    """Spusti editor"""
    import subprocess
    
    cmd = [sys.executable, str(IDE_SCRIPT)] + args
    subprocess.run(cmd)

def main():
    if len(sys.argv) == 1:
        launch_editor([])
        return
    
    arg = sys.argv[1]
    
    if arg in ("--help", "-h", "/?"):
        print_help()
    elif arg in ("--version", "-v"):
        print(f"glow v{VERSION}")
    elif arg == "--install":
        install()
    elif arg == "--uninstall":
        uninstall()
    elif arg == "--status":
        check_status()
    else:
        if os.path.exists(arg):
            launch_editor([arg])
        else:
            print(f"Soubor nenalezen: {arg}")
            print(f"Zkus: glow --help")

if __name__ == "__main__":
    main()
