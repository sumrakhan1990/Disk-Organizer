import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk

class DiskCleanup:
    def __init__(self, parent):
        self.tab = ttk.Frame(parent)
        parent.add(self.tab, text="Disk Clean")

        ttk.Button(self.tab, text="Delete Temporary Files", command=self.delete_temp_files).pack(pady=5)
        self.cleanup_result = tk.Label(self.tab, text="", font=("Arial", 12))
        self.cleanup_result.pack(pady=10)

    def delete_temp_files(self):
        temp_dir = os.environ.get("TEMP", "/tmp")
        total_deleted_size = 0

        if temp_dir:
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        file_size = os.path.getsize(file_path)
                        os.remove(file_path)
                        total_deleted_size += file_size
                    except Exception:
                        pass

        size_message = f"{total_deleted_size / (1024**2):.2f} MB of temporary files deleted."
        self.cleanup_result.config(text=size_message)
