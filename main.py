#---------------------------------
import subprocess
import threading
import uuid
import customtkinter
from vars import *
import psutil
#---------------------------------------------------
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
max_ram = psutil.virtual_memory().total
total_mem_gb = round(max_ram / (1024 ** 3))
class MyApp(customtkinter.CTk):
    def __init__(self):
        super(MyApp,self).__init__()
        self.title("MyLauncher")
        self.geometry("600x650")
        self.iconbitmap(bitmap="rocket.ico")
        self.resizable(True,True)
        self.widget()
        self.grid()
        self.load_config_values()
        self.ram_value = cfg_data['user_ram']
    def load_config_values(self):
        # Загрузка значений из config.ini
        self.cfg_data = Config['DEFAULT']
        username = self.cfg_data.get('nickname', '')  # Получение никнейма из конфигурации
        user_ram = self.cfg_data.get('user_ram')  # Получение объема памяти из конфигурации

        self.userInput.insert(0,username)
        self.ram_allocation_select_label.configure(text=user_ram)
        self.ram_allocation_select.set(int(user_ram))
    def launch_minecraft(self):
        uid = str(uuid.uuid1())
        username = self.userInput.get()
        ram_value = self.ram_value
        if  username != self.cfg_data['nickname'] or ram_value != self.cfg_data['user_ram']:
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

        subprocess.call(
            minecraft_launcher_lib.command.get_minecraft_command(version=self.availible_version_select.get(),
                                                                 minecraft_directory=minecraft_directory,
                                                                 options=options))
    def install_minecraft(self):
        self.vanilla_version = self.new_version_select.get()
        if self.forge_var.get() == "on":
            self.forge_version = minecraft_launcher_lib.forge.find_forge_version(self.vanilla_version)

            callback = {
                "setStatus": lambda text:self.progress_label.configure(text=text),
                "setProgress": lambda int: self.progress_bar.set(int)

            }
            minecraft_launcher_lib.forge.install_forge_version(self.forge_version,minecraft_directory,callback=callback)
        elif self.fabric_var.get() == "on":
            callback = {
                "setStatus": lambda text: self.progress_label.configure(text=text),
                "setProgress" :lambda int:self.progress_bar.set(int)}
            minecraft_launcher_lib.fabric.install_fabric(self.vanilla_version,minecraft_directory,callback=callback)

        elif self.forge_var.get() == "off" and self.fabric_var.get()=="off":
            callback = {
                "setStatus": lambda text: self.progress_label.configure(text=text),
                "setProgress" :lambda int:self.progress_bar.set(int)}
            minecraft_launcher_lib.install.install_minecraft_version(self.vanilla_version,minecraft_directory,callback=callback)

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
    def widget(self):
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.pack(pady=5)
        self.launch_tab = self.tabview.add("Launch")

        #self.sideframe = customtkinter.CTkFrame(self, corner_radius=10, fg_color="#141414")
        #self.sideframe.pack(side=customtkinter.LEFT, fill=customtkinter.Y)

        #------------Launch Tab-----------------------------------------------------------------------------------------

        self.userLabel = customtkinter.CTkLabel(master=self.launch_tab,text=" Enter your Username:")
        self.userLabel.grid(row=0,column=0,sticky="nw")

        self.userInput = customtkinter.CTkEntry(self.launch_tab,width=500,height=10,placeholder_text="Username")
        self.userInput.grid(row=5,column=0,sticky="nw")
        self.availible_version_select = customtkinter.CTkOptionMenu(self.launch_tab,width=500,height=20,values=availible_version_list)
        self.availible_version_select.grid(row=9,column=0,sticky="n")
        self.availible_version_select.grab_current()

        self.availible_version_select_label = customtkinter.CTkLabel(self.launch_tab, text="Choose version for launch")
        self.availible_version_select_label.grid(row=7, column=0,sticky="W")
        #---------------------------------------------------------------------------------------------------------------

        self.ram_value_label = customtkinter.CTkLabel(self.launch_tab,text="Объем оперативной памяти для запуска:")
        self.ram_value_label.grid(sticky="W")
        self.ram_allocation_select = customtkinter.CTkSlider(self.launch_tab,width=300,from_= 1,to=total_mem_gb,command=self.sliding)
    
        self.ram_allocation_select.grid(row=12, column=0, sticky="W", padx=10)
        #---------------------------------------------------------------------------------------------------------------
        self.ram_allocation_select_label = customtkinter.CTkLabel(self.launch_tab,text=f'{self.ram_allocation_select.get()}ГБ')
        self.ram_allocation_select_label.grid(sticky="E",pady=20)

        self.launch_btn = customtkinter.CTkButton(self.launch_tab,width=100,height=50,text="Launch Minecraft",command=self.launch_minecraft)
        self.launch_btn.grid(padx=50,pady=100)

        #------------Install Tab----------------------------------------------------------------------------------------
        self.tab2 = self.tabview.add("Install")

        self.version_label = customtkinter.CTkLabel(self.tab2,text="Choose version:")
        self.version_label.grid(pady=10,sticky="W")
        self.new_version_select = customtkinter.CTkOptionMenu(self.tab2,width=300,height=10,values=version_list_for_install)
        self.new_version_select.grid(pady=10)

        self.checkbox_label = customtkinter.CTkLabel(self.tab2,text="Choose version(Fabric or Forge):")
        self.checkbox_label.grid(pady=10,sticky="W")
        self.forge_var = customtkinter.StringVar(value="off")
        self.forge_check = customtkinter.CTkCheckBox(self.tab2,width=10,text="Forge",onvalue="on",offvalue="off",variable=self.forge_var)
        self.forge_check.grid(padx=10,pady=20,sticky="w")

        self.fabric_var = customtkinter.StringVar(value="off")
        self.fabric_check = customtkinter.CTkCheckBox(self.tab2,width=10,text="Fabric",onvalue="on",offvalue="off",variable=self.fabric_var)
        self.fabric_check.grid(sticky = "W",pady=20,padx=10)

        self.warning_label = customtkinter.CTkLabel(self.tab2,text="After install of build release reboot launcher")
        self.warning_label.grid(sticky="W",pady=15)



        self.install_btn = customtkinter.CTkButton(self.tab2,width=100,height=50,text="Install",command=self.thread_install)
        self.install_btn.grid(sticky="E",pady=20,padx=10)

        self.progress_label = customtkinter.CTkLabel(self.tab2,text="Some data")
        self.progress_label.grid(sticky="W",pady=20,padx=30)

        self.progress_bar = customtkinter.CTkProgressBar(self.tab2,width=400,height=10)
        self.progress_bar.set(0)
        self.progress_bar.grid(sticky="W",pady=30,padx=30)
        #---------------------------------------------------------------------------------------------------------------
        self.open_dir_btn = customtkinter.CTkButton(self.launch_tab,width=100,height=50,text="open Minecraft Folder",command=self.open_mine_dir)
        self.open_dir_btn.grid(sticky="SW",padx=10,pady=10)
if __name__ == "__main__":
    app = MyApp()
    app.mainloop()