@echo off
REM Скрипт для сборки GUI приложения в EXE файл для Windows
REM Запустите этот файл на Windows после установки зависимостей

echo ========================================
echo Сборка приложения "Удаление белого фона"
echo ========================================
echo.

REM Проверка установки Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ОШИБКА: Python не найден!
    echo Установите Python с https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Установка зависимостей...
pip install -r requirements.txt
if errorlevel 1 (
    echo ОШИБКА: Не удалось установить зависимости
    pause
    exit /b 1
)

echo.
echo [2/4] Установка PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo ОШИБКА: Не удалось установить PyInstaller
    pause
    exit /b 1
)

echo.
echo [3/4] Сборка EXE файла (standalone)...
if exist "app_icon.ico" (
    echo Используется иконка: app_icon.ico
    pyinstaller --onefile --windowed --name="BackgroundRemover" --icon=app_icon.ico --clean --hidden-import=PIL --hidden-import=PIL._imagingtk --hidden-import=PIL._tkinter_finder --collect-all tkinterdnd2 background_remover_gui.py
) else (
    echo Иконка не найдена, сборка без иконки
    pyinstaller --onefile --windowed --name="BackgroundRemover" --icon=NONE --clean --hidden-import=PIL --hidden-import=PIL._imagingtk --hidden-import=PIL._tkinter_finder --collect-all tkinterdnd2 background_remover_gui.py
)
if errorlevel 1 (
    echo ОШИБКА: Не удалось собрать приложение
    pause
    exit /b 1
)

echo.
echo [4/4] Готово!
echo.
echo ========================================
echo EXE файл находится в папке: dist\BackgroundRemover.exe
echo ========================================
echo.
pause
