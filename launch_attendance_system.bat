@echo off
title Face Recognition Attendance System
echo ========================================
echo   Face Recognition Attendance System
echo ========================================
echo.
echo Choose an option:
echo 1. Main Application (Recommended)
echo 2. Register New Faces
echo 3. Take Attendance
echo 4. View Attendance Dashboard
echo 5. Extract Features (Run after registering faces)
echo 6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" (
    echo Starting Main Application...
    start "" "dist\FaceAttendanceSystem\FaceAttendanceSystem.exe"
) else if "%choice%"=="2" (
    echo Starting Face Registration...
    start "" "dist\FaceRegistration\FaceRegistration.exe"
) else if "%choice%"=="3" (
    echo Starting Attendance Taker...
    start "" "dist\AttendanceTaker\AttendanceTaker.exe"
) else if "%choice%"=="4" (
    echo Starting Web Dashboard...
    start "" "dist\AttendanceDashboard\AttendanceDashboard.exe"
    echo Opening web browser...
    timeout /t 3
    start http://localhost:5000
) else if "%choice%"=="5" (
    echo Extracting features...
    python features_extraction_to_csv.py
    pause
) else if "%choice%"=="6" (
    exit
) else (
    echo Invalid choice. Please try again.
    pause
    goto :eof
)
