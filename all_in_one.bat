@echo off
setlocal ENABLEDELAYEDEXPANSION

cd /d %~dp0

echo ==============================
echo 🍓 Strawberry Disease: One-Click
echo ==============================

rem Step 1: Install dependencies
echo [1/4] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
  echo Failed to install requirements. Exiting.
  goto :end
)

rem Optional: quiet OpenCV GUI backend warnings
pip install opencv-python-headless >nul 2>nul

rem Step 2: Convert LabelMe -> YOLO + dataset.yaml
echo [2/4] Converting annotations to YOLO format...
python tools\convert_labelme_to_yolo.py
if errorlevel 1 (
  echo Conversion failed. Exiting.
  goto :end
)

rem Step 3: Train or auto-resume
echo [3/4] Training (auto-resume if last.pt exists)...
python train_yolov8.py
if errorlevel 1 (
  echo Training exited with an error. Check logs in runs\...
  goto :end
)

rem Step 4: Detect on provided or sample image
set IMG=%~1
if "%IMG%"=="" (
  if exist "test\*.jpg" (
    for %%F in (test\*.jpg) do (
      set IMG=%%F
      goto afterfind
    )
  ) else if exist "train\*.jpg" (
    for %%F in (train\*.jpg) do (
      set IMG=%%F
      goto afterfind
    )
  )
)
:afterfind

if "%IMG%"=="" (
  echo [4/4] No sample image found. Skipping detection.
) else (
  echo [4/4] Running detection on: %IMG%
  python detect_strawberry.py "%IMG%"
)

echo Done.

:end
endlocal

