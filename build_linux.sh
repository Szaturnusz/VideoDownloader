#!/bin/bash
set -e

APP_NAME="videodownloader"
VERSION="1.0.0"
ARCH="amd64"
MAINTAINER="Szaturnusz <info@example.com>"
DESC="Ultimate Video Downloader & Player"

echo "=== Building Linux Executable with PyInstaller ==="
# Clean previous builds
rm -rf build dist

# Build the executable
# --onefile: Create a single executable
# --windowed: No terminal window
# --icon: App icon
# --name: Output name
# --add-data: Include necessary files (if any, e.g., images)
# --collect-all: Ensure curl_cffi and other complex packages are included
pyinstaller --noconfirm --onefile --windowed --icon "app_icon.ico" --name "VideoDownloader" --collect-all curl_cffi --collect-all ttkbootstrap gui.py

echo "=== Creating Debian Package Structure ==="
DEB_DIR="deb_package/${APP_NAME}_${VERSION}_${ARCH}"
mkdir -p "$DEB_DIR/usr/bin"
mkdir -p "$DEB_DIR/usr/share/applications"
mkdir -p "$DEB_DIR/usr/share/icons/hicolor/256x256/apps"
mkdir -p "$DEB_DIR/DEBIAN"

# Copy executable
cp dist/VideoDownloader "$DEB_DIR/usr/bin/$APP_NAME"
chmod 755 "$DEB_DIR/usr/bin/$APP_NAME"

# Copy icon
cp app_icon.png "$DEB_DIR/usr/share/icons/hicolor/256x256/apps/$APP_NAME.png"

# Create .desktop file
cat > "$DEB_DIR/usr/share/applications/$APP_NAME.desktop" << EOL
[Desktop Entry]
Version=1.0
Type=Application
Name=Ultimate Video Downloader
Comment=Download videos from various sites
Exec=/usr/bin/$APP_NAME
Icon=$APP_NAME
Terminal=false
Categories=Network;Video;
Keywords=video;downloader;youtube;
EOL

# Create control file
# Depends: aria2 (for acceleration), ffmpeg (for conversion)
cat > "$DEB_DIR/DEBIAN/control" << EOL
Package: $APP_NAME
Version: $VERSION
Section: video
Priority: optional
Architecture: $ARCH
Maintainer: $MAINTAINER
Description: $DESC
 A powerful video downloader GUI using yt-dlp and aria2c.
 Supports multiple languages and high-speed downloads.
Depends: aria2, ffmpeg, python3
EOL

echo "=== Building .deb Package ==="
dpkg-deb --build "$DEB_DIR"

echo "=== Done! ==="
echo "Package created at: deb_package/${APP_NAME}_${VERSION}_${ARCH}.deb"
