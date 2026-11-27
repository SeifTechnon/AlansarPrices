@echo off
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  echo Python is not installed. Install it from python.org and tick "Add python.exe to PATH".
  pause
  exit /b
)
py -m pip install pyinstaller pillow tkinterdnd2

if exist icon.png (
  if not exist icon.ico py make_icon.py
)

if exist icon.ico (
  py -m PyInstaller --noconsole --onefile --name AlansarPrices --icon icon.ico --add-data "icon.ico;." --collect-all tkinterdnd2 app.py
) else (
  echo No icon found. Building without an icon. Put icon.ico next to this file to add one.
  py -m PyInstaller --noconsole --onefile --name AlansarPrices --collect-all tkinterdnd2 app.py
)

echo.
echo Done. Your program is in the dist folder: AlansarPrices.exe
pause
