@echo off
echo ========================================
echo Build Background Remover
echo ========================================
echo.

echo [1/4] Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo [2/4] Creating icon from Mad6d.gif...
if exist "Mad6d.gif" (
    python create_icon.py Mad6d.gif
    if errorlevel 1 (
        echo Warning: Could not create icon, continuing without it
    )
) else (
    echo Warning: Mad6d.gif not found, continuing without icon
)

echo.
echo [3/4] Building EXE (this may take 2-5 minutes)...
if exist "app_icon.ico" (
    echo Using icon: app_icon.ico
    pyinstaller --onefile --windowed --name="Background Remover" --icon=app_icon.ico --clean --hidden-import=PIL --hidden-import=PIL._imagingtk --hidden-import=PIL._tkinter_finder --hidden-import=tkinterdnd2 --collect-all=tkinterdnd2 background_remover_gui.py
) else (
    echo Icon not found, building without icon
    pyinstaller --onefile --windowed --name="Background Remover" --clean --hidden-import=PIL --hidden-import=PIL._imagingtk --hidden-import=PIL._tkinter_finder --hidden-import=tkinterdnd2 --collect-all=tkinterdnd2 background_remover_gui.py
)

if errorlevel 1 (
    echo ERROR: Build failed!
    echo Check the logs above
    pause
    exit /b 1
)

echo.
echo [4/4] Checking result...
if exist "dist\Background Remover.exe" (
    echo.
    echo ========================================
    echo SUCCESS! EXE file created:
    echo dist\Background Remover.exe
    echo.
    echo File size:
    dir "dist\Background Remover.exe" | findstr Background Remover
    echo ========================================
) else (
    echo.
    echo ERROR: EXE file not created!
    echo Check logs above
)

echo.
pause
