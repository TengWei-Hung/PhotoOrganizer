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
    current_lang = "zh"
    texts = {
        "zh": {
            "title": "照片整理工具",
            "select_folder": "選擇照片資料夾：",
            "browse": "瀏覽",
            "organize_by": "分類方式：",
            "year": "年份",
            "month": "月份",
            "day": "日期",
            "exclude": "是否排除子資料夾",
            "start": "開始整理",
            "warning_title": "警告",
            "warning_folder": "請選擇資料夾。",
            "done_title": "完成",
            "done": "照片已依{mode}分類！",
            "toggle": "Switch to English",
        },
        "en": {
            "title": "Photo Organizer",
            "select_folder": "Select Photo Folder:",
            "browse": "Browse",
            "organize_by": "Organize by:",
            "year": "Year",
            "month": "Month",
            "day": "Day",
            "exclude": "Exclude subfolders",
            "start": "Start Organizing",
            "warning_title": "Warning",
            "warning_folder": "Please select a folder.",
            "done_title": "Done",
            "done": "Photos organized by {mode}!",
            "toggle": "切換至繁體中文",
        },
    }

    def t(key):
        return texts[current_lang][key]

    def choose_folder():
        folder = filedialog.askdirectory()
        if folder:
            folder_var.set(folder)

    def run_sorting():
        folder = folder_var.get()
        mode = mode_var.get()
        exclude = exclude_var.get()
        if not folder:
            messagebox.showwarning(t("warning_title"), t("warning_folder"))
            return
        organize_photos(folder, mode, exclude_subfolders=exclude)
        messagebox.showinfo(t("done_title"), t("done").format(mode=t(mode)))

    def toggle_language():
        nonlocal current_lang
        current_lang = "en" if current_lang == "zh" else "zh"
        update_texts()

    def update_texts():
        root.title(t("title"))
        select_label.config(text=t("select_folder"))
        browse_btn.config(text=t("browse"))
        organize_label.config(text=t("organize_by"))
        year_rb.config(text=t("year"))
        month_rb.config(text=t("month"))
        day_rb.config(text=t("day"))
        exclude_cb.config(text=t("exclude"))
        start_btn.config(text=t("start"))
        toggle_btn.config(text=t("toggle"))

    root = tk.Tk()

    select_label = tk.Label(root)
    select_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
    folder_var = tk.StringVar()
    tk.Entry(root, textvariable=folder_var, width=40).grid(row=0, column=1, padx=5)
    browse_btn = tk.Button(root, command=choose_folder)
    browse_btn.grid(row=0, column=2, padx=5)

    mode_var = tk.StringVar(value="year")
    organize_label = tk.Label(root)
    organize_label.grid(row=1, column=0, sticky="w", padx=10)
    year_rb = tk.Radiobutton(root, variable=mode_var, value="year")
    year_rb.grid(row=1, column=1, sticky="w")
    month_rb = tk.Radiobutton(root, variable=mode_var, value="month")
    month_rb.grid(row=2, column=1, sticky="w")
    day_rb = tk.Radiobutton(root, variable=mode_var, value="day")
    day_rb.grid(row=3, column=1, sticky="w")

    exclude_var = tk.BooleanVar(value=True)
    exclude_cb = tk.Checkbutton(root, variable=exclude_var)
    exclude_cb.grid(row=4, column=1, sticky="w", pady=5)

    start_btn = tk.Button(root, command=run_sorting, bg="lightblue")
    start_btn.grid(row=5, column=1, pady=10)

    toggle_btn = tk.Button(root, command=toggle_language)
    toggle_btn.grid(row=6, column=1, pady=5)

    update_texts()

    root.mainloop()

if __name__ == "__main__":
    start_gui()
