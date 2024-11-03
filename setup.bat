@echo off
REM Check if Python is added to PATH
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python is not added to PATH. Please check your installation.
    pause
    exit /b
)

REM Install libraries from requirements.txt
echo Installing libraries...
pip install -r requirements.txt

echo Installation completed.
pause
