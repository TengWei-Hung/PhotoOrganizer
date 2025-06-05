import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

# === 日期讀取 ===
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
    return datetime.fromtimestamp(os.path.getmtime(file_path))

# === 照片分類主邏輯 ===
def organize_photos(folder, mode, exclude_subfolders=True):
    if exclude_subfolders:
        walkers = [(folder, [], os.listdir(folder))]
    else:
        walkers = os.walk(folder)
    for root, _, files in walkers:
        for filename in files:
            file_path = os.path.join(root, filename)
            if not os.path.isfile(file_path):
                continue
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.heic', '.mov', '.mp4')):
                continue

            date_taken = get_exif_date(file_path)
            if not date_taken:
                date_taken = get_file_date(file_path)

            if mode == "year":
                folder_name = date_taken.strftime("%Y")
            elif mode == "month":
                folder_name = date_taken.strftime("%Y-%m")
            else:  # day
                folder_name = date_taken.strftime("%Y-%m-%d")

            dest_dir = os.path.join(folder, folder_name)
            os.makedirs(dest_dir, exist_ok=True)

            dest_path = os.path.join(dest_dir, filename)
            if os.path.exists(dest_path):
                base, ext = os.path.splitext(filename)
                dest_path = os.path.join(dest_dir, f"{base}_{int(datetime.now().timestamp())}{ext}")

            shutil.move(file_path, dest_path)

# === Tkinter GUI ===
def start_gui():
    def choose_folder():
        folder = filedialog.askdirectory()
        if folder:
            folder_var.set(folder)

    def run_sorting():
        folder = folder_var.get()
        mode = mode_var.get()
        exclude = exclude_var.get()
        if not folder:
            messagebox.showwarning("Warning", "Please select a folder.")
            return
        organize_photos(folder, mode, exclude_subfolders=exclude)
        messagebox.showinfo("Done", f"Photos organized by {mode}!")

    root = tk.Tk()
    root.title("Photo Organizer")

    tk.Label(root, text="Select Photo Folder:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    folder_var = tk.StringVar()
    tk.Entry(root, textvariable=folder_var, width=40).grid(row=0, column=1, padx=5)
    tk.Button(root, text="Browse", command=choose_folder).grid(row=0, column=2, padx=5)

    mode_var = tk.StringVar(value="year")
    tk.Label(root, text="Organize by:").grid(row=1, column=0, sticky="w", padx=10)
    tk.Radiobutton(root, text="Year", variable=mode_var, value="year").grid(row=1, column=1, sticky="w")
    tk.Radiobutton(root, text="Month", variable=mode_var, value="month").grid(row=2, column=1, sticky="w")
    tk.Radiobutton(root, text="Day", variable=mode_var, value="day").grid(row=3, column=1, sticky="w")

    exclude_var = tk.BooleanVar(value=True)
    tk.Checkbutton(root, text="是否排除子資料夾", variable=exclude_var).grid(row=4, column=1, sticky="w", pady=5)

    tk.Button(root, text="Start Organizing", command=run_sorting, bg="lightblue").grid(row=5, column=1, pady=10)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
