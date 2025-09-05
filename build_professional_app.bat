@echo off
title Building Professional Face Recognition Attendance System
color 0A
echo.
echo ================================================================
echo    Building Professional Face Recognition Attendance System
echo ================================================================
echo.
echo This script will create a professional standalone application
echo with modern GUI, auto-update system, and easy installation.
echo.
echo Features being built:
echo - Professional GUI with navigation
echo - Auto-update system
echo - One-click installer
echo - Offline-first architecture
echo - Modern styling and branding
echo.
pause

echo.
echo Step 1: Installing required packages...
echo ========================================
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)

echo.
echo Step 2: Creating application icon...
echo ====================================
python create_icon.py
if %errorlevel% neq 0 (
    echo WARNING: Could not create icon, continuing without it...
)

echo.
echo Step 3: Building professional application...
echo ============================================
python build_exe.py
if %errorlevel% neq 0 (
    echo ERROR: Build process failed
    pause
    exit /b 1
)

echo.
echo Step 4: Creating distribution package...
echo ========================================
if not exist "dist_package" mkdir dist_package
if not exist "dist_package\FaceAttendanceSystem" mkdir "dist_package\FaceAttendanceSystem"

echo Copying main application...
xcopy "dist\FaceAttendanceSystem\*" "dist_package\FaceAttendanceSystem\" /E /I /Y

echo Copying documentation...
copy "DISTRIBUTION_README.md" "dist_package\FaceAttendanceSystem\README.md"
copy "README.md" "dist_package\FaceAttendanceSystem\DEVELOPER_README.md"

echo Copying launcher...
copy "launch_attendance_system.bat" "dist_package\FaceAttendanceSystem\"

echo.
echo Step 5: Creating installer (if NSIS is available)...
echo ====================================================
where makensis >nul 2>nul
if %errorlevel% equ 0 (
    echo Creating installer with NSIS...
    makensis installer.nsi
    if %errorlevel% equ 0 (
        echo ✅ Installer created successfully!
        move "FaceAttendanceSystem_Installer.exe" "dist_package\"
    ) else (
        echo WARNING: Installer creation failed
    )
) else (
    echo INFO: NSIS not found. Installer not created.
    echo To create installer:
    echo 1. Download NSIS from https://nsis.sourceforge.io/
    echo 2. Run: makensis installer.nsi
)

echo.
echo ================================================================
echo                        BUILD COMPLETED!
echo ================================================================
echo.
echo Your professional application is ready!
echo.
echo Files created:
echo - dist_package\FaceAttendanceSystem\ (Main application folder)
echo - dist_package\FaceAttendanceSystem_Installer.exe (Installer - if NSIS available)
echo.
echo To distribute your application:
echo 1. Test the application in dist_package\FaceAttendanceSystem\
echo 2. Zip the FaceAttendanceSystem folder for portable distribution
echo 3. Use the installer for professional deployment
echo.
echo Main application: dist_package\FaceAttendanceSystem\FaceAttendanceSystem.exe
echo.
echo Features included:
echo ✅ Professional GUI with modern interface
echo ✅ Auto-update system with network checking
echo ✅ Offline-first architecture
echo ✅ Department and position tracking
echo ✅ Web dashboard integration
echo ✅ Easy installation and deployment
echo ✅ Professional styling and branding
echo.
echo Ready for professional distribution! 🚀
echo.
pause
