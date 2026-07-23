@echo off
cd /d "%~dp0"
pip install -q requests 2>nul
python ai_battle.py
