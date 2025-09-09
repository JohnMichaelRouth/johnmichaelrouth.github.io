@echo off
echo ================================
echo Advanced Auto Clicker Build Script
echo ================================
echo.

echo Installing Python dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Error installing dependencies!
    pause
    exit /b 1
)

echo.
echo Installing PyInstaller...
pip install pyinstaller
if %ERRORLEVEL% NEQ 0 (
    echo Error installing PyInstaller!
    pause
    exit /b 1
)

echo.
echo Compiling to executable...
pyinstaller --onefile --windowed --name "AdvancedAutoClicker" main.py
if %ERRORLEVEL% NEQ 0 (
    echo Error during compilation!
    pause
    exit /b 1
)

echo.
echo ================================
echo BUILD SUCCESSFUL!
echo ================================
echo.
echo Your executable is located at:
echo %CD%\dist\AdvancedAutoClicker.exe
echo.
echo The executable is ready for distribution and does not require Python to be installed.
echo.
pause