"""
this module uploads backed up retroid console data to an ftp site for archive
"""

import os
import paramiko
import shutil
import logging
from datetime import datetime
from common import LOCAL_SAVE_DIRECTORY
# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Local save directory (this should be the same directory where your files are saved locally)
local_save_directory = LOCAL_SAVE_DIRECTORY  # Update this path


# Create a timestamped directory name for the archive
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
archive_directory = f"/Games/EmulatorSettingsBackup/Retroid-{timestamp}"  # Update the base path

# SFTP Connection Details
SFTP_HOST = os.environ.get("RETROID_BACKUP_SFTP_IP", None)
SFTP_PORT = int(os.environ.get("RETROID_BACKUP_SFTP_PORT", 22))  # Default SFTP port is 22
SFTP_USER = os.environ.get("RETROID_BACKUP_SFTP_USER", None)
SFTP_PASS = os.environ.get("RETROID_BACKUP_SFTP_PASS", None)

print(f"password:'{SFTP_PASS}'")

# Function to recursively copy directory to SFTP
def sftp_put_dir(sftp, local_path, remote_path):
    for item in os.listdir(local_path):
        local_item_path = os.path.join(local_path, item)
        remote_item_path = os.path.join(remote_path, item)

        if os.path.isdir(local_item_path):
            # Create remote directory
            try:
                sftp.mkdir(remote_item_path)
            except IOError:
                # Directory already exists
                pass
            sftp_put_dir(sftp, local_item_path, remote_item_path)
        else:
            sftp.put(local_item_path, remote_item_path)


# Connect to SFTP and copy directory
def upload_settings():
    try:
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USER, password=SFTP_PASS)

        sftp = paramiko.SFTPClient.from_transport(transport)

        # Create remote archive directory
        try:
            sftp.mkdir(archive_directory)
        except IOError as e:
            # Handle error if directory creation fails
            logging.error(f"Failed to create remote directory: {archive_directory}. Error: {e}")

        # Copy local directory to remote archive
        sftp_put_dir(sftp, local_save_directory, archive_directory)

        sftp.close()
        transport.close()
        logging.info("Backup to SFTP completed successfully.")
    except Exception as e:
        logging.error(f"Error in SFTP backup: {e}")

if __name__=="__main__":
    upload_settings()
