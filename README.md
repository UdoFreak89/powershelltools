# Terminal Challenge Toolkit

Sada nástrojů pro ovládání PC pouze přes terminál.

## Nástroje

### 🌟 Glow IDE
```
glow                      Otevře prázdný editor
glow soubor.py            Otevře soubor
glow --install            Nainstaluje do PATH
glow --uninstall          Odebere z PATH
```
- Syntax highlighting pro Python, JS, Rust, Go
- Císla řádků, status bar
- Ctrl+S=save, Ctrl+Q=quit, Ctrl+O=open, Ctrl+G=goto

### 📁 File Tool
```
ft cp soubor.py backup.py          Kopíruje soubor
ft cp -r slozka/ nova/             Kopíruje složku
ft mv soubor.py archiv/            Přesune soubor
ft rm *.bak                        Smaže soubory
ft ren stary.py novy.py            Přejmenuje
ft ls                              Zobrazí obsah
ft find *.py                       Hledá soubory
ft size ./projekt                  Velikost složky
ft tree                            Stromová struktura
```

### ⚔️ AI Battle
```
python ai_battle.py                Dvě AI debatují
```
- Streaming - vidíš text písmenko po písmenku
- Zobrazení myšlení AI (reasoning)
- Podpora: OpenRouter, DeepSeek, OpenAI, Anthropic, Google

### 🛠️ Terminal Challenge Toolkit
```
python tools.py                    Hlavní menu nástrojů
```

## Instalace

1. Klonuj repo:
```bash
git clone https://github.com/UdoFreak89/powershelltools.git
```

2. Nainstaluj do PATH:
```bash
.\install.bat
```

3. Restartuj terminal a používej:
```bash
glow --help
ft --help
```

## Požadavky

- Python 3.8+
- prompt_toolkit (pro Glow IDE)
- psutil (pro sysinfo)
- requests (pro AI Battle)

## Licence

MIT
