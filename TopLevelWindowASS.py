import os
import shutil
import subprocess
from vars import minecraft_directory
import customtkinter
import webbrowser as wb
class TLW_About_Us(customtkinter.CTkToplevel):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.geometry("300x300")
        self.title("About Us")
        self.label = customtkinter.CTkLabel(self,text="Информация о нас:\n Контора пидорасов")
        self.label.pack(padx=20,pady=20)

        self.discord_btn = customtkinter.CTkButton(self,width=20,height=50,text="Discord",command=self.open_discord_server)
        self.discord_btn.pack(anchor="s")


    def open_discord_server(self):
        discord_path = os.path.join(os.getenv('LOCALAPPDATA'),"Discord","Update.exe")
        link = "https://discord.com/invite/wrEvCM5CeR"
        if os.path.exists(discord_path):
            print("This path working")
            subprocess.run([discord_path,"--processStart",'Discord.exe','--url',link])
        else:
            wb.open_new_tab()

class TLW_Select_Mods(customtkinter.CTkToplevel):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.geometry("300x300")
        self.label_SM = customtkinter.CTkLabel(self,text="Включенные моды")
        self.label_SM.pack(anchor="nw",padx=20,pady=20)
        self.list_mods()
        self.save_btn_mods()
        self.dis_list_mods()

    def list_mods(self):
        self.en_msl_frame = customtkinter.CTkScrollableFrame(self)
        self.en_msl_frame.pack(side='left')



        mods_dir = os.path.join(minecraft_directory, "mods")
        dis_mods = os.path.join(minecraft_directory,"mods_disabled")
        os.makedirs(mods_dir, exist_ok=True)
        mod_files = [f for f in os.listdir(mods_dir) if os.path.isfile(os.path.join(mods_dir, f))]
        dis_mod_files = [f for f in os.listdir(dis_mods) if os.path.isfile(os.path.join(dis_mods, f))]
        mod_files.extend(dis_mod_files)
        self.mod_checkboxes = []
        for mod_file in mod_files:
            var = customtkinter.BooleanVar()
            chk = customtkinter.CTkCheckBox(self.en_msl_frame, text=mod_file, variable=var)
            chk.pack(anchor='w')
            self.mod_checkboxes.append((chk, var, mod_file))

    def dis_list_mods(self):
        self.dis_msl_frame = customtkinter.CTkScrollableFrame(self)
        self.dis_msl_frame.pack(side="right")
        self.dis_mods_label = customtkinter.CTkLabel(self,text="Выключенные моды")
        self.dis_mods_label.pack(anchor="ne",padx=20,pady=20)
        dis_mods = os.path.join(minecraft_directory, "mods_disabled")
        os.makedirs(dis_mods,exist_ok=True)
        dis_mod_files = [f for f in os.listdir(dis_mods) if os.path.isfile(os.path.join(dis_mods, f))]
        self.mod_checkboxes = []
        for mod_file in dis_mod_files:
            var = customtkinter.BooleanVar()
            chk = customtkinter.CTkCheckBox(self.dis_msl_frame, text=mod_file, variable=var)
            chk.pack(anchor='w', padx=50,pady=40)
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

    def save_btn_mods(self):
        self.save_btn = customtkinter.CTkButton(self,width=20,height=20,text="Save Mods",command=self.save_mod_selections)
        self.save_btn.pack(anchor="s")