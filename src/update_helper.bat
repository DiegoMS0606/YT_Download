@echo off
setlocal

set OLD_EXE=%1
set NEW_EXE=%2

echo Waiting for program to close...
timeout /t 2 >nul

echo Replacing exe...
move /Y "%NEW_EXE%" "%OLD_EXE%"
echo Launching new version...
start "" "%OLD_EXE%"

exit