import os
from tkinter import filedialog, ttk, messagebox
import tkinter as tk

class DiskAnalyzer:
    def __init__(self, parent):
        self.tab = ttk.Frame(parent)
        parent.add(self.tab, text="Disk Space Analysis")

        # Directory selection
        ttk.Button(self.tab, text="Select Directory", command=self.analyze_directory).pack(pady=5)

        # Search bar
        search_frame = ttk.Frame(self.tab)
        search_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(search_frame, text="Search by Extension:").pack(side="left", padx=5)
        self.search_entry = ttk.Entry(search_frame, width=15)
        self.search_entry.pack(side="left", padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_files).pack(side="left", padx=5)

        # Directory statistics
        self.stats_label = tk.Label(self.tab, text="", font=("Arial", 12))
        self.stats_label.pack(pady=10)

        # Treeview for displaying directory contents
        self.analysis_tree = ttk.Treeview(
            self.tab, 
            columns=("Name", "Type", "Size"), 
            show="headings", 
            height=15
        )
        self.analysis_tree.heading("Name", text="File/Folder Name")
        self.analysis_tree.column("Name", width=300, anchor="w")
        self.analysis_tree.heading("Type", text="Type")
        self.analysis_tree.column("Type", width=100, anchor="center")
        self.analysis_tree.heading("Size", text="Size")
        self.analysis_tree.column("Size", width=100, anchor="center")
        self.analysis_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Store current directory and file info for search functionality
        self.current_directory = ""
        self.file_data = []

    def analyze_directory(self):
        """Analyze the selected directory and display its contents."""
        directory_path = filedialog.askdirectory(title="Select Directory for Analysis")
        if directory_path:
            self.current_directory = directory_path
            self.file_data = []  # Reset file data for the new directory
            total_files = 0
            total_size = 0

            # Clear the Treeview
            self.analysis_tree.delete(*self.analysis_tree.get_children())

            # Traverse the directory
            for item in os.scandir(directory_path):
                if item.is_file():
                    file_type = "File"
                    size = os.path.getsize(item.path)
                    total_files += 1
                    total_size += size
                else:
                    file_type = "Folder"
                    size = "-"
                self.analysis_tree.insert(
                    "", "end", iid=item.path, 
                    values=(item.name, file_type, f"{size} bytes" if size != "-" else size)
                )
                # Add to file data for search functionality
                self.file_data.append({"name": item.name, "path": item.path, "type": file_type, "size": size})

            # Display directory statistics
            self.stats_label.config(
                text=f"Directory: {directory_path}\nTotal Files: {total_files}\nTotal Size: {total_size / (1024**2):.2f} MB"
            )

    def search_files(self):
        """Filter the displayed files by the extension entered in the search bar."""
        if not self.current_directory:
            messagebox.showwarning("No Directory Selected", "Please select a directory first.")
            return

        extension = self.search_entry.get().strip().lower()
        if not extension.startswith("."):
            extension = f".{extension}"  # Ensure the extension starts with a dot

        # Filter files by extension
        filtered_files = [f for f in self.file_data if f["type"] == "File" and f["name"].lower().endswith(extension)]

        # Update Treeview with the filtered data
        self.analysis_tree.delete(*self.analysis_tree.get_children())  # Clear current contents
        for file in filtered_files:
            self.analysis_tree.insert(
                "", "end", iid=file["path"], 
                values=(file["name"], "File", f"{file['size']} bytes")
            )

        # Update statistics for filtered files
        total_filtered_size = sum(f["size"] for f in filtered_files)
        self.stats_label.config(
            text=f"Filtered Files: {len(filtered_files)}\nTotal Size: {total_filtered_size / (1024**2):.2f} MB"
        )
