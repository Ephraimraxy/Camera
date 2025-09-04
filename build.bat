@echo off
title Building Face Recognition Attendance System
echo ========================================
echo   Building Face Recognition System
echo ========================================
echo.

echo Installing required packages...
pip install pyinstaller auto-py-to-exe

echo.
echo Running build script...
python build_exe.py

echo.
echo Build completed! Check the 'dist' folder for executables.
pause
