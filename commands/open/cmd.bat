@echo off
setlocal enabledelayedexpansion

for /f %%i in ('python NLPTS.py %1 -tag "open" -model "../models/15.9.2023.pth"') do set APP=%%i

python say.py "Sto aprendo %APP%" -l "it" --connect
echo Sto aprendo %APP%

for /f "delims=" %%i in ('python jsonutils.py get -f "../commands/open/apps.json" -k %APP%') do (set "p=%%i")

echo "%p%"
start "" "%p%"
exit