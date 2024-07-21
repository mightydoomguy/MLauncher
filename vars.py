from configparser import ConfigParser
import os
import minecraft_launcher_lib
link_template = 'https://minecraft-inside.ru/'

minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace("minecraft","myLauncher")
availible_version_list  = [version['id'] for version in minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory)]
version_list_for_install = [install_versions['id'] for install_versions in minecraft_launcher_lib.utils.get_version_list()]

versions_of_mods = ["1.20.6-forge","1.20.6-fabric","1.20.6","1.20.5-neoforge",
                    "1.20.5-fabric","1.20.5","1.20.4","1.20.4-forge",
                    "1.20.4-neoforge","1.20.4-fabric","1.20.4-quilt",
                    "1.20.3","1.20.3-forge","1.20.3-neoforge","1.20.3-fabric","1.20.3-quilt",
                    "1.20.2",
                    "1.20.2-forge","1.20.2-neoforge","1.20.2-fabric","1.20.2-quilt","1.20.1",
                    "1.20.1-forge","1.20.1-fabric","1.20.1-quilt","1.20",
                    "1.20-forge","1.20-fabric","1.20-quilt",
                    "1.19.4","1.19.4-forge","1.19.4-fabric","1.19.4-quilt",
                    "1.19.3","1.19.3-forge","1.19.3-fabric","1.19.3-quilt",
                    "1.19.2","1.19.2-forge","1.19.2-fabric","1.19.2-quilt",
                    "1.19.1","1.19.1-forge","1.19.1-fabric",
                    "1.19","1.19-forge","1.19-fabric",
                    "1.18.2","1.18.2-forge","1.18.2-fabric",
                    "1.18.1","1.18.1-forge","1.18.1-fabric",
                    "1.18","1.18-forge","1.18-fabric",
                    "1.17.1","1.17.1-forge","1.17.1-fabric",
                    "1.17",
                    "1.16.5","1.16.5-forge","1.16.5-fabric",
                    "1.16.4","1.16.4-forge","1.16.4-fabric",
                    "1.16.3","1.16.3-forge","1.16.3-fabric",
                    "1.16.2","1.16.2-forge","1.16.2-fabric",
                    "1.16.1","1.16.1-forge","1.16.1-fabric",
                    "1.16",
                    "1.15.2","1.15.2-forge","1.15.2-fabric",
                    "1.15.1","1.15.1-forge","1.15.1-fabric",
                    "1.15",
                    "1.14.4","1.14.4-forge","1.14.4-fabric",
                    "1.14.3","1.14.3-forge","1.14.3-fabric",
                    "1.14.2","1.14.2-forge","1.14.2-fabric",
                    "1.14.1","1.14.1-forge","1.14.1-fabric",
                    "1.14","1.14-forge","1.14-fabric",
                    "1.13.2",
                    "1.13.1",
                    "1.13",
                    "1.12.2",
                    "1.12.1",
                    "1.12",
                    "1.11.2",
                    "1.11",
                    "1.10.2",
                    "1.10",
                    "1.9.4",
                    "1.9",
                    "1.8.9",
                    "1.8",
                    "1.7.10",
                    "1.7.2",
                    "1.6.4",
                    "1.6.2",
                    "1.5.2"
                    ]
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


