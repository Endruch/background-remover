@echo off
REM Расширенная сборка с использованием .spec файла
REM Гарантирует включение всех зависимостей

echo ========================================
echo Сборка BackgroundRemover (Advanced)
echo ========================================
echo.

echo [1/4] Установка зависимостей...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo [2/4] Создание иконки из Mad6d.gif...
if exist "Mad6d.gif" (
    python create_icon.py Mad6d.gif
    if errorlevel 1 (
        echo Предупреждение: Не удалось создать иконку, продолжаем без неё
    )
) else (
    echo Предупреждение: Mad6d.gif не найден, продолжаем без иконки
)

echo.
echo [3/4] Сборка через .spec файл...
pyinstaller --clean BackgroundRemover.spec

echo.
echo [4/4] Проверка результата...
if exist "dist\BackgroundRemover.exe" (
    echo.
    echo ========================================
    echo УСПЕХ! EXE файл создан:
    echo dist\BackgroundRemover.exe
    echo.
    echo Размер файла:
    dir "dist\BackgroundRemover.exe" | findstr BackgroundRemover
    echo ========================================
) else (
    echo.
    echo ОШИБКА: EXE файл не создан!
    echo Проверьте логи выше
)

echo.
pause
