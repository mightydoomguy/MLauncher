import logging
import subprocess
import uuid

import dearpygui.dearpygui as dpg
import minecraft_launcher_lib.command
import psutil

from MLauncherDPGUI.install_minecraft.install_mine_window import InstallWindow
from vars import *
dpg.create_context()
max_ram = psutil.virtual_memory().total
total_mem_gb = round(max_ram / (1024 ** 3))
class MyApp:

    def __init__(self):
        dpg.create_viewport(title="SomeTitle", width=600, height=400)
        self.setup()

    def print_value(self):
        ram = dpg.get_value(self.ram_slider)
        print(ram)
    def init_Install_Window(self):
            InstallWindow()
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
    def setup(self):
        with dpg.window(label="Primary Window", tag="primary_window"):
           self.label =  dpg.add_text("Hello, world!")
           self.nickname = dpg.add_input_text(hint="Enter username")
           self.installed_version = dpg.add_combo(items=availible_version_list)
           self.ram_slider = dpg.add_slider_int(min_value=0,max_value=total_mem_gb)
           dpg.add_button(label="Click me",callback=self.launch_minecraft)

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