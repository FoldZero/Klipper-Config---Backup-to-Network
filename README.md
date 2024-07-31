# Klipper-Config---Backup-to-Network

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

#Install Steps - Broken Down
# Klipper Backup Install Script Overview

The install script performs the following actions:

1. Package Installation:
   - Updates package lists
   - Installs required packages:
     * cifs-utils (for mounting CIFS/SMB shares)
     * rsync (for efficient file transfers)
     * python3 (for running the backup script)

2. Directory Creation:
   - Creates the backup script directory:
     `/home/sovol/klipper_backup`
   - Creates the NAS mount point:
     `/mnt/nas_backup`

3. Permission Setting:
   - Sets ownership of the backup script directory to the specified user and group (sovol:sovol)
   - Sets ownership of the NAS mount point to the specified user and group (sovol:sovol)

4. Backup Script Creation:
   - Creates the main backup script:
     `/home/sovol/klipper_backup/backup_script.py`
   - Sets the correct permissions for the backup script (executable by the owner)

5. Sudoers Configuration:
   - Adds a sudoers entry to allow the specified user (sovol) to run mount and umount commands without a password

6. File Creation:
   - Creates a log file for the backup process:
     `/home/sovol/klipper_backup/backup.log`

7. Script Content:
   The backup script (`backup_script.py`) is created with the following main components:
   - Import statements for required Python modules
   - Variable definitions for customizable settings (e.g., paths, NAS details)
   - Logging configuration
   - Functions for:
     * Running shell commands
     * Checking if the NAS is mounted
     * Mounting the NAS
     * Performing the backup process
   - Main execution block

8. Not Created But Referenced:
   - The script assumes the existence of the Klipper configuration directory:
     `/home/sovol/printer_data`

9. User Action Required:
   - After installation, the user needs to edit the backup script to set their specific NAS details (IP, share path, username, password)

10. Klipper Macro (Manual Setup Required):
    - The install script doesn't create the Klipper macro
    - Instructions are provided for manually adding the macro to the Klipper configuration file


