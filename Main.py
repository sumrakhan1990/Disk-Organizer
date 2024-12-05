import tkinter as tk
from tkinter import ttk
from Analyzer import DiskAnalyzer
from Manager import FileManager
from Clean import DiskCleanup

class DiskOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disk Organizer")
        self.root.geometry("800x600")

        # Tabs
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True)

        # Initialize tabs
        self.disk_analyzer = DiskAnalyzer(self.tabs)
        self.file_manager = FileManager(self.tabs)
        self.disk_cleanup = DiskCleanup(self.tabs)

if __name__ == "__main__":
    root = tk.Tk()
    app = DiskOrganizerApp(root)
    root.mainloop()
