import dearpygui.dearpygui as dpg
from vars import *
class InstallWindow:
    def __init__(self):
        self.install_window()

    def install_minecraft(self):
        self.version_vanilla = dpg.get_value(self.version_for_install)
        if self.vanilla_check == True:
            callback = {
                    "setStatus":lambda text:dpg.set_value(self.progress_label,text)}
            minecraft_launcher_lib.install.install_minecraft_version(versionid=self.version_vanilla,
                                                                         minecraft_directory=minecraft_directory,callback=callback)
        elif self.forge_check == True:
            self.forge_version = minecraft_launcher_lib.forge.find_forge_version(self.version_vanilla)
            callback = {
                "setStatus": lambda text: dpg.set_value(self.progress_label, text)
            }
            minecraft_launcher_lib.forge.install_forge_version(versionid=self.forge_version,
                                                               minecraft_directory=minecraft_directory,callback=callback)
        elif self.fabric_check == True:
            callback = {
                "setStatus": lambda text: dpg.set_value(self.progress_label, text)
            }
            minecraft_launcher_lib.fabric.install_fabric(self.version_vanilla,minecraft_directory=minecraft_directory,callback=callback)
        elif self.quilt_check == True:
            callback = {
                "setStatus": lambda text: dpg.set_value(self.progress_label, text)
            }
            minecraft_launcher_lib.quilt.install_quilt(self.version_vanilla,minecraft_directory=minecraft_directory,callback=callback)

    def install_window(self):
        with dpg.window(label="Install Minecraft",width=600,height=600):
            dpg.add_text("Choose version for install")
            self.version_for_install = dpg.add_combo(items=version_list_for_install)
            self.forge_check = dpg.add_checkbox(label="Forge")
            self.fabric_check = dpg.add_checkbox(label="Fabric")
            self.vanilla_check = dpg.add_checkbox(label="vanilla",default_value=True)
            self.quilt_check = dpg.add_checkbox(label="Quilt")

            self.progress_label = dpg.add_text("Some Data")

            dpg.add_button(label="Install",callback=self.install_minecraft)