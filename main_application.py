"""
Professional Face Recognition Attendance System
Main application with modern GUI, navigation, and auto-update
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import subprocess
import os
import sys
import threading
from datetime import datetime
import webbrowser
from version import VersionManager, check_updates_async

class ModernAttendanceApp:
    def __init__(self):
        self.root = tk.Tk()
        self.version_manager = VersionManager()
        self.setup_window()
        self.create_menu()
        self.create_main_interface()
        self.create_status_bar()
        
        # Check for updates on startup
        self.check_updates_on_startup()
    
    def setup_window(self):
        """Setup main window properties"""
        self.root.title("Face Recognition Attendance System v1.0.0")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Custom colors
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'light': '#ecf0f1',
            'dark': '#34495e'
        }
        
        # Configure custom styles
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground=self.colors['primary'])
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'), foreground=self.colors['dark'])
        self.style.configure('Primary.TButton', font=('Arial', 10, 'bold'))
        self.style.configure('Success.TButton', font=('Arial', 10, 'bold'))
        self.style.configure('Warning.TButton', font=('Arial', 10, 'bold'))
    
    def create_menu(self):
        """Create application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Register New Faces", command=self.open_face_registration)
        file_menu.add_command(label="Take Attendance", command=self.open_attendance_taker)
        file_menu.add_separator()
        file_menu.add_command(label="Extract Features", command=self.extract_features)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="View Attendance Dashboard", command=self.open_dashboard)
        tools_menu.add_command(label="Database Manager", command=self.open_database_manager)
        tools_menu.add_separator()
        tools_menu.add_command(label="Settings", command=self.open_settings)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Check for Updates", command=self.check_for_updates)
        help_menu.add_command(label="User Manual", command=self.open_manual)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_main_interface(self):
        """Create main interface with navigation"""
        # Main container
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Title and subtitle
        title_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        title_frame.pack(expand=True)
        
        tk.Label(title_frame, text="Face Recognition Attendance System", 
                font=('Arial', 20, 'bold'), fg='white', bg=self.colors['primary']).pack()
        tk.Label(title_frame, text="Professional Automated Attendance Management", 
                font=('Arial', 12), fg='#bdc3c7', bg=self.colors['primary']).pack()
        
        # Main content area
        content_frame = tk.Frame(main_frame, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Quick Actions
        left_panel = tk.Frame(content_frame, bg='white', width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left_panel.pack_propagate(False)
        
        self.create_quick_actions(left_panel)
        
        # Right panel - Dashboard
        right_panel = tk.Frame(content_frame, bg='white')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_dashboard(right_panel)
    
    def create_quick_actions(self, parent):
        """Create quick action buttons"""
        tk.Label(parent, text="Quick Actions", 
                font=('Arial', 14, 'bold'), bg='white', fg=self.colors['primary']).pack(pady=(0, 15))
        
        # Action buttons
        actions = [
            ("👤 Register New Faces", self.open_face_registration, self.colors['secondary']),
            ("📷 Take Attendance", self.open_attendance_taker, self.colors['success']),
            ("📊 View Dashboard", self.open_dashboard, self.colors['warning']),
            ("⚙️ Extract Features", self.extract_features, self.colors['dark']),
            ("🗄️ Database Manager", self.open_database_manager, self.colors['primary']),
            ("🔧 Settings", self.open_settings, self.colors['dark'])
        ]
        
        for text, command, color in actions:
            btn = tk.Button(parent, text=text, command=command,
                          font=('Arial', 10, 'bold'), bg=color, fg='white',
                          relief=tk.FLAT, padx=20, pady=12, cursor='hand2')
            btn.pack(fill=tk.X, pady=5)
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg=self.lighten_color(b['bg'])))
            btn.bind('<Leave>', lambda e, b=btn, c=color: b.config(bg=c))
    
    def create_dashboard(self, parent):
        """Create dashboard with system information"""
        tk.Label(parent, text="System Dashboard", 
                font=('Arial', 14, 'bold'), bg='white', fg=self.colors['primary']).pack(pady=(0, 15))
        
        # Stats frame
        stats_frame = tk.Frame(parent, bg='white')
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        # System stats
        stats = self.get_system_stats()
        
        stat_items = [
            ("Registered People", stats['registered_people'], self.colors['success']),
            ("Today's Attendance", stats['today_attendance'], self.colors['secondary']),
            ("Database Size", stats['db_size'], self.colors['warning']),
            ("System Status", stats['system_status'], self.colors['success'])
        ]
        
        for i, (label, value, color) in enumerate(stat_items):
            stat_frame = tk.Frame(stats_frame, bg=color, relief=tk.RAISED, bd=1)
            stat_frame.grid(row=0, column=i, padx=5, sticky='ew')
            stats_frame.grid_columnconfigure(i, weight=1)
            
            tk.Label(stat_frame, text=value, font=('Arial', 18, 'bold'), 
                    fg='white', bg=color).pack(pady=5)
            tk.Label(stat_frame, text=label, font=('Arial', 9), 
                    fg='white', bg=color).pack()
        
        # Recent activity
        activity_frame = tk.LabelFrame(parent, text="Recent Activity", 
                                     font=('Arial', 10, 'bold'), bg='white')
        activity_frame.pack(fill=tk.BOTH, expand=True)
        
        # Activity list
        activity_list = tk.Listbox(activity_frame, font=('Arial', 9), 
                                 bg='#f8f9fa', relief=tk.FLAT, bd=0)
        activity_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add some sample activities
        activities = [
            f"[{datetime.now().strftime('%H:%M')}] System started successfully",
            f"[{datetime.now().strftime('%H:%M')}] Database connection established",
            f"[{datetime.now().strftime('%H:%M')}] Ready for face registration",
            f"[{datetime.now().strftime('%H:%M')}] Camera system initialized"
        ]
        
        for activity in activities:
            activity_list.insert(tk.END, activity)
    
    def create_status_bar(self):
        """Create status bar at bottom"""
        status_frame = tk.Frame(self.root, bg=self.colors['light'], height=25)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        # Status labels
        self.status_label = tk.Label(status_frame, text="Ready", 
                                   font=('Arial', 9), bg=self.colors['light'])
        self.status_label.pack(side=tk.LEFT, padx=10, pady=2)
        
        # Version info
        version_label = tk.Label(status_frame, text=f"v{self.version_manager.get_current_version()}", 
                               font=('Arial', 9), bg=self.colors['light'], fg=self.colors['dark'])
        version_label.pack(side=tk.RIGHT, padx=10, pady=2)
    
    def get_system_stats(self):
        """Get system statistics"""
        try:
            # Count registered people
            people_count = 0
            faces_dir = "data/data_faces_from_camera"
            if os.path.exists(faces_dir):
                people_count = len([d for d in os.listdir(faces_dir) if os.path.isdir(os.path.join(faces_dir, d))])
            
            # Count today's attendance
            today_count = 0
            if os.path.exists("attendance.db"):
                import sqlite3
                conn = sqlite3.connect("attendance.db")
                cursor = conn.cursor()
                today = datetime.now().strftime('%Y-%m-%d')
                cursor.execute("SELECT COUNT(*) FROM attendance WHERE date = ?", (today,))
                today_count = cursor.fetchone()[0]
                conn.close()
            
            # Database size
            db_size = "0 KB"
            if os.path.exists("attendance.db"):
                size_bytes = os.path.getsize("attendance.db")
                if size_bytes > 1024:
                    db_size = f"{size_bytes // 1024} KB"
                else:
                    db_size = f"{size_bytes} B"
            
            return {
                'registered_people': people_count,
                'today_attendance': today_count,
                'db_size': db_size,
                'system_status': 'Online'
            }
        except Exception:
            return {
                'registered_people': 0,
                'today_attendance': 0,
                'db_size': '0 KB',
                'system_status': 'Error'
            }
    
    def lighten_color(self, color):
        """Lighten a hex color"""
        color_map = {
            '#2c3e50': '#34495e',
            '#3498db': '#5dade2',
            '#27ae60': '#58d68d',
            '#f39c12': '#f7dc6f',
            '#e74c3c': '#ec7063',
            '#34495e': '#5d6d7e'
        }
        return color_map.get(color, color)
    
    # Action methods
    def open_face_registration(self):
        """Open face registration window"""
        self.status_label.config(text="Opening Face Registration...")
        try:
            if os.path.exists("get_faces_from_camera_tkinter.py"):
                subprocess.Popen([sys.executable, "get_faces_from_camera_tkinter.py"])
                self.status_label.config(text="Face Registration opened")
            else:
                messagebox.showerror("Error", "Face registration module not found")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open face registration: {e}")
            self.status_label.config(text="Error opening Face Registration")
    
    def open_attendance_taker(self):
        """Open attendance taker"""
        self.status_label.config(text="Opening Attendance Taker...")
        try:
            if os.path.exists("attendance_taker.py"):
                subprocess.Popen([sys.executable, "attendance_taker.py"])
                self.status_label.config(text="Attendance Taker opened")
            else:
                messagebox.showerror("Error", "Attendance taker module not found")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open attendance taker: {e}")
            self.status_label.config(text="Error opening Attendance Taker")
    
    def open_dashboard(self):
        """Open web dashboard"""
        self.status_label.config(text="Opening Dashboard...")
        try:
            if os.path.exists("app.py"):
                # Start Flask app in background
                subprocess.Popen([sys.executable, "app.py"])
                # Wait a moment then open browser
                self.root.after(2000, lambda: webbrowser.open("http://localhost:5000"))
                self.status_label.config(text="Dashboard opened in browser")
            else:
                messagebox.showerror("Error", "Dashboard module not found")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open dashboard: {e}")
            self.status_label.config(text="Error opening Dashboard")
    
    def extract_features(self):
        """Extract features from registered faces"""
        self.status_label.config(text="Extracting features...")
        try:
            if os.path.exists("features_extraction_to_csv.py"):
                result = subprocess.run([sys.executable, "features_extraction_to_csv.py"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    messagebox.showinfo("Success", "Features extracted successfully!")
                    self.status_label.config(text="Features extracted successfully")
                else:
                    messagebox.showerror("Error", f"Feature extraction failed:\n{result.stderr}")
                    self.status_label.config(text="Feature extraction failed")
            else:
                messagebox.showerror("Error", "Feature extraction module not found")
        except Exception as e:
            messagebox.showerror("Error", f"Could not extract features: {e}")
            self.status_label.config(text="Error extracting features")
    
    def open_database_manager(self):
        """Open database management window"""
        messagebox.showinfo("Database Manager", "Database management feature coming soon!")
    
    def open_settings(self):
        """Open settings window"""
        messagebox.showinfo("Settings", "Settings panel coming soon!")
    
    def check_for_updates(self):
        """Check for updates manually"""
        self.status_label.config(text="Checking for updates...")
        check_updates_async(self.root, self.version_manager)
        self.status_label.config(text="Update check completed")
    
    def check_updates_on_startup(self):
        """Check for updates on application startup"""
        def startup_check():
            try:
                update_info = self.version_manager.check_for_updates()
                if update_info.get('has_update'):
                    self.root.after(0, lambda: messagebox.showinfo(
                        "Update Available", 
                        f"Version {update_info['online_version']} is available!\n"
                        f"Current version: {update_info['current_version']}\n\n"
                        f"Go to Help > Check for Updates to download."
                    ))
            except:
                pass  # Silent fail on startup
        
        threading.Thread(target=startup_check, daemon=True).start()
    
    def open_manual(self):
        """Open user manual"""
        messagebox.showinfo("User Manual", "User manual will open in your default browser")
        webbrowser.open("https://github.com/Ephraimraxy/Camera/wiki")
    
    def show_about(self):
        """Show about dialog"""
        about_text = f"""
Face Recognition Attendance System
Version {self.version_manager.get_current_version()}

A professional automated attendance management system
using advanced face recognition technology.

Features:
• Face Registration and Recognition
• Automated Attendance Tracking
• Web-based Dashboard
• Database Management
• Auto-update System

Developed by: Ephraimraxy
GitHub: https://github.com/Ephraimraxy/Camera

© 2024 All rights reserved.
        """
        messagebox.showinfo("About", about_text)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernAttendanceApp()
    app.run()
