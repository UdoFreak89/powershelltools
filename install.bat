@echo off
echo.
echo +====================================================+
echo         TERMINAL IDE - INSTALACE
echo +====================================================+
echo.
echo 1. Spoustim instalaci do PATH...
echo.
python "%~dp0glow.py" --install
echo.
echo 2. Kontrola stavu...
python "%~dp0glow.py" --status
echo.
echo +====================================================+
echo   INSTALACE DOKONCENA
echo.
echo   Restartuj terminal a pak pouzivej:
echo     glow soubor.py
echo     glow --help
echo +====================================================+
echo.
pause
