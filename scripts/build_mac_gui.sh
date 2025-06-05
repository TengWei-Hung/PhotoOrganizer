#!/bin/bash
# Build PhotoOrganizer GUI for macOS using PyInstaller
# Requires: pip install pyinstaller
set -e

pyinstaller --noconfirm --windowed --name PhotoOrganizer gui/photo_gui_launcher.py

if [ -d dist/PhotoOrganizer.app ]; then
    (cd dist && zip -r PhotoOrganizer_mac.zip PhotoOrganizer.app)
fi
