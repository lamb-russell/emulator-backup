import logging
from datetime import datetime
import ftplib
import paramiko
import shutil
import os

# Import common configuration
from common import LOCAL_SAVE_DIRECTORY

# Import from download_settings.py
from download_settings import download_settings

# Import from upload_settings_to_backup.py
from upload_settings_to_backup import upload_settings

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    download_settings()
    upload_settings()


if __name__ == "__main__":
    main()
