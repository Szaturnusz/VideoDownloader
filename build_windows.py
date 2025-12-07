import PyInstaller.__main__
import os
import shutil

# Configuration
APP_NAME = "VideoDownloader"
MAIN_SCRIPT = "gui.py"
ICON_FILE = "app_icon.ico"

def build():
    print("=== Building Windows Executable ===")
    
    # PyInstaller arguments
    args = [
        MAIN_SCRIPT,
        '--name=%s' % APP_NAME,
        '--onefile',
        '--windowed',
        '--icon=%s' % ICON_FILE,
        '--noconfirm',
        '--clean',
        # Collect packages that might be missed
        '--collect-all=curl_cffi',
        '--collect-all=ttkbootstrap',
        '--collect-all=PIL',
        '--hidden-import=PIL._tkinter_finder',
        '--hidden-import=PIL.ImageTk',
    ]
    
    PyInstaller.__main__.run(args)
    
    print("=== Build Complete ===")
    print(f"Executable is in the 'dist' folder: dist/{APP_NAME}.exe")
    print("\nIMPORTANT FOR WINDOWS USERS:")
    print("1. Download 'aria2c.exe' and 'ffmpeg.exe' (static builds).")
    print("2. Place them in the SAME folder as VideoDownloader.exe")
    print("   OR add them to your System PATH.")

if __name__ == "__main__":
    build()
