@echo off
setlocal ENABLEDELAYEDEXPANSION
cd /d %~dp0

echo ==============================
echo 🧹 Clean repository (safe)
echo ==============================
echo This will remove derived/heavy artifacts only.
echo It will NOT delete your code.
echo.
echo To proceed, press Y then Enter. To cancel, press any other key.
set /p OK=Proceed (Y/N)? 
if /I not "%OK%"=="Y" (
  echo Cancelled.
  goto :end
)

rem Remove Ultralytics runs (training logs and checkpoints)
if exist runs (
  echo Deleting runs\ ...
  rmdir /s /q runs
)

rem Remove YOLO-converted dataset folder
if exist yolo (
  echo Deleting yolo\ ...
  rmdir /s /q yolo
)

rem Remove Streamlit cache
if exist .streamlit (
  echo Deleting .streamlit\ ...
  rmdir /s /q .streamlit
)

rem Remove Python caches
for /f "delims=" %%D in ('dir /s /b /ad __pycache__ 2^>nul') do (
  echo Deleting %%D ...
  rmdir /s /q "%%D"
)

rem Remove large weight/binary artifacts from repo root (keeps dataset images)
for %%E in (pt onnx engine tflite) do (
  for /f "delims=" %%F in ('dir /b *.%%E 2^>nul') do (
    echo Deleting %%F ...
    del /q "%%F"
  )
)

echo Done.

:end
endlocal

