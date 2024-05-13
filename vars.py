from configparser import ConfigParser
import os

import minecraft_launcher_lib

minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace("minecraft","myLauncher")
availible_version_list  = [version['id'] for version in minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory)]
version_list_for_install = [install_versions['id'] for install_versions in minecraft_launcher_lib.utils.get_version_list()]

Config = ConfigParser()
if os.path.exists("config.ini"):
        print("File found")
        Config.read("config.ini")
        cfg_data = Config["DEFAULT"]
else:
     print("File not found")
     print("Creating file")
     Config["DEFAULT"] = {
            "nickname": "Your nickname",
            "uid": '1',
            "user_ram": "2"
        }
     with open("config.ini", "w") as f:
            Config.write(f)


