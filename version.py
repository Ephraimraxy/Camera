"""
Version management and auto-update system for Face Recognition Attendance System
"""

import json
import os
import requests
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import threading
from datetime import datetime

class VersionManager:
    def __init__(self):
        self.current_version = "1.0.0"
        self.version_file = "version.json"
        self.update_url = "https://raw.githubusercontent.com/Ephraimraxy/Camera/main/version.json"
        self.download_url = "https://github.com/Ephraimraxy/Camera/releases/latest"
        
    def get_current_version(self):
        """Get current version from version.json file"""
        try:
            if os.path.exists(self.version_file):
                with open(self.version_file, 'r') as f:
                    data = json.load(f)
                    return data.get('version', self.current_version)
            return self.current_version
        except Exception:
            return self.current_version
    
    def save_version(self, version):
        """Save version to version.json file"""
        try:
            version_data = {
                "version": version,
                "last_updated": datetime.now().isoformat(),
                "build_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(self.version_file, 'w') as f:
                json.dump(version_data, f, indent=2)
        except Exception as e:
            print(f"Error saving version: {e}")
    
    def check_for_updates(self):
        """Check for updates online"""
        try:
            response = requests.get(self.update_url, timeout=10)
            if response.status_code == 200:
                online_data = response.json()
                online_version = online_data.get('version', '0.0.0')
                current_version = self.get_current_version()
                
                return {
                    'has_update': self.compare_versions(online_version, current_version),
                    'online_version': online_version,
                    'current_version': current_version,
                    'download_url': online_data.get('download_url', self.download_url),
                    'changelog': online_data.get('changelog', 'No changelog available')
                }
        except requests.exceptions.RequestException:
            return {'has_update': False, 'error': 'No internet connection'}
        except Exception as e:
            return {'has_update': False, 'error': str(e)}
    
    def compare_versions(self, version1, version2):
        """Compare two version strings"""
        def version_tuple(v):
            return tuple(map(int, v.split('.')))
        
        try:
            return version_tuple(version1) > version_tuple(version2)
        except:
            return False
    
    def download_update(self, download_url, progress_callback=None):
        """Download update file"""
        try:
            response = requests.get(download_url, stream=True, timeout=30)
            if response.status_code == 200:
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                filename = "update_installer.exe"
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if progress_callback and total_size > 0:
                                progress = (downloaded / total_size) * 100
                                progress_callback(progress)
                
                return filename
        except Exception as e:
            raise Exception(f"Download failed: {e}")

class UpdateDialog:
    def __init__(self, parent, version_manager):
        self.parent = parent
        self.version_manager = version_manager
        self.dialog = None
        
    def show_update_dialog(self, update_info):
        """Show update available dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Update Available")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 50,
            self.parent.winfo_rooty() + 50
        ))
        
        # Header
        header_frame = tk.Frame(self.dialog, bg='#2c3e50', height=60)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🔄 Update Available", 
                font=('Arial', 16, 'bold'), fg='white', bg='#2c3e50').pack(pady=15)
        
        # Content
        content_frame = tk.Frame(self.dialog, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Version info
        version_frame = tk.Frame(content_frame, bg='white')
        version_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(version_frame, text="Current Version:", font=('Arial', 10, 'bold'), bg='white').pack(anchor=tk.W)
        tk.Label(version_frame, text=update_info['current_version'], 
                font=('Arial', 10), bg='white', fg='#7f8c8d').pack(anchor=tk.W)
        
        tk.Label(version_frame, text="New Version:", font=('Arial', 10, 'bold'), bg='white').pack(anchor=tk.W, pady=(10, 0))
        tk.Label(version_frame, text=update_info['online_version'], 
                font=('Arial', 10), bg='white', fg='#27ae60').pack(anchor=tk.W)
        
        # Changelog
        tk.Label(content_frame, text="What's New:", font=('Arial', 10, 'bold'), bg='white').pack(anchor=tk.W, pady=(15, 5))
        
        changelog_text = tk.Text(content_frame, height=8, wrap=tk.WORD, 
                               font=('Arial', 9), bg='#f8f9fa', relief=tk.FLAT)
        changelog_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        changelog_text.insert(tk.END, update_info.get('changelog', 'No changelog available'))
        changelog_text.config(state=tk.DISABLED)
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Button(button_frame, text="Update Now", command=self.update_now,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold'),
                 relief=tk.FLAT, padx=20, pady=8).pack(side=tk.RIGHT, padx=(10, 0))
        
        tk.Button(button_frame, text="Later", command=self.dialog.destroy,
                 bg='#95a5a6', fg='white', font=('Arial', 10),
                 relief=tk.FLAT, padx=20, pady=8).pack(side=tk.RIGHT)
    
    def update_now(self):
        """Start update process"""
        self.dialog.destroy()
        self.show_progress_dialog()
    
    def show_progress_dialog(self):
        """Show download progress dialog"""
        progress_dialog = tk.Toplevel(self.parent)
        progress_dialog.title("Downloading Update")
        progress_dialog.geometry("400x200")
        progress_dialog.resizable(False, False)
        progress_dialog.transient(self.parent)
        progress_dialog.grab_set()
        
        # Center the dialog
        progress_dialog.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 100,
            self.parent.winfo_rooty() + 100
        ))
        
        tk.Label(progress_dialog, text="Downloading update...", 
                font=('Arial', 12, 'bold')).pack(pady=20)
        
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(progress_dialog, variable=progress_var, 
                                     maximum=100, length=300)
        progress_bar.pack(pady=10)
        
        status_label = tk.Label(progress_dialog, text="Preparing download...", 
                               font=('Arial', 9))
        status_label.pack(pady=5)
        
        def download_thread():
            try:
                update_info = self.version_manager.check_for_updates()
                if update_info.get('has_update'):
                    def progress_callback(progress):
                        progress_var.set(progress)
                        status_label.config(text=f"Downloading... {progress:.1f}%")
                        progress_dialog.update()
                    
                    filename = self.version_manager.download_update(
                        update_info['download_url'], progress_callback)
                    
                    progress_dialog.destroy()
                    self.install_update(filename)
                else:
                    progress_dialog.destroy()
                    messagebox.showerror("Error", "No update available")
            except Exception as e:
                progress_dialog.destroy()
                messagebox.showerror("Download Error", str(e))
        
        threading.Thread(target=download_thread, daemon=True).start()
        progress_dialog.mainloop()
    
    def install_update(self, filename):
        """Install the downloaded update"""
        try:
            if os.path.exists(filename):
                # Run the installer
                subprocess.Popen([filename], shell=True)
                messagebox.showinfo("Update", "Update installer started. Please follow the installation wizard.")
                sys.exit(0)  # Close current application
            else:
                messagebox.showerror("Error", "Update file not found")
        except Exception as e:
            messagebox.showerror("Installation Error", str(e))

def check_updates_async(parent, version_manager):
    """Check for updates in background thread"""
    def check_thread():
        try:
            update_info = version_manager.check_for_updates()
            if update_info.get('has_update'):
                # Show update dialog on main thread
                parent.after(0, lambda: UpdateDialog(parent, version_manager).show_update_dialog(update_info))
            elif update_info.get('error'):
                # Show error on main thread
                parent.after(0, lambda: messagebox.showwarning("Update Check", f"Could not check for updates: {update_info['error']}"))
        except Exception as e:
            parent.after(0, lambda: messagebox.showerror("Update Error", str(e)))
    
    threading.Thread(target=check_thread, daemon=True).start()
