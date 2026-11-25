@echo off
set "APP=%LOCALAPPDATA%\AlansarPrices"
mkdir "%APP%" 2>nul
copy /Y "%~dp0dist\AlansarPrices.exe" "%APP%\" >nul
powershell -NoProfile -Command "$s=New-Object -ComObject WScript.Shell; foreach($p in @([Environment]::GetFolderPath('Desktop'),[Environment]::GetFolderPath('Programs'))){ $l=$s.CreateShortcut($p+'\Alansar Prices.lnk'); $l.TargetPath='%APP%\AlansarPrices.exe'; $l.WorkingDirectory='%APP%'; $l.Save() }"
start "" "%APP%\AlansarPrices.exe"
echo Done. Right-click the app icon on the taskbar and choose "Pin to taskbar".
pause
