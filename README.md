# Terminal Challenge Toolkit

A set of tools for controlling your PC entirely from the terminal.

## Tools

### 🌟 Glow IDE
```
glow                      Open empty editor
glow file.py              Open a file
glow --install            Add to PATH
glow --uninstall          Remove from PATH
```
- Syntax highlighting for Python, JS, Rust, Go
- Line numbers, status bar
- Ctrl+S=save, Ctrl+Q=quit, Ctrl+O=open, Ctrl+G=goto

### 📁 File Tool
```
ft cp file.py backup.py          Copy file
ft cp -r folder/ new/            Copy folder recursively
ft mv file.py archive/           Move file
ft rm *.bak                      Delete files
ft ren old.py new.py             Rename file
ft ls                            List directory contents
ft find *.py                     Search for files
ft size ./project                Folder size
ft tree                          Tree view
```

### ⚔️ AI Battle
```
python ai_battle.py              Two AIs debate each other
```
- Real-time streaming - watch text appear character by character
- Shows AI reasoning/thinking process
- Supports: OpenRouter, DeepSeek, OpenAI, Anthropic, Google

### 🛠️ Terminal Challenge Toolkit
```
python tools.py                  Main tools menu
```

## Installation

1. Clone the repo:
```bash
git clone https://github.com/UdoFreak89/powershelltools.git
```

2. Install to PATH:
```bash
.\install.bat
```

3. Restart your terminal and use:
```bash
glow --help
ft --help
```

## Requirements

- Python 3.8+
- prompt_toolkit (for Glow IDE)
- psutil (for sysinfo)
- requests (for AI Battle)

## License

MIT

## Contributors

- **UdoFreak89** - Project creator
- **big-pickle** - AI assistant (code, architecture, debugging)
