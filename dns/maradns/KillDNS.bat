netstat -abno | findstr ":53"
@echo off
set /p id=Enter ID: 
taskkill /F /PID %id%

pause