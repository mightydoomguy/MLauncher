import requests
import os
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from vars import minecraft_directory

BASE_URL = 'https://api.modrinth.com/v2'

ctk.set_appearance_mode("light")

class ModDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mod Downloader")
        self.root.geometry("600x600")

        self.create_widgets()

    def create_widgets(self):
        # Entry для поиска модов
        self.search_entry = ctk.CTkEntry(self.root, placeholder_text="Enter the name of the mod",width=1000)
        self.search_entry.pack(pady=10)

        # Кнопка для поиска модов
        self.search_button = ctk.CTkButton(self.root, text="Search Mods", command=self.search_mods_handler)
        self.search_button.pack(pady=5)

        # ScrollableFrame и Listbox для отображения модов
        self.mod_listbox_frame = tk.Frame(self.root)
        self.mod_listbox_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.mod_listbox = tk.Listbox(self.mod_listbox_frame, selectmode=tk.SINGLE)
        self.mod_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.mod_listbox_scrollbar = tk.Scrollbar(self.mod_listbox_frame, orient=tk.VERTICAL,
                                                  command=self.mod_listbox.yview)
        self.mod_listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.mod_listbox.config(yscrollcommand=self.mod_listbox_scrollbar.set)

        # Кнопка для выбора мода
        self.select_mod_button = ctk.CTkButton(self.root, text="Select Mod", command=self.select_mod_handler)
        self.select_mod_button.pack(pady=5)

        # ScrollableFrame и Listbox для отображения версий
        self.version_listbox_frame = tk.Frame(self.root)
        self.version_listbox_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.version_listbox = tk.Listbox(self.version_listbox_frame, selectmode=tk.SINGLE)
        self.version_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.version_listbox_scrollbar = tk.Scrollbar(self.version_listbox_frame, orient=tk.VERTICAL,
                                                      command=self.version_listbox.yview)
        self.version_listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.version_listbox.config(yscrollcommand=self.version_listbox_scrollbar.set)

        # Кнопка для выбора версии и загрузки
        self.select_version_button = ctk.CTkButton(self.root, text="Select Version and Download",
                                                   command=self.select_version_handler)
        self.select_version_button.pack(pady=5)

        self.selected_mod_id = None

    def search_mods(self, mod_name):
        params = {'query': mod_name}
        try:
            response = requests.get(f'{BASE_URL}/search', params=params)
            response.raise_for_status()
            return response.json().get('hits', [])
        except requests.RequestException as e:
            print(f"Error during search: {e}")
            return []

    def get_mod_versions(self, mod_id):
        try:
            response = requests.get(f'{BASE_URL}/project/{mod_id}/version')
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching versions: {e}")
            return []

    def download_mod(self, version_id, download_path):
        try:
            response = requests.get(f'{BASE_URL}/version/{version_id}')
            response.raise_for_status()
            version_info = response.json()
            download_url = version_info['files'][0]['url']
            mod_file_name = version_info['files'][0]['filename']
            mod_file_path = os.path.join(download_path, mod_file_name)

            download_response = requests.get(download_url)
            download_response.raise_for_status()
            with open(mod_file_path, 'wb') as file:
                file.write(download_response.content)

            print(f"Mod downloaded and saved to {mod_file_path}")
        except requests.RequestException as e:
            print(f"Error downloading mod: {e}")
        except IOError as e:
            print(f"Error saving file: {e}")

    def search_mods_handler(self):
        mod_name = self.search_entry.get()
        mods = self.search_mods(mod_name)

        self.mod_listbox.delete(0, tk.END)
        if not mods:
            self.mod_listbox.insert(tk.END, "No mods found.")
        else:
            for idx, mod in enumerate(mods):
                self.mod_listbox.insert(tk.END, f"{idx + 1}: {mod['title']}")

        # Убираем старые версии
        self.version_listbox.delete(0, tk.END)
        self.selected_mod_id = None

    def select_mod_handler(self):
        selected_mods = self.mod_listbox.curselection()
        if not selected_mods:
            print("Please select a mod first.")
            return

        mod_choice = int(selected_mods[0])
        mods = self.search_mods(self.search_entry.get())
        if mod_choice >= len(mods):
            print("Invalid mod selection.")
            return

        selected_mod = mods[mod_choice]
        self.selected_mod_id = selected_mod['project_id']
        mod_versions = self.get_mod_versions(self.selected_mod_id)

        self.version_listbox.delete(0, tk.END)
        for idx, version in enumerate(mod_versions):
            self.version_listbox.insert(tk.END, f"{idx + 1}: {version['name']} - {version['version_number']}")

    def select_version_handler(self):
        if self.selected_mod_id is None:
            print("Please select a mod first.")
            return

        selected_versions = self.version_listbox.curselection()
        if not selected_versions:
            print("Please select a version first.")
            return

        version_choice = int(selected_versions[0])
        mod_versions = self.get_mod_versions(self.selected_mod_id)
        if version_choice >= len(mod_versions):
            print("Invalid version selection.")
            return

        selected_version = mod_versions[version_choice]

        download_path = os.path.join(minecraft_directory, "mods")
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        self.download_mod(selected_version['id'], download_path)
        print(f"Mod version {selected_version['version_number']} downloaded successfully.")

    def runMOD(self):
        root = tk.Tk()
        app = ModDownloaderApp(root)
        root.mainloop()

