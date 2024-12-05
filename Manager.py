import os
import shutil
from tkinter import filedialog, simpledialog, messagebox, ttk
import tkinter as tk

class FileManager:
    def __init__(self, parent):
        self.tab = ttk.Frame(parent)
        parent.add(self.tab, text="File Management")

        # Folder selection button
        ttk.Button(self.tab, text="Select Folder", command=self.select_folder).pack(pady=5)

        # Treeview for managing files
        self.file_tree = ttk.Treeview(
            self.tab, 
            columns=("Name", "Type", "Size"), 
            show="headings", 
            height=15
        )
        self.file_tree.heading("Name", text="File/Folder Name")
        self.file_tree.column("Name", width=300, anchor="w")
        self.file_tree.heading("Type", text="Type")
        self.file_tree.column("Type", width=100, anchor="center")
        self.file_tree.heading("Size", text="Size")
        self.file_tree.column("Size", width=100, anchor="center")
        self.file_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Bind right-click to show context menu
        self.file_tree.bind("<Button-3>", self.show_context_menu)

        # Context menu for file operations
        self.context_menu = tk.Menu(self.tab, tearoff=0)
        self.context_menu.add_command(label="Open", command=self.open_selected)
        self.context_menu.add_command(label="Rename", command=self.rename_selected)
        self.context_menu.add_command(label="Delete", command=self.delete_selected)

        # Store current folder path and its contents
        self.current_folder = ""
        self.folder_contents = []

    def select_folder(self):
        """Prompt the user to select a folder and display its contents."""
        folder_path = filedialog.askdirectory(title="Select Folder to Manage")
        if folder_path:
            self.current_folder = folder_path
            self.folder_contents = []  # Reset folder contents for the new folder

            # Clear the Treeview
            self.file_tree.delete(*self.file_tree.get_children())

            # Populate Treeview with folder contents
            for item in os.scandir(folder_path):
                if item.is_file():
                    file_type = os.path.splitext(item.name)[-1].lower()  # File extension
                    size = f"{os.path.getsize(item.path)} bytes"
                else:
                    file_type = "Folder"
                    size = ""  # No size for folders
                self.file_tree.insert(
                    "", "end", iid=item.path, 
                    values=(item.name, file_type, size)
                )

                # Add to folder contents for future reference
                self.folder_contents.append({"name": item.name, "path": item.path, "type": file_type, "size": size})

    def show_context_menu(self, event):
        """Show context menu on right-click."""
        selected_item = self.file_tree.identify_row(event.y)
        if selected_item:
            self.file_tree.selection_set(selected_item)  # Highlight the selected row
            self.context_menu.post(event.x_root, event.y_root)

    def open_selected(self):
        """Open the selected file or folder."""
        selected_item = self.file_tree.selection()
        if selected_item:
            path = selected_item[0]
            os.startfile(path)

    def rename_selected(self):
        """Rename the selected file or folder."""
        selected_item = self.file_tree.selection()
        if selected_item:
            path = selected_item[0]
            new_name = simpledialog.askstring("Rename", "Enter new name:")
            if new_name:
                new_path = os.path.join(os.path.dirname(path), new_name)
                os.rename(path, new_path)
                self.select_folder()  # Refresh the Treeview
                messagebox.showinfo("Success", "File/Folder renamed successfully.")

    def delete_selected(self):
        """Delete the selected file or folder."""
        selected_item = self.file_tree.selection()
        if selected_item:
            path = selected_item[0]
            if os.path.isdir(path):
                if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this folder?"):
                    shutil.rmtree(path)
            else:
                if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this file?"):
                    os.remove(path)
            self.select_folder()  # Refresh the Treeview
            messagebox.showinfo("Success", "File/Folder deleted successfully.")
