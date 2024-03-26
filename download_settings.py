"""
this module downloads configuraiton and saves from a retroid console via ftp.

ftp can be created by using CX file explorer or similar
"""

import os

from common import LOCAL_SAVE_DIRECTORY
import ftplib
import logging
import shutil

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# FTP Connection Details
FTP_HOST = os.environ.get("RETROID_FTP_IP", None)
FTP_PORT = int(os.environ.get("RETROID_FTP_PORT", 2821))  # Default FTP port is 21
FTP_USER = os.environ.get("RETROID_FTP_USER", None)
FTP_PASS = os.environ.get("RETROID_FTP_PASS", None)

# Paths for emulator saves and configuration files on your Android device
emulator_paths = {
    "skyline": {
        "saves": "/device/Android/data/skyline.emu/files/switch/nand/user/save",
        "config": []  # Add config paths if available
    },
    "retroarch": {
        "saves": "/device/RetroArch/saves",
        "config": [
            "/device/RetroArch/config",
            "/device/RetroArch/states",
            "/device/RetroArch/screenshots"
        ]
    },
    "ppsspp": {
        "saves": "/device/ROMs/PSP/PSP/SAVEDATA",
        "config": [
                   "/device/ROMs/PSP/PSP/SYSTEM"
                   #,"/device/ROMs/PSP/PSP/PPSSPP_STATE"
                   ]
    },
    "aethersx2": {
        "saves": "/device/Android/data/xyz.aethersx2.android/files/memcards",
        "config": ["/device/Android/data/xyz.aethersx2.android/files/inputprofiles",
                    #"/device/Android/data/xyz.aethersx2.android/files/sstates",
                   "/device/Android/data/xyz.aethersx2.android/files/gamesettings"

        ]
    },
    "dolphin": {
        "saves": "/device/Android/data/org.dolphinemu.dolphinemu/files/GC",
        "config": ["/device/Android/data/org.dolphinemu.dolphinemu/files/Config",
                   "/device/Android/data/org.dolphinemu.dolphinemu/files/GameSettings",
                   "/device/Android/data/org.dolphinemu.dolphinemu/files/StateSaves"
                   ]
    },
    "dolphin_mmjr": {
        "saves": "/device/dolphin-mmjr/GC",
        "config": ["/device/dolphin-mmjr/Config", "/device/dolphin-mmjr/GameSettings"]
    }
}

# Local save directory
local_save_directory = LOCAL_SAVE_DIRECTORY


# Function to check if a path is a directory
def is_directory(ftp, path):
    """
    Checks if a given path is a directory on the FTP server.

    Args:
        ftp: An active FTP connection object.
        path: Path on the FTP server to check.

    Returns:
        True if the path is a directory, False otherwise.
    """
    try:
        original_cwd = ftp.pwd()
        ftp.cwd(path)
        ftp.cwd(original_cwd)
        return True
    except ftplib.error_perm as e:
        # If it's not a directory, a permission error should be thrown
        logging.debug(f"Checked if '{path}' is a directory: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error when checking if '{path}' is a directory: {e}")
        return False


# Function to download a file
def download_file(ftp, remote_path, local_path):
    """
    Downloads a single file from the FTP server.

    Args:
        ftp: An active FTP connection object.
        remote_path: The path of the file on the FTP server.
        local_path: The local path where the file will be saved.
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        logging.debug(f"Downloading file {remote_path} to {local_path}")
        with open(local_path, 'wb') as f:
            ftp.retrbinary('RETR ' + remote_path, f.write)
    except Exception as e:
        logging.error(f"Error downloading file '{remote_path}': {e}")

# Function to download a directory
def download_directory(ftp, remote_path, local_path):
    """
    Recursively downloads a directory from the FTP server.

    Args:
        ftp: An active FTP connection object.
        remote_path: The path of the directory on the FTP server.
        local_path: The local path where the directory will be saved.
    """
    try:
        items = ftp.nlst(remote_path)
        for item in items:
            remote_item_path = os.path.join(remote_path, item)
            # Replace '%20' with spaces for local path
            local_item_name = os.path.basename(item).replace('%20', ' ')
            local_item_path = os.path.join(local_path, local_item_name)

            if is_directory(ftp, remote_item_path):
                logging.debug(f"Downloading directory {remote_item_path} to {local_item_path}")
                if not os.path.exists(local_item_path):
                    os.makedirs(local_item_path, exist_ok=True)
                download_directory(ftp, remote_item_path, local_item_path)
            else:
                download_file(ftp, remote_item_path, local_item_path)
    except ftplib.error_perm as e:
        logging.error(f"FTP error for path '{remote_path}': {e}")
    except Exception as e:
        logging.error(f"Error downloading from '{remote_path}': {e}")

# Main execution
def download_settings():
    try:
        # Delete and recreate the entire local save directory
        shutil.rmtree(local_save_directory, ignore_errors=True)
        os.makedirs(local_save_directory, exist_ok=True)

        with ftplib.FTP() as ftp:
            ftp.connect(FTP_HOST, FTP_PORT)
            ftp.login(FTP_USER, FTP_PASS)
            # Set debug level for FTP to get more detailed logs
            # ftp.set_debuglevel(2)
            for emulator, paths in emulator_paths.items():
                logging.info(f"Downloading saves and configuration for {emulator}...")

                # Download saves
                saves_path = paths.get('saves')
                if saves_path:
                    local_saves_path = os.path.join(local_save_directory, emulator, 'saves')
                    os.makedirs(local_saves_path, exist_ok=True)
                    if is_directory(ftp, saves_path):
                        download_directory(ftp, saves_path, local_saves_path)
                    else:
                        download_file(ftp, saves_path, local_saves_path)

                # Download configs
                config_paths = paths.get('config', [])
                for config_path in config_paths:
                    local_config_path = os.path.join(local_save_directory, emulator, 'config',
                                                     os.path.basename(config_path))
                    os.makedirs(os.path.dirname(local_config_path), exist_ok=True)
                    if is_directory(ftp, config_path):
                        download_directory(ftp, config_path, local_config_path)
                    else:
                        download_file(ftp, config_path, local_config_path)

                logging.info(f"Saves and configuration for {emulator} downloaded.")

        logging.info("All saves and configurations downloaded successfully.")
    except Exception as e:
        logging.error("An error occurred:", exc_info=True)

if __name__=="__main__":
    download_settings()