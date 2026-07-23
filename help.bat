@echo off
REM Terminal Challenge - Rychle prikazy
REM Pridej do PATH nebo spoustej primo

set DIR=%~dp0

echo.
echo +========================================+
echo   TERMINAL CHALLENGE - RYCHLE PRIKAZY
echo +========================================+
echo.
echo  python %DIR%tools.py          - Hlavni menu
echo  python %DIR%quick.py list     - Rychle poznamky
echo  python %DIR%quick.py add      - Pridat poznamku
echo  python %DIR%glow.py           - Terminal IDE (glow)
echo.
echo  Tip: Pridej do PATH pro pristup odkudkoliv:
echo    set PATH=%%PATH%%;%DIR%
echo.
