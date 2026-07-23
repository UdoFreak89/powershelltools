#!/usr/bin/env python3
"""
Terminal IDE - Help viewer
Zobrazi napovedu k editoru
"""

def show_help():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                    TERMINAL IDE - NAPovedA                        ║
╚═══════════════════════════════════════════════════════════════════╝

  KLAVESOVE ZKRATKY:
  ═══════════════════════════════════════════════════════════════════

  OVLADANI SOUBORU:
    Ctrl+N         Novy soubor
    Ctrl+O         Otevrit soubor (zobrazi prompt)
    Ctrl+S         Ulozit soubor
    Ctrl+Q         Ukoncit editor (zepta se na neulozene zmeny)
    Ctrl+C         Ukoncit bez ulozeni

  EDITACE:
    (normalni mod) Psani textu - rovnou vklada znaky
    Backspace      Smazat znak pred kurzorem
    Enter          Novy radek
    Tab            4 mezery
    Ctrl+K         Kopirovat aktualni radek
    Ctrl+V         Vlozit zkopirovany radek

  NAVIGACE:
    Sipka nahoru   Pohyb nahoru
    Sipka dolu     Pohyb dolu
    Sipka vlevo    Pohyb vlevo
    Sipka vpravo   Pohyb vpravo
    Home           Zacatek radku
    Konec          Konec radku
    Page Up        O stranku nahoru
    Page Down      O stranku dolu
    Ctrl+G         Skocit na cislo radku

  ZOBRAZENI:
    Ctrl+L         Zapnout/vypnout cisla radku

  COMMAND MODE (po zmacknuti : ):
    :w <file>      Ulozit jako <file>
    :e <file>      Otevrit <file>
    :q             Ukoncit (bez ulozeni)
    :wq            Ulozit a ukoncit
    :goto <cislo>  Skocit na radek <cislo>
    :set theme=dark|light|matrix    Zmenit tema
    :set number    Zapnout cisla radku
    :set nonumber  Vypnout cisla radku
    :themes        Zobrazit dostupna temata
    :colors        Zobrazit dostupne barvy
    :help          Zobrazit tuto napovedu

  THEME:
    dark           Tmave tema (default)
    light          Svetle tema
    matrix         Matrix zeleny

  SPUSTENI:
    python terminal_ide.py                Bez souboru
    python terminal_ide.py soubor.py      S otevrenym souborem
    ide.bat                               Pres batch soubor
    ide.bat soubor.py                     S otevrenym souborem

  TIPY:
    - Editor automaticky prida cisla radku
    - Syntax highlighting pro Python, JS, Rust, Go
    - Ulozene soubory se automaticky nedoplnuji do promptu
    - Stiskni Escape pro zruseni command mode
    - Editor funguje na Windows i Linux/Mac

    """)

if __name__ == "__main__":
    show_help()
