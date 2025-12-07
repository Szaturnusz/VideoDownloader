# Ultimate Video Downloader

A powerful, modern GUI video downloader application built with Python, `ttkbootstrap`, and `yt-dlp`. It supports downloading videos from thousands of websites with high-speed acceleration using `aria2c`.

![App Icon](app_icon.png)

## Features

*   **Modern GUI:** Clean, dark-themed interface using `ttkbootstrap`.
*   **High Speed:** Integrated `aria2c` support for multi-connection downloading.
*   **Smart Conversion:** Automatically converts videos to MP4 format for maximum compatibility.
*   **Multi-language Support:** Auto-detects system language (Supports English, Hungarian, German, Russian, and more).
*   **Custom Filenames:** Option to rename files before downloading.
*   **Clipboard Integration:** Right-click to paste URLs easily.
*   **Management:** Open download folder, play videos, or delete unwanted files directly from the app.
*   **Anti-Bot:** Built-in mechanisms to bypass Cloudflare and other protections.

## ⚠️ Important Note on Speed

**Please note that the actual download speed is highly dependent on your internet connection bandwidth and the target server's upload limits.** While this application uses acceleration technologies (multi-threading), it cannot exceed the physical limits of your network or the restrictions placed by the video hosting provider.

## Installation & Usage

### Linux

#### Option 1: Install via .deb package (Recommended)
If you have the `.deb` file:
```bash
sudo dpkg -i videodownloader_5.2.1_amd64.deb
sudo apt-get install -f  # To install dependencies like aria2 and ffmpeg
```

#### Option 2: Run from Source
1.  Ensure you have Python 3.12+ installed.
2.  Install system dependencies:
    ```bash
    sudo apt install python3-venv python3-tk aria2 ffmpeg
    ```
3.  Run the startup script:
    ```bash
    ./run.sh
    ```

#### Building the .deb Package
To create your own installer:
```bash
./build_linux.sh
```

### Windows

#### Option 1: Run from Source
1.  Install Python 3.12+.
2.  Install dependencies:
    ```cmd
    pip install -r requirements.txt
    ```
3.  **Crucial Step:** Download `ffmpeg.exe` and `aria2c.exe` and place them in the project folder (or add them to your System PATH).
4.  Run the application:
    ```cmd
    python gui.py
    ```

#### Option 2: Build .exe
1.  Install PyInstaller: `pip install pyinstaller`
2.  Run the build script:
    ```cmd
    python build_windows.py
    ```
3.  The executable will be in the `dist` folder. Don't forget to copy `ffmpeg.exe` and `aria2c.exe` next to the generated `.exe` file!

## Requirements

*   Python 3.12 or higher
*   `ffmpeg` (for video conversion)
*   `aria2` (for download acceleration)
*   Internet connection

## License

This project is for educational purposes. Please respect copyright laws and the terms of service of the websites you download from.
# VideoDownloader
