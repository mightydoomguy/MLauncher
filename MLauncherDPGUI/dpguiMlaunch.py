import logging
import subprocess
import uuid

import dearpygui.dearpygui as dpg
import minecraft_launcher_lib.command
import psutil
from  MLauncherDPGUI.About_as.about_as_window import About_ASS_Window
from MLauncherDPGUI.install_minecraft.install_mine_window import InstallWindow
from MLauncherDPGUI.mod_window.mod_mine_window import ModDownloaderApp
from vars import *
dpg.create_context()
max_ram = psutil.virtual_memory().total
total_mem_gb = round(max_ram / (1024 ** 3))
class MyApp:
    def __init__(self):
        dpg.create_viewport(title="Dlauncher", width=600, height=400)
        self.setup()


    def print_value(self):
        ram = dpg.get_value(self.ram_slider)
        print(ram)
    def init_Install_Window(self):
            InstallWindow()
    def init_About_Ass(self):
        About_ASS_Window()
    def init_search_mods(self):
        ModDownloaderApp.runMOD(self)
    def launch_minecraft(self):
        uid = str(uuid.uuid1())
        username = dpg.get_value(self.nickname)
        ram_value = dpg.get_value(self.ram_slider)

        options = {
            "username":username,
            "uuid":uid,
            "token":" ",
            "jvmArguments": [f"-Xmx{ram_value}G"]
        }
        subprocess.Popen(minecraft_launcher_lib.command.get_minecraft_command(version=dpg.get_value(self.installed_version),minecraft_directory=minecraft_directory,options=options))

    def open_mine_dir(self):
        subprocess.call(f'explorer.exe {minecraft_directory}')
    def setup(self):
        with dpg.window(label="Primary Window", tag="primary_window"):
           self.label =  dpg.add_text("Hello, world!",pos=(160,20))
           self.nickname = dpg.add_input_text(hint="Enter username",pos=(160,40))
           self.installed_version = dpg.add_combo(items=availible_version_list,pos=(160,60))
           self.ram_slider = dpg.add_slider_int(min_value=0,max_value=total_mem_gb,pos=(160,80))
           dpg.add_button(label="Click me",callback=self.launch_minecraft,pos=(160,100))

           with dpg.child_window(width=150,pos=(0,10), autosize_y=True):
               with dpg.group(horizontal=False,horizontal_spacing=0):
                   with dpg.tree_node(selectable=True,label="Menu",pos=(0,20)):
                       dpg.add_text("Menu")
                       dpg.add_button(label="Install Minecraft",callback=self.init_Install_Window)
                       dpg.add_button(label="About Ass",callback=self.init_About_Ass)
                       dpg.add_button(label="Minecraft Folder",callback=self.open_mine_dir)
                       dpg.add_button(label="Mods",callback=self.init_search_mods)


           with dpg.menu_bar():
               with dpg.menu(label="Install"):
                   dpg.add_menu_item(label="install minecraft",callback=self.init_Install_Window)

            # Создание второго окна
        with dpg.window(label="Secondary Window", tag="secondary_window", pos=(350, 100)):
            dpg.add_text("This is the second window")
            dpg.add_button(label="Press me")

        # Установите primary_window в качестве основного окна
        dpg.set_primary_window("primary_window", True)

    def run(self):
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

if __name__ == '__main__':
    app = MyApp()
    app.run()