import sys
import tkinter.messagebox
import urllib.request

import customtkinter as ctkin
import minecraft_launcher_lib.forge
import psutil
import threading
import uuid
from vars import *
import requests
import subprocess
import zipfile
import shutil
import CTkListbox
from bs4 import BeautifulSoup
from TopLevelWindowASS import *
ctkin.set_appearance_mode("dark")
ctkin.set_default_color_theme("green")
max_ram = psutil.virtual_memory().total
total_mem_gb = round(max_ram / (1024 ** 3))

class MLauncher(ctkin.CTk):
    def __init__(self):
        super(MLauncher,self).__init__()
        self.title("SomeLauncher")
        self.geometry("1250x750")
        self.iconbitmap(bitmap="rocket.ico")
        self.resizable(True, True)
        self.widget()
        self.grid()
        self.load_config_values()
        self.ram_value = cfg_data['user_ram']
        self.setup_frame.pack_forget()
        self.btn_frame.pack_forget()
        self.show_launch()
        self.toplevel_window = None
        self.toplevel_select_mods = None



    def load_config_values(self):
        # Загрузка значений из config.ini
        self.cfg_data = Config['DEFAULT']
        username = self.cfg_data.get('nickname', '')  # Получение никнейма из конфигурации
        user_ram = self.cfg_data.get('user_ram')  # Получение объема памяти из конфигурации

        self.userInput.insert(0,username)
        self.ram_allocation_select_label.configure(text=user_ram)
        self.ram_allocation_select.set(int(user_ram))
    def show_profile(self):
        self.mod_frame.pack_forget()
        self.launch_frame.pack_forget()
        self.btn_frame.pack_forget()
        self.mod_search_filters.pack_forget()
        self.available_mod_frame.pack_forget()
        #self.search_frame.pack_forget()
        self.setup_frame.pack(fill=ctkin.BOTH,expand=True)

    def show_launch(self):
        self.mod_frame.pack_forget()
        self.setup_frame.pack_forget()
        self.btn_frame.pack_forget()
        self.mod_search_filters.pack_forget()
        #self.search_frame.pack_forget()
        self.launch_frame.pack(fill=ctkin.BOTH)
        self.available_mod_frame.pack(side="right", anchor="w",expand=True)


    def show_mods(self):
        self.setup_frame.pack_forget()
        self.launch_frame.pack_forget()
        self.available_mod_frame.pack_forget()
        self.mod_search_filters.pack(fill=ctkin.X,anchor="ne",side="right")
        self.mod_frame.pack(fill=ctkin.BOTH)
        self.btn_frame.pack(fill=ctkin.X,anchor="nw",side='left')
        #self.search_frame.pack(fill=ctkin.X)

    def install_minecraft(self):
        self.vanilla_version = self.new_version_select.get()
        try:
            if self.forge_var.get() == "on":
                self.forge_version = minecraft_launcher_lib.forge.find_forge_version(self.vanilla_version)

                callback = {
                    "setStatus": lambda text: self.progress_label.configure(text=text),
                    "setProgress": lambda int: self.progress_bar.set(int)

                }
                minecraft_launcher_lib.forge.install_forge_version(self.forge_version, minecraft_directory,
                                                                   callback=callback)
                self.progress_label.configure(text=f"Forge Version ({self.forge_version}) successfully download")
                #minecraft_launcher_lib.forge.run_forge_installer(self.forge_version)
            elif self.fabric_var.get() == "on":
                callback = {
                    "setStatus": lambda text: self.progress_label.configure(text=text),
                    "setProgress": lambda int: self.progress_bar.set(int)}
                minecraft_launcher_lib.fabric.install_fabric(self.vanilla_version, minecraft_directory, callback=callback)

            elif self.quilt_var.get() == 'on':
                callback = {
                    "setStatus": lambda text: self.progress_label.configure(text=text),
                    "setProgress": lambda int: self.progress_bar.set(int)}
                minecraft_launcher_lib.quilt.install_quilt(self.vanilla_version,minecraft_directory,callback=callback)

            elif self.forge_var.get() == "off" and self.fabric_var.get() == "off":
                callback = {
                    "setStatus": lambda text: self.progress_label.configure(text=text),
                    "setProgress": lambda int: self.progress_bar.set(int)}
                minecraft_launcher_lib.install.install_minecraft_version(self.vanilla_version, minecraft_directory,
                                                                         callback=callback)
        except Exception as e:
            print(f"Error:{str(e)}")

    def update_version_list(self):
        for version in minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory):
            availible_version_list.append(version['id'])

    def thread_install(self):
        self.thread = threading.Thread(target=self.install_minecraft)
        self.thread.start()
        self.thread1 = threading.Thread(target=self.update_version_list)
        self.thread1.start()

    def open_mine_dir(self):
        subprocess.Popen(f'explorer.exe "{minecraft_directory}"')

    def sliding(self,ram_value):
        self.ram_value = int(self.ram_allocation_select.get())
        self.ram_allocation_select_label.configure(text=self.ram_value)
    def launch_minecraft(self):
        uid = str(uuid.uuid1())
        username = self.userInput.get()
        ram_value = self.ram_value
        if username != self.cfg_data['nickname'] or ram_value != self.cfg_data['user_ram']:
            cfg_data['uid'] = uid
            cfg_data['nickname'] = username
            cfg_data['user_ram'] = str(ram_value)
            with open('config.ini', 'w') as f:
                Config.write(f)

        options = {
            "username": cfg_data['nickname'],
            'uuid': cfg_data['uid'],
            "token": '',
            "jvmArguments": [f"-Xmx{cfg_data['user_ram']}G"]
        }
        self.save_mod_selections()
        subprocess.Popen(
            minecraft_launcher_lib.command.get_minecraft_command(version=self.availible_version_select.get(),
                                                                 minecraft_directory=minecraft_directory,
                                                                 options=options))

    def install_mod(self):
        mod_url = self.mod_url_entry.get()
        if not mod_url:
            self.mod_label.configure(text="URL модификации не указан.")
            return

        real_download_url = self.get_real_download_url(mod_url)
        print(real_download_url)
        mods_dir = minecraft_directory + "\\mods\\"
        filemodname = self.getJarName(mod_url) + '.jar'
        mods_dir_file = mods_dir + filemodname

        try:
            response = requests.get(real_download_url)
            response.raise_for_status()

            with open(mods_dir_file,"wb") as file:
                file.write(response.content)
            print(f"Jar файл успешно загружен и сохранен как {mods_dir_file}")
            self.mod_label.configure(text=f"Jar файл успешно загружен и сохранен как {mods_dir_file}")
            self.mod_label.configure(text="")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при загрузке jar файла: {str(e)}")

    def get_real_download_url(self, page_url):
        try:
            response = requests.get(page_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for a_tag in soup.find_all('a'):
                    href = a_tag.get('href', '')
                    if 'download' in href:
                        #print(href)
                        return href
                self.mod_label.configure(text="Не удалось найти кнопку загрузки или отсутствует атрибут href.")
                return None
            else:
                self.mod_label.configure(text=f"Ошибка при получении страницы: {response.status_code}")
                return None
        except Exception as e:
            self.mod_label.configure(text=f"Ошибка при парсинге страницы: {str(e)}")
            return None

    def getJarName(self,page_url):
        try:
            response = requests.get(page_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text,"html.parser")
                for title_tag in soup.find_all('h1'):
                    title = title_tag.getText()
                    print(title)
                    return title
        except Exception as e:
            print("Не удалось взять имя файла" + e)

    def search_mod(self):
        keyword_query = self.keyword_input.get()
        version_mod_for_link = self.version_mod_list.get()


        #search_url = f"https://minecraft-inside.ru/mods/"
        self.mod_lst_box.delete(0,'end')
        if self.use_filters_var.get() == 'on':
            search_url = f"https://minecraft-inside.ru/mods/{version_mod_for_link}/"

        # Параметры запроса
            params = {
                    'q': keyword_query,
                }
            response = requests.get(search_url,params)
        elif self.use_filters_var.get() == 'off':
            search_url = f"https://minecraft-inside.ru/mods/"
            params = { 'q':keyword_query}
            response = requests.get(search_url,params)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text,"html.parser")

            results = soup.find_all("div",class_= "box box_grass post")

            for result in results:
                link = result.find("a")['href']
                self.mod_lst_box.insert("end",link_template+link)

    def install_selected_mod(self):
        selected_mod = self.mod_lst_box.get(self.mod_lst_box.curselection())
        if not selected_mod:
            self.mod_label.configure(text="Пожалуйста, выберите мод для установки.")
            return

        mod_url = selected_mod
        real_download_url = self.get_real_download_url(mod_url)
        if not real_download_url:
            self.mod_label.configure(text="Ошибка: не удалось найти реальную ссылку для скачивания.")
            return

        mods_dir = os.path.join(minecraft_directory, "mods")
        os.makedirs(mods_dir, exist_ok=True)
        filemodname = self.getJarName(mod_url) + '.jar'
        mods_dir_file = os.path.join(mods_dir, filemodname)

        try:
            response = requests.get(real_download_url)
            response.raise_for_status()
            with open(mods_dir_file, "wb") as file:
                file.write(response.content)
            self.mod_label.configure(text=f"Jar файл успешно загружен и сохранен как {mods_dir_file}")
        except requests.exceptions.RequestException as e:
            self.mod_label.configure(text=f"Ошибка при загрузке jar файла: {str(e)}")

    def list_mods(self):
        mods_dir = os.path.join(minecraft_directory, "mods")
        os.makedirs(mods_dir, exist_ok=True)
        mod_files = [f for f in os.listdir(mods_dir) if os.path.isfile(os.path.join(mods_dir, f))]
        self.mod_checkboxes = []
        for mod_file in mod_files:
            var = ctkin.BooleanVar()
            chk = ctkin.CTkCheckBox(self.available_mod_frame, text=mod_file, variable=var)
            chk.pack(anchor='w')
            self.mod_checkboxes.append((chk, var, mod_file))
    def save_mod_selections(self):
        mod_dir = os.path.join(minecraft_directory,"mods")
        mods_disabled_dir = os.path.join(minecraft_directory,"mods_disabled")
        os.makedirs(mods_disabled_dir,exist_ok=True)
        for chk,var,mod_file in self.mod_checkboxes:
            mod_path = os.path.join(mod_dir,mod_file)
            disabled_mod_path = os.path.join(mods_disabled_dir,mod_file)
            if var.get():
                if os.path.exists(disabled_mod_path):
                    shutil.move(disabled_mod_path,mod_dir)
            else:
                if os.path.exists(mod_path):
                    shutil.move(mod_path,mods_disabled_dir)

    def open_about_us_window(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = TLW_About_Us(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

        #self.about_us_label = ctkin.CTkLabel(self.toplevel_window,text="https://discord.com/invite/wrEvCM5CeR")

    def open_select_mod_window(self):
        if self.toplevel_select_mods is None or not self.toplevel_select_mods.winfo_exists():
            self.toplevel_select_mods = TLW_Select_Mods(self)  # create window if its None or destroyed
        else:
            self.toplevel_select_mods.focus()  # if window exists focus it

        #self.about_us_label = ctkin.CTkLabel(self.toplevel_window,text="https://discord.com/invite/wrEvCM5CeR")

    def update_installed_version_select(self):
        availible_version_list = [version['id'] for version in minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory)]
        self.availible_version_select.configure(values=availible_version_list)

    def widget(self):
        self.sideframe = ctkin.CTkFrame(master=self, corner_radius=10, fg_color="#141414",height=750)
        self.sideframe.pack(side=ctkin.LEFT,fill=ctkin.Y)

        self.launch_frame = ctkin.CTkFrame(self)
        self.setup_frame = ctkin.CTkFrame(self)
        self.mod_frame = ctkin.CTkFrame(self)
        self.btn_frame = ctkin.CTkFrame(self)
        self.mod_search_filters = ctkin.CTkFrame(self)
        self.available_mod_frame = ctkin.CTkScrollableFrame(self)
        #self.search_frame = ctkin.CTkFrame(self)
        #self.search_frame.pack(side=ctkin.BOTTOM)
        self.setup_frame.pack(side=ctkin.TOP)
        #-------------------------------------------------
        self.menuLabel = ctkin.CTkLabel(self.sideframe,text="MLauncher",font=("Arial",24,"bold"))
        self.menuLabel.pack(padx=10,pady=0)

        self.profile_label = ctkin.CTkLabel(self.setup_frame, text="Установка minecraft")
        self.profile_label.grid(sticky="N")
        #-------------------------------------------------
        self.showsetupbutton = ctkin.CTkButton(self.sideframe,width=20,height=30,text="Установка",command=self.show_profile)
        self.showsetupbutton.pack(padx=10,pady=20,fill=ctkin.X)
        #-------------------------------------------------
        self.launchmenubtn = ctkin.CTkButton(self.sideframe,width=20,height=30,text="Меню запуска",command=self.show_launch)
        self.launchmenubtn.pack(padx=10,pady=20,fill=ctkin.X)

        self.open_dir_btn = ctkin.CTkButton(self.sideframe,width=20,height=30,text="Minecraft Folder",command=self.open_mine_dir)
        self.open_dir_btn.pack(padx=10,pady=30,fill=ctkin.Y)

        self.modsmenubtn = ctkin.CTkButton(self.sideframe,width=20,height=30,text="Mods",command=self.show_mods)
        self.modsmenubtn.pack(padx=10,pady=30,fill=ctkin.Y)

        self.show_about_us_btn = ctkin.CTkButton(self.sideframe,width=20,height=30,text="About USA",command=self.open_about_us_window)
        self.show_about_us_btn.pack(padx=10,pady=50,fill=ctkin.Y)
        #------------------Setup Page----------------------------------
        self.version_label = ctkin.CTkLabel(self.setup_frame, text="Choose version:")
        self.version_label.grid(pady=10, sticky="W")
        self.new_version_select = ctkin.CTkOptionMenu(self.setup_frame, width=300, height=10,
                                                              values=version_list_for_install)
        self.new_version_select.grid(pady=10)

        self.checkbox_label = ctkin.CTkLabel(self.setup_frame, text="Choose version(Fabric or Forge):")
        self.checkbox_label.grid(pady=10, sticky="W")
        self.forge_var = ctkin.StringVar(value="off")
        self.forge_check = ctkin.CTkCheckBox(self.setup_frame, width=10, text="Forge", onvalue="on", offvalue="off",
                                                     variable=self.forge_var)
        self.forge_check.grid(padx=10, pady=20, sticky="w")

        self.fabric_var = ctkin.StringVar(value="off")
        self.fabric_check = ctkin.CTkCheckBox(self.setup_frame, width=10, text="Fabric", onvalue="on", offvalue="off",
                                                      variable=self.fabric_var)
        self.fabric_check.grid(sticky="W", pady=20, padx=10)

        self.quilt_var = ctkin.StringVar(value="off")
        self.quilt_check = ctkin.CTkCheckBox(self.setup_frame,width=10,text="Quilt",onvalue='on',offvalue='off',variable=self.quilt_var)
        self.quilt_check.grid(sticky="W",pady=30,padx=10)

        self.warning_label = ctkin.CTkLabel(self.setup_frame, text="After install of build release reboot launcher")
        self.warning_label.grid(sticky="W", pady=15)

        self.install_btn = ctkin.CTkButton(self.setup_frame, width=100, height=50, text="Install",
                                                   command=self.thread_install)
        self.install_btn.grid(sticky="E", pady=20, padx=10)

        self.progress_label = ctkin.CTkLabel(self.setup_frame, text="Some data")
        self.progress_label.grid(sticky="W", pady=20, padx=30)

        self.progress_bar = ctkin.CTkProgressBar(self.setup_frame, width=400, height=10)
        self.progress_bar.set(0)
        self.progress_bar.grid(sticky="W", pady=30, padx=30)
        #----------------------Launch Page ---------------------------
        # ------------Launch Tab----------------------------------------------------------------------------------------

        self.userLabel = ctkin.CTkLabel(master=self.launch_frame, text=" Enter your Username:")
        self.userLabel.grid(row=0, column=0, sticky="nw")

        self.userInput = ctkin.CTkEntry(self.launch_frame, width=500, height=10, placeholder_text="Username")
        self.userInput.grid(row=5, column=0, sticky="nw")
        self.availible_version_select = ctkin.CTkOptionMenu(self.launch_frame, width=500, height=20,
                                                                    values=availible_version_list)
        self.availible_version_select.grid(row=9, column=0, sticky="n")
        self.availible_version_select.grab_current()

        self.availible_version_select_label = ctkin.CTkLabel(self.launch_frame, text="Choose version for launch")
        self.availible_version_select_label.grid(row=7, column=0, sticky="W")

        self.update_installed_version_select_btn = ctkin.CTkButton(self.launch_frame, text="Обновить список версий",
                                                                   command=self.update_installed_version_select)
        self.update_installed_version_select_btn.grid(column=7,row=1,padx=25)

        # --------------------------------------------------------------------------------------------------------------
        self.ram_value_label = ctkin.CTkLabel(self.launch_frame, text="Объем оперативной памяти для запуска:")
        self.ram_value_label.grid(sticky="W")
        self.ram_allocation_select = ctkin.CTkSlider(self.launch_frame, width=300, from_=1, to=total_mem_gb,
                                                             command=self.sliding)

        self.ram_allocation_select.grid(row=12, column=0, sticky="W", padx=10)
        # --------------------------------------------------------------------------------------------------------------
        self.ram_allocation_select_label = ctkin.CTkLabel(self.launch_frame,
                                                                  text=f'{self.ram_allocation_select.get()}ГБ')
        self.ram_allocation_select_label.grid(sticky="E", pady=20)

        self.launch_btn = ctkin.CTkButton(self.launch_frame, width=100, height=50, text="Launch Minecraft",
                                                  command=self.launch_minecraft)
        self.launch_btn.grid(padx=50, pady=100)


        self.mods_select_btn = ctkin.CTkButton(self.launch_frame, text="Выбрать моды",command=self.open_select_mod_window)
        self.mods_select_btn.grid(column=8,row=1,padx=20)
        #---------------------------------------------------------------------------------------------------------------

        #-------------Mods Menu-----------------------------------------------------------------------------------------
        self.mod_label = ctkin.CTkLabel(self.mod_frame,text="Search Frame")
        self.mod_label.grid(sticky="N")
        #---------------------------------------------------------------------------------------------------------
        self.keyword_input = ctkin.CTkEntry(self.mod_frame,placeholder_text="Название мода ",width=600)
        self.keyword_input.grid(sticky="W")

        self.search_btn = ctkin.CTkButton(self.btn_frame,text="Найти",command=self.search_mod)
        self.search_btn.grid(sticky="W",padx=0,pady=20,column=0,row=0)

        self.mod_lst_box = CTkListbox.CTkListbox(self.mod_frame,width=600,height=300)
        self.mod_lst_box.grid(sticky="S",column=0,row=6)

        self.setup_mod_btn = ctkin.CTkButton(self.btn_frame,text="Установить",command=self.install_selected_mod)
        self.setup_mod_btn.grid(sticky="W",padx=490,pady=20,column=0,row=0)

        #TODO сделать фильтры для поиска модов по версиям
        self.filters_label = ctkin.CTkLabel(self.mod_search_filters,text="Фильтр поиска",font=("Arial",24,"bold"))
        self.filters_label.grid(column=3,row=2)
        self.version_mod_list_label = ctkin.CTkLabel(self.mod_search_filters,text="Выберите версию")
        self.version_mod_list_label.grid(column=3,row=4)
        self.version_mod_list = ctkin.CTkOptionMenu(self.mod_search_filters,width=300,corner_radius=10,values=versions_of_mods)
        self.version_mod_list.grid(column=3,row=5,sticky="E")

        self.use_filters_var = ctkin.StringVar(value="off")
        self.check_filters = ctkin.CTkCheckBox(self.mod_search_filters,width=10,text="Использовать фильтры при поиске",height=10,onvalue="on",offvalue="off",variable=self.use_filters_var)
        self.check_filters.grid(column=3,row=1)

        self.list_mods()

        #Todo Исправить загрузку поврежденных  файлов
app = MLauncher()
app.mainloop()