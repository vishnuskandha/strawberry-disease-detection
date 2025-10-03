@echo off
echo 🍓 Strawberry Disease Detection
echo ================================

if "%1"=="" (
    echo Usage: detect.bat "path\to\image.jpg"
    echo Or: detect.bat
    echo.
    python detect_strawberry.py
) else (
    python detect_strawberry.py "%1"
)

pause
