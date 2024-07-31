#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime
import logging

# Variables (modify these as needed)
SOURCE = "/home/sovol/printer_data"
DEST = "/home/sovol/klipper_backup"
NAS_IP = "YOUR_NAS_IP"
NAS_SHARE = f"//{NAS_IP}/YOUR_SHARE_PATH"
NAS_USER = "YOUR_NAS_USERNAME"
NAS_PASS = "YOUR_NAS_PASSWORD"
MOUNT_POINT = "/mnt/nas_backup"
LOG_FILE = "/home/sovol/klipper_backup/backup.log"
BACKUP_RETENTION_DAYS = 7

# Set up logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def run_command(command):
    """Execute a shell command and log the output"""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        logging.info(f"Command executed successfully: {command}")
        logging.debug(f"Command output: {result.stdout}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {command}")
        logging.error(f"Error output: {e.stderr}")
        raise

def is_nas_mounted():
    """Check if the NAS is already mounted"""
    try:
        with open('/proc/mounts', 'r') as f:
            if any(MOUNT_POINT in line for line in f):
                return True
    except IOError:
        logging.error("Failed to read /proc/mounts")
    return False

def mount_nas():
    """Mount the NAS if it's not already mounted"""
    if not is_nas_mounted():
        try:
            mount_command = f"sudo mount -t cifs -o username={NAS_USER},password={NAS_PASS},uid=$(id -u),gid=$(id -g),file_mode=0777,dir_mode=0777 {NAS_SHARE} {MOUNT_POINT}"
            run_command(mount_command)
            logging.info("NAS share mounted successfully")
        except Exception as e:
            logging.error(f"Failed to mount NAS: {str(e)}")
            raise
    else:
        logging.info("NAS is already mounted")

def backup_klipper_config():
    try:
        # Create timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        logging.info(f"Starting backup process with timestamp: {timestamp}")

        # Create local backup
        local_backup_path = os.path.join(DEST, f"backup_{timestamp}")
        run_command(f"rsync -avz --delete {SOURCE}/ {local_backup_path}")
        logging.info(f"Local backup created at: {local_backup_path}")

        # Mount NAS share (if not already mounted)
        mount_nas()

        # Copy to NAS
        nas_backup_path = os.path.join(MOUNT_POINT, f"backup_{timestamp}")
        rsync_command = (
            f"rsync -avz --delete "
            f"--exclude='*.sock' "
            f"--exclude='*.serial' "
            f"--copy-links "
            f"{local_backup_path}/ {nas_backup_path}"
        )
        run_command(rsync_command)
        logging.info(f"Backup copied to NAS: {nas_backup_path}")

        # Clean up local backups older than BACKUP_RETENTION_DAYS
        run_command(f"find {DEST} -type d -mtime +{BACKUP_RETENTION_DAYS} -exec rm -rf {{}} +")
        logging.info(f"Local backups older than {BACKUP_RETENTION_DAYS} days cleaned up")

        logging.info("Backup completed successfully!")
        print("Backup completed successfully!")

    except Exception as e:
        logging.error(f"Backup failed: {str(e)}")
        print(f"Backup failed. Check the log file for details.")

if __name__ == "__main__":
    backup_klipper_config()
