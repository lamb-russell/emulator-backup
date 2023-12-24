

# Emulator Backup Tool

This repository contains a Python script for downloading emulator saves and configuration files from an FTP server. It's designed to facilitate the backup of emulator data from an Android device.

## Features

- **FTP Download**: Securely connects to an FTP server to access and download files.
- **Supports Multiple Emulators**: Customizable for various emulators like Skyline, RetroArch, PPSSPP, AetherSX2, Dolphin, and Dolphin MMJR.
- **Directory & File Handling**: Recursively downloads directories and handles individual files, including those with spaces in their names.
- **Logging**: Detailed logging for easy tracking and debugging.

## Getting Started

### Prerequisites

- Python 3
- Access to an FTP server where emulator data is stored.
- an Android emulator device with a running FTP server for file transfer (e.g. CX File Explorer)


### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/emulator-backup-tool.git
   cd emulator-backup-tool
   ```

2. **Environment Setup**

   Set up the necessary FTP connection details as environment variables or directly in the script:

   - `RETROID_FTP_IP`: FTP Server IP
   - `RETROID_FTP_PORT`: FTP Server Port (default is 21)
   - `RETROID_FTP_USER`: FTP Username
   - `RETROID_FTP_PASS`: FTP Password

   These can be set in your environment, or you can directly edit the script to include these details.

3. **Customize Emulator Paths**

   Edit `emulator_paths` in the script to match the paths of your emulator saves and configuration files on your FTP server.

### Usage

Run the script using Python:

```bash
python emulator_backup.py
```

The script will connect to the FTP server, navigate through the specified emulator directories, and download the saves and configuration files to the local machine.

## Customization

You can customize the script by modifying the `emulator_paths` dictionary. Add or remove emulator sections as needed, ensuring the paths match those on your FTP server.

## Contributing

Contributions to improve the script or add new features are welcome. Please feel free to fork the repository and submit pull requests.

## Acknowledgments

- This script was created to assist gamers in backing up their emulator data efficiently.
