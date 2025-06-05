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
                    date_str = value
                    return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        print(f"Failed to read EXIF date from {file_path}: {e}")
    return None

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


def organize_photos_by_year(source_folder, exclude_subfolders=True):
    for file_path in _iter_files(source_folder, exclude_subfolders):
        filename = os.path.basename(file_path)

        if not os.path.isfile(file_path):
            continue

        # Check file extension (process images only)
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        date_taken = get_exif_date(file_path)
        if not date_taken:
            print(f"Capture date not found, skipping: {filename}")
            continue

        year_folder = os.path.join(source_folder, str(date_taken.year))
        os.makedirs(year_folder, exist_ok=True)

        dest_path = os.path.join(year_folder, filename)
        shutil.move(file_path, dest_path)
        print(f"Moved: {filename} -> {year_folder}")

# ⚠️ Modify this to the path of your source photo folder
source_folder = r"D:\Photos\2025.05.03_CellphoneBackup\CameraRoll"
organize_photos_by_year(source_folder, exclude_subfolders=True)
