@echo off
echo|set /p=Activating virtual environment...
call .venv\Scripts\activate > nul
<nul set /p=Done!
echo.

if exist build (rmdir /s /q build)
if exist dist (rmdir /s /q dist)

echo|set /p=Installing required dependencies...
pip install --upgrade pip > nul
pip install requests pandas tabulate pyinstaller datetime > nul
<nul set /p=Done!
echo.

echo|set /p=Building Warranty_Report_GUI.exe...
pyinstaller --onefile --windowed --clean --noconfirm Warranty_Report_GUI.py > build_log.txt 2>&1

move ".\build_log.txt" ".\build" > nul

echo Done!
echo Check the "dist" folder for your .exe
TIMEOUT /T 15 REM shows a countdown, can be ended with keypress