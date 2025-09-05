
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
InstallDir "$PROGRAMFILES\${APPNAME}"
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
    file /r "dist\*"
    file "launch_attendance_system.bat"
    file "README.md"
    
    writeUninstaller "$INSTDIR\uninstall.exe"
    
    createDirectory "$SMPROGRAMS\${APPNAME}"
    createShortCut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\launch_attendance_system.bat" "" "$INSTDIR\icon.ico"
    createShortCut "$SMPROGRAMS\${APPNAME}\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe"
    
    createShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\launch_attendance_system.bat" "" "$INSTDIR\icon.ico"
sectionEnd

section "uninstall"
    delete "$INSTDIR\uninstall.exe"
    rmDir /r "$INSTDIR"
    rmDir /r "$SMPROGRAMS\${APPNAME}"
    delete "$DESKTOP\${APPNAME}.lnk"
sectionEnd
