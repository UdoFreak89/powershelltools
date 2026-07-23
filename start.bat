@echo off
cd /d "%~dp0"
pip install -q psutil 2>nul
python tools.py
