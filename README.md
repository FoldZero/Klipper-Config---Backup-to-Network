# Klipper-Config---Backup-to-Network
Klipper Backup to Network
# Klipper Backup Setup Instructions

## Prerequisites
- Klipper installed and configured
- Root access to your Klipper host system
- Network access to your NAS

## Installation

1. Download the install script to your Klipper host system.
2. Make the script executable:
   ```
   chmod +x install_klipper_backup.sh
   ```
3. Run the script as root:
   ```
   sudo ./install_klipper_backup.sh
   ```

## Configuration

1. Edit the backup script:
   ```
   sudo nano /home/sovol/klipper_backup/backup_script.py
   ```
2. Modify the following variables with your NAS details:
   - NAS_IP
   - NAS_SHARE
   - NAS_USER
   - NAS_PASS

## Setting up the Klipper Macro

1. Edit your Klipper config file:
   ```
   nano /home/sovol/printer_data/config/printer.cfg
   ```
2. Add the following macro:
   ```
   [gcode_macro BACKUP_KLIPPER_CONFIG]
   gcode:
       RUN_SHELL_COMMAND CMD=run_backup_script

   [gcode_shell_command run_backup_script]
   command: python3 /home/sovol/klipper_backup/backup_script.py
   timeout: 600.0
   verbose: True
   ```
3. Save the file and restart Klipper.

## Usage

To run a backup, use the following command in your printer interface:
```
BACKUP_KLIPPER_CONFIG
```

## Troubleshooting

- Check the log file at `/home/sovol/klipper_backup/backup.log` for any error messages.
- Ensure your NAS is accessible and the share path is correct.
- Verify that the user has the necessary permissions to mount the NAS share.
