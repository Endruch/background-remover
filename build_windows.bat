@echo off
REM Script for building GUI application to EXE file for Windows
REM Run this file on Windows after installing dependencies

echo ========================================
echo Building "Background Remover" application
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/4] Installing PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)

echo.
echo [3/4] Building EXE file (standalone)...
if exist "app_icon.ico" (
    echo Using icon: app_icon.ico
    pyinstaller --onefile --windowed --name="Background Remover" --icon=app_icon.ico --clean --hidden-import=PIL --hidden-import=PIL._imagingtk --hidden-import=PIL._tkinter_finder --collect-all tkinterdnd2 background_remover_gui.py
) else (
    echo Icon not found, building without icon
    pyinstaller --onefile --windowed --name="Background Remover" --icon=NONE --clean --hidden-import=PIL --hidden-import=PIL._imagingtk --hidden-import=PIL._tkinter_finder --collect-all tkinterdnd2 background_remover_gui.py
)
if errorlevel 1 (
    echo ERROR: Failed to build application
    pause
    exit /b 1
)

echo.
echo [4/4] Done!
echo.
echo ========================================
echo EXE file located at: dist\Background Remover.exe
echo ========================================
echo.
pause
