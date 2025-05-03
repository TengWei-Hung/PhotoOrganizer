import os
import shutil
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

def get_exif_date(file_path):
    """Try to extract EXIF DateTimeOriginal from image file."""
    try:
        image = Image.open(file_path)
        exif_data = image._getexif()
        if exif_data:
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id)
                if tag == 'DateTimeOriginal':
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        print(f"Failed to read EXIF date from {file_path}: {e}")
    return None

def get_file_date(file_path):
    """Fallback: use file's last modified time."""
    timestamp = os.path.getmtime(file_path)
    return datetime.fromtimestamp(timestamp)

def organize_photos_by_date(source_folder):
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)

        if not os.path.isfile(file_path):
            continue

        # Only handle image files
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.heic', '.mov')):
            continue

        # Step 1: Try EXIF date
        date_taken = get_exif_date(file_path)

        # Step 2: Fallback to file modification date
        if not date_taken:
            date_taken = get_file_date(file_path)
            print(f"Using file date for: {filename}")

        # Format folder name: YYYY-MM-DD
        date_folder_name = date_taken.strftime("%Y-%m-%d")
        date_folder = os.path.join(source_folder, date_folder_name)
        os.makedirs(date_folder, exist_ok=True)

        dest_path = os.path.join(date_folder, filename)
        shutil.move(file_path, dest_path)
        print(f"Moved: {filename} -> {date_folder_name}")

# Set source folder (you can also use os.getcwd())
source_folder = r"D:\照片\2025.05.03_CellphoneBackup\CameraRoll"
organize_photos_by_date(source_folder)
