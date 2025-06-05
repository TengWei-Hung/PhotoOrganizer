import os
import shutil
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

def get_exif_date(file_path):
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
    timestamp = os.path.getmtime(file_path)
    return datetime.fromtimestamp(timestamp)

def _iter_files(source_folder, exclude_subfolders):
    if exclude_subfolders:
        for filename in os.listdir(source_folder):
            file_path = os.path.join(source_folder, filename)
            if os.path.isfile(file_path):
                yield file_path
    else:
        for root, _, files in os.walk(source_folder):
            for filename in files:
                yield os.path.join(root, filename)


def organize_photos_by_month(source_folder, exclude_subfolders=True):
    for file_path in _iter_files(source_folder, exclude_subfolders):
        filename = os.path.basename(file_path)

        if not os.path.isfile(file_path):
            continue

        if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.heic', '.mov', '.mp4')):
            continue

        date_taken = get_exif_date(file_path)
        if not date_taken:
            date_taken = get_file_date(file_path)
            print(f"[Fallback] {filename} - used file date")

        month_folder_name = date_taken.strftime("%Y-%m")
        month_folder_path = os.path.join(source_folder, month_folder_name)
        os.makedirs(month_folder_path, exist_ok=True)

        dest_path = os.path.join(month_folder_path, filename)
        if os.path.exists(dest_path):
            base, ext = os.path.splitext(filename)
            dest_path = os.path.join(month_folder_path, f"{base}_{int(datetime.now().timestamp())}{ext}")

        shutil.move(file_path, dest_path)
        print(f"Moved: {filename} -> {month_folder_name}/")

# ⚠️ Replace this path with your actual folder path
source_folder = r"D:\照片\2025.05.03_CellphoneBackup\CameraRoll"
organize_photos_by_month(source_folder, exclude_subfolders=True)

