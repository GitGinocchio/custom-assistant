@echo off
setlocal
set ora=%time%
for /f "tokens=1-2 delims=:" %%a in ("%ora%") do (set "ora=%%a:%%b")
python say.py "In questo momento sono le ore %ora%"
echo In questo momento sono le ore: %ora%