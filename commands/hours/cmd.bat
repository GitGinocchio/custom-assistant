@echo off
setlocal enabledelayedexpansion
for /f "tokens=1-2 delims=:" %%a in ("%time%") do (set "ora=%%a:%%b")
python say.py "In questo momento sono le ore %ora%"
echo In questo momento sono le ore: %ora%