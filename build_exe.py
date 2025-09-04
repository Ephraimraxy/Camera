#!/usr/bin/env python3
"""
Build script for Face Recognition Attendance System
Creates standalone executables for all components
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("✅ PyInstaller already installed")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installed successfully")

def create_spec_files():
    """Create PyInstaller spec files for each component"""
    
    # Main attendance taker spec
    attendance_spec = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['attendance_taker.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('data', 'data'),
        ('templates', 'templates'),
        ('attendance.db', '.'),
    ],
    hiddenimports=[
        'dlib',
        'cv2',
        'numpy',
        'pandas',
        'sqlite3',
        'pyttsx3',
        'datetime',
        'logging',
        'time'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AttendanceTaker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'  # Add your icon file here
)
"""
    
    # Face registration GUI spec
    registration_spec = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['get_faces_from_camera_tkinter.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('data', 'data'),
    ],
    hiddenimports=[
        'dlib',
        'cv2',
        'numpy',
        'tkinter',
        'PIL',
        'pyttsx3',
        'logging',
        'time',
        'os',
        'shutil'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='FaceRegistration',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI app, no console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'
)
"""
    
    # Web dashboard spec
    webapp_spec = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('attendance.db', '.'),
    ],
    hiddenimports=[
        'flask',
        'sqlite3',
        'datetime'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AttendanceDashboard',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'
)
"""
    
    # Write spec files
    with open('attendance_taker.spec', 'w') as f:
        f.write(attendance_spec)
    
    with open('face_registration.spec', 'w') as f:
        f.write(registration_spec)
    
    with open('web_dashboard.spec', 'w') as f:
        f.write(webapp_spec)
    
    print("✅ PyInstaller spec files created")

def build_executables():
    """Build all executables using PyInstaller"""
    print("🔨 Building executables...")
    
    # Build each component
    components = [
        ('attendance_taker.spec', 'AttendanceTaker'),
        ('face_registration.spec', 'FaceRegistration'),
        ('web_dashboard.spec', 'AttendanceDashboard')
    ]
    
    for spec_file, name in components:
        print(f"Building {name}...")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'PyInstaller',
                '--clean',
                '--noconfirm',
                spec_file
            ])
            print(f"✅ {name} built successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to build {name}: {e}")

def create_launcher_script():
    """Create a simple launcher script"""
    launcher = '''@echo off
title Face Recognition Attendance System
echo ========================================
echo   Face Recognition Attendance System
echo ========================================
echo.
echo Choose an option:
echo 1. Register New Faces
echo 2. Take Attendance
echo 3. View Attendance Dashboard
echo 4. Extract Features (Run after registering faces)
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo Starting Face Registration...
    start "" "dist\\FaceRegistration\\FaceRegistration.exe"
) else if "%choice%"=="2" (
    echo Starting Attendance Taker...
    start "" "dist\\AttendanceTaker\\AttendanceTaker.exe"
) else if "%choice%"=="3" (
    echo Starting Web Dashboard...
    start "" "dist\\AttendanceDashboard\\AttendanceDashboard.exe"
    echo Opening web browser...
    timeout /t 3
    start http://localhost:5000
) else if "%choice%"=="4" (
    echo Extracting features...
    python features_extraction_to_csv.py
    pause
) else if "%choice%"=="5" (
    exit
) else (
    echo Invalid choice. Please try again.
    pause
    goto :eof
)
'''
    
    with open('launch_attendance_system.bat', 'w') as f:
        f.write(launcher)
    
    print("✅ Launcher script created")

def create_installer_script():
    """Create NSIS installer script"""
    nsis_script = '''
!define APPNAME "Face Recognition Attendance System"
!define COMPANYNAME "Your Company"
!define DESCRIPTION "Automated attendance system using face recognition"
!define VERSIONMAJOR 1
!define VERSIONMINOR 0
!define VERSIONBUILD 0
!define HELPURL "https://github.com/Ephraimraxy/Camera"
!define UPDATEURL "https://github.com/Ephraimraxy/Camera"
!define ABOUTURL "https://github.com/Ephraimraxy/Camera"
!define INSTALLSIZE 500000

RequestExecutionLevel admin
InstallDir "$PROGRAMFILES\\${APPNAME}"
Name "${APPNAME}"
outFile "FaceAttendanceSystem_Installer.exe"

!include LogicLib.nsh

page directory
page instfiles

!macro VerifyUserIsAdmin
UserInfo::GetAccountType
pop $0
${If} $0 != "admin"
    messageBox mb_iconstop "Administrator rights required!"
    setErrorLevel 740
    quit
${EndIf}
!macroend

function .onInit
    setShellVarContext all
    !insertmacro VerifyUserIsAdmin
functionEnd

section "install"
    setOutPath $INSTDIR
    file /r "dist\\*"
    file "launch_attendance_system.bat"
    file "README.md"
    
    writeUninstaller "$INSTDIR\\uninstall.exe"
    
    createDirectory "$SMPROGRAMS\\${APPNAME}"
    createShortCut "$SMPROGRAMS\\${APPNAME}\\${APPNAME}.lnk" "$INSTDIR\\launch_attendance_system.bat" "" "$INSTDIR\\icon.ico"
    createShortCut "$SMPROGRAMS\\${APPNAME}\\Uninstall.lnk" "$INSTDIR\\uninstall.exe" "" "$INSTDIR\\uninstall.exe"
    
    createShortCut "$DESKTOP\\${APPNAME}.lnk" "$INSTDIR\\launch_attendance_system.bat" "" "$INSTDIR\\icon.ico"
sectionEnd

section "uninstall"
    delete "$INSTDIR\\uninstall.exe"
    rmDir /r "$INSTDIR"
    rmDir /r "$SMPROGRAMS\\${APPNAME}"
    delete "$DESKTOP\\${APPNAME}.lnk"
sectionEnd
'''
    
    with open('installer.nsi', 'w') as f:
        f.write(nsis_script)
    
    print("✅ NSIS installer script created")

def main():
    """Main build process"""
    print("🚀 Building Face Recognition Attendance System")
    print("=" * 50)
    
    # Step 1: Install PyInstaller
    install_pyinstaller()
    
    # Step 2: Create spec files
    create_spec_files()
    
    # Step 3: Build executables
    build_executables()
    
    # Step 4: Create launcher
    create_launcher_script()
    
    # Step 5: Create installer script
    create_installer_script()
    
    print("\n" + "=" * 50)
    print("✅ Build process completed!")
    print("\nNext steps:")
    print("1. Test the executables in the 'dist' folder")
    print("2. Install NSIS to create installer: https://nsis.sourceforge.io/")
    print("3. Run: makensis installer.nsi")
    print("4. Distribute the installer to users")
    print("\nFiles created:")
    print("- dist/AttendanceTaker/ (Main attendance system)")
    print("- dist/FaceRegistration/ (Face registration GUI)")
    print("- dist/AttendanceDashboard/ (Web dashboard)")
    print("- launch_attendance_system.bat (Easy launcher)")
    print("- installer.nsi (NSIS installer script)")

if __name__ == "__main__":
    main()
