@echo off
setlocal enabledelayedexpansion

python say.py "Sto aprendo "%2"" -l "it" --connect
echo Sto aprendo %2

for /f "delims=" %%i in ('python jsonutils.py get -f "../commands/open/apps.json" -k %2') do (set "p=%%i")
echo "%p%"

start "" "%p%"
exit