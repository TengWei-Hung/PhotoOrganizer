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
    except Exception:
        pass
    return None

def get_file_date(file_path):
    """Fallback: use file's last modified time."""
    timestamp = os.path.getmtime(file_path)
    return datetime.fromtimestamp(timestamp)

def organize_photos_by_month(source_folder):
    for root, _, files in os.walk(source_folder):
        for filename in files:
            file_path = os.path.join(root, filename)

            if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.heic', '.mov')):
                continue

            # Step 1: EXIF
            date_taken = get_exif_date(file_path)

            # Step 2: fallback to file time
            if not date_taken:
                date_taken = get_file_date(file_path)
                print(f"[Fallback] Using file date for: {filename}")

            # Format: YYYY-MM
            month_folder_name = date_taken.strftime("%Y-%m")
            month_folder_path = os.path.join(source_folder, month_folder_name)
            os.makedirs(month_folder_path, exist_ok=True)

            # Move file
            dest_path = os.path.join(month_folder_path, filename)

            # Avoid overwriting same-named files from different folders
            if os.path.exists(dest_path):
                base, ext = os.path.splitext(filename)
                dest_path = os.path.join(month_folder_path, f"{base}_{int(datetime.now().timestamp())}{ext}")

            shutil.move(file_path, dest_path)
            print(f"Moved: {filename} -> {month_folder_name}/")

# 修改為你的實際根目錄，例如貓咪備份所在的根資料夾
source_folder = r"D:\照片\2025.05.03_CellphoneBackup\CameraRoll"
organize_photos_by_month(source_folder)
