# Terminal Challenge Toolkit

I wanted to see if I could control my entire PC using only the terminal - no mouse, no GUI, just pure command line. So I built these tools to make that challenge easier. They cover everything from file management and system monitoring to AI battles and password generation. The whole project is open source, so feel free to download, try it out, and contribute!

## Quick Start

```bash
git clone https://github.com/UdoFreak89/powershelltools.git
cd powershelltools
pip install -r requirements.txt
python tools.py
```

Or use the `.bat` wrappers directly - they're all in the root folder.

## Tools

### tools.py - Main Menu
```bash
python tools.py        Launch the interactive hub with all tools
```
The central menu that ties everything together. Run it and pick what you need.

### File Tool (ft.bat)
```bash
ft cp file.py backup.py          Copy file
ft cp -r folder/ new/            Copy folder recursively
ft mv file.py archive/           Move file
ft rm *.bak                      Delete files
ft ren old.py new.py             Rename file
ft ls                            List directory contents
ft find *.py                     Search for files
ft size ./project                Folder size
ft tree                          Tree view
ft md new_folder                 Create directory
ft touch new.txt                 Create empty file
ft info file.py                  File details
ft batch cp *.py backup/         Batch copy
```

### AI Battle (ai_battle.bat)
```bash
python ai_battle.py              Two AIs debate each other in real-time
```
- Real-time streaming - watch text appear character by character
- Shows AI reasoning/thinking process live
- Supports: OpenRouter, DeepSeek, OpenAI, Anthropic, Google
- Pick any models, any providers, any topic

### System Monitor (sm.bat)
```bash
python sysmon.py                 Live CPU, RAM, disk, network, battery
python sysmon.py cpu             CPU only
python sysmon.py ram             Memory only
python sysmon.py all             Everything
```
Real-time dashboard that refreshes every 2 seconds.

### Password Generator (pw.bat)
```bash
python password_gen.py           Interactive password/password/PIN/UUID/token generator
```
- Secure passwords with configurable complexity
- Passphrases from word lists
- UUIDs (v1 and v4)
- API keys and tokens
- Batch generation

### Hash Tool (hash.bat)
```bash
python hash_tool.py              MD5, SHA1, SHA256, SHA512 for files and text
```
- Hash files or text
- Compare two files
- Search for hex patterns in binary files

### Encoder/Decoder (enc.bat)
```bash
python encoder.py                Base64, URL, Hex, HTML, ROT13, Binary, Morse
```
13 encoding/decoding options in one tool.

### Timer & Stopwatch (timer.bat)
```bash
python timer.py                  Countdown, stopwatch, Pomodoro, alarm
```
- Countdown timer
- Stopwatch with split timing
- Pomodoro (work/break cycles)
- Alarm clock

### JSON Tool (json.bat)
```bash
python json_tool.py              Format, validate, minify, search, convert JSON
```
- Format/prettify JSON
- Validate syntax
- Minify
- Search keys/values recursively
- Export to CSV or YAML
- Inspect structure and depth

### Network Tool (net.bat)
```bash
python net_tool.py               Ping, DNS, port scan, traceroute, IP info
```
- Ping with custom count
- DNS lookup and reverse DNS
- Multi-threaded port scanner
- Single port check
- Traceroute
- Local IP detection

### Git Helper (git.bat)
```bash
python git_helper.py             Interactive git shortcuts
```
- Status, log, diff
- Quick add + commit
- Push, pull, branches
- Clone, stash, blame
- .gitignore management

### Quick Notes (quick.py)
```bash
python quick.py add "name" "text"    Save a note
python quick.py list                 List all notes
python quick.py read "name"          Read a note
python quick.py del "name"           Delete a note
```

## All Batch Wrappers

| Command | Tool |
|---------|------|
| `ft` | File Tool |
| `sm` | System Monitor |
| `pw` | Password Generator |
| `hash` | Hash Tool |
| `enc` | Encoder/Decoder |
| `timer` | Timer & Stopwatch |
| `json` | JSON Tool |
| `net` | Network Tool |
| `git` | Git Helper |
| `ai_battle` | AI Battle |

## Requirements

- Python 3.8+
- psutil (for system monitor and sysinfo)
- requests (for AI Battle)
- prompt_toolkit (optional, for enhanced terminal input)

```bash
pip install -r requirements.txt
```

## License

MIT - do whatever you want with it.

## Contributors

- **UdoFreak89** - Project creator
- **big-pickle** - AI assistant (code, architecture, debugging)
