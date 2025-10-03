@echo off
setlocal ENABLEDELAYEDEXPANSION

REM Change to repo directory
cd /d %~dp0

REM Timestamp
for /f "tokens=1-4 delims=/ " %%a in ("%date%") do set DATE=%%d-%%b-%%c
set TIMESTR=%time: =0%
set STAMP=%DATE%_%TIMESTR::=-%

REM Show starting message
echo [!STAMP!] Starting YOLOv8 training (auto-resume if available)...

REM Estimate epochs remaining if a last.pt exists by reading results.csv epochs
set RUN_DIR=runs\yolov8n-strawberry
set CSV=%RUN_DIR%\results.csv
if exist "%CSV%" (
  for /f "usebackq skip=1 tokens=1 delims=," %%E in ("%CSV%") do (
    set LAST_EPOCH=%%E
  )
  if defined LAST_EPOCH (
    set /a LEFT=50-!LAST_EPOCH!
    echo Detected progress: epoch !LAST_EPOCH!/50. Approx epochs remaining: !LEFT!.
  )
)

REM Launch training
python train_yolov8.py

REM Done
for /f "tokens=1-4 delims=/ " %%a in ("%date%") do set DATE=%%d-%%b-%%c
set TIMESTR=%time: =0%
set STAMP=%DATE%_%TIMESTR::=-%

echo [!STAMP!] Training finished.
endlocal


