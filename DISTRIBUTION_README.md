# Face Recognition Attendance System

## Professional Standalone Application

A modern, professional face recognition attendance management system with auto-update capabilities and offline-first architecture.

## 🚀 Features

### Core Functionality
- **Face Registration**: Register new employees with department and position information
- **Automated Attendance**: Real-time face recognition for attendance tracking
- **Web Dashboard**: Professional web interface for viewing attendance reports
- **Database Management**: SQLite database with department and position tracking

### Professional Features
- **Modern GUI**: Professional interface with navigation and status indicators
- **Auto-Update System**: Automatic update checking and installation
- **Offline-First**: Works completely offline except for updates
- **Professional Styling**: Modern UI with consistent branding
- **Easy Installation**: One-click installer for Windows

## 📦 Installation

### Option 1: Installer (Recommended)
1. Download `FaceAttendanceSystem_Installer.exe`
2. Run the installer as Administrator
3. Follow the installation wizard
4. Launch from Desktop or Start Menu

### Option 2: Portable Version
1. Extract the ZIP file to your desired location
2. Run `FaceAttendanceSystem.exe` from the extracted folder
3. No installation required

## 🎯 Quick Start

### 1. Launch the Application
- **Main Application**: Double-click `FaceAttendanceSystem.exe` (Recommended)
- **Alternative**: Use the launcher script for individual components

### 2. Register Employees
1. Click "Register New Faces" or use the menu
2. Enter employee details:
   - Name (Required)
   - Department (Optional)
   - Position (Optional)
3. Position face in camera view
4. Click "Save Current Face" when ready
5. Repeat for multiple photos per person

### 3. Extract Features
1. After registering all employees
2. Click "Extract Features" or use menu
3. Wait for processing to complete

### 4. Take Attendance
1. Click "Take Attendance" or use menu
2. Position face in camera view
3. System will automatically recognize and record attendance
4. Audio confirmation will be provided

### 5. View Reports
1. Click "View Dashboard" or use menu
2. Web browser will open with attendance dashboard
3. Select date to view attendance records
4. Export data as needed

## 🔧 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11 (64-bit)
- **RAM**: 4GB
- **Storage**: 2GB free space
- **Camera**: USB webcam or built-in camera
- **Internet**: Required only for updates

### Recommended
- **OS**: Windows 11 (64-bit)
- **RAM**: 8GB
- **Storage**: 5GB free space
- **Camera**: HD webcam (720p or higher)
- **Internet**: Broadband connection for updates

## 📱 Application Components

### Main Application (`FaceAttendanceSystem.exe`)
- Professional GUI with navigation
- System dashboard and statistics
- Quick access to all features
- Auto-update management
- **Recommended for daily use**

### Individual Components
- **Face Registration** (`FaceRegistration.exe`): Register new employees
- **Attendance Taker** (`AttendanceTaker.exe`): Take attendance
- **Web Dashboard** (`AttendanceDashboard.exe`): View reports
- **Feature Extractor**: Process registered faces

## 🔄 Auto-Update System

The application includes an automatic update system:

### Features
- **Background Checking**: Checks for updates on startup
- **Manual Checking**: Use Help > Check for Updates
- **Progress Tracking**: Shows download progress
- **Automatic Installation**: Downloads and installs updates
- **Version Management**: Tracks current and available versions

### Update Process
1. Application checks for updates automatically
2. If update available, notification appears
3. Click "Update Now" to download
4. Progress bar shows download status
5. Installer runs automatically
6. Application restarts with new version

## 🗄️ Database Structure

### Attendance Table
- **name**: Employee name
- **department**: Department (optional)
- **position**: Position/role (optional)
- **time**: Check-in time
- **date**: Check-in date

### File Structure
```
FaceAttendanceSystem/
├── data/
│   ├── data_faces_from_camera/     # Employee face photos
│   ├── data_dlib/                  # AI models
│   └── features_all.csv           # Face recognition data
├── templates/                      # Web dashboard templates
├── attendance.db                   # SQLite database
├── version.json                   # Version information
└── FaceAttendanceSystem.exe       # Main application
```

## 🛠️ Troubleshooting

### Common Issues

#### Camera Not Working
- Ensure camera is connected and not used by other applications
- Check camera permissions in Windows Settings
- Try restarting the application

#### Face Recognition Not Working
- Ensure good lighting conditions
- Position face clearly in camera view
- Make sure features have been extracted after registration
- Check that face is registered in the system

#### Update Issues
- Check internet connection
- Ensure application is not running during update
- Try manual update from Help menu
- Restart application if update fails

#### Database Issues
- Check if `attendance.db` file exists
- Ensure application has write permissions
- Try running as Administrator

### Performance Optimization
- Close other applications using camera
- Ensure adequate lighting
- Use HD camera for better recognition
- Keep face database updated

## 📞 Support

### Documentation
- **User Manual**: Available in Help menu
- **GitHub Repository**: https://github.com/Ephraimraxy/Camera
- **Wiki**: https://github.com/Ephraimraxy/Camera/wiki

### Getting Help
1. Check this README for common solutions
2. Visit the GitHub repository for issues
3. Check the application's Help menu
4. Review the user manual

## 🔒 Privacy & Security

### Data Storage
- All data stored locally on your computer
- No data sent to external servers (except updates)
- Face images stored securely in local folders
- Database encrypted and protected

### Network Usage
- **Updates Only**: Internet used only for checking/downloading updates
- **No Data Transmission**: No personal data sent online
- **Offline Operation**: Full functionality without internet

## 📋 Version History

### Version 1.0.0 (Current)
- Initial professional release
- Modern GUI with navigation
- Auto-update system
- Department and position tracking
- Professional styling and branding
- One-click installer

## 🏢 Enterprise Features

### Multi-User Support
- Multiple employee registration
- Department-based organization
- Position tracking
- Comprehensive reporting

### Data Management
- SQLite database for reliability
- CSV export capabilities
- Web-based reporting
- Historical data tracking

### Professional Deployment
- Easy installation process
- Auto-update management
- Professional branding
- Comprehensive documentation

---

**© 2024 Face Recognition Attendance System. All rights reserved.**

*Developed with ❤️ for professional attendance management*
