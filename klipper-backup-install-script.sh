#!/bin/bash

# Variables (modify these as needed)
BACKUP_USER="sovol"
BACKUP_GROUP="sovol"
KLIPPER_CONFIG_DIR="/home/$BACKUP_USER/printer_data"
BACKUP_SCRIPT_DIR="/home/$BACKUP_USER/klipper_backup"
BACKUP_SCRIPT_NAME="backup_script.py"
BACKUP_LOG_NAME="backup.log"
NAS_MOUNT_POINT="/mnt/nas_backup"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    echo -e "${1}${2}${NC}"
}

# Check if script is run as root
if [ "$EUID" -ne 0 ]; then
    print_color $RED "Please run as root"
    exit 1
fi

# Install required packages
print_color $GREEN "Installing required packages..."
apt-get update
apt-get install -y cifs-utils rsync python3

# Create necessary directories
print_color $GREEN "Creating necessary directories..."
mkdir -p $BACKUP_SCRIPT_DIR
mkdir -p $NAS_MOUNT_POINT

# Set correct permissions
chown $BACKUP_USER:$BACKUP_GROUP $BACKUP_SCRIPT_DIR
chown $BACKUP_USER:$BACKUP_GROUP $NAS_MOUNT_POINT

# Create the backup script
print_color $GREEN "Creating the backup script..."
cat << EOF > $BACKUP_SCRIPT_DIR/$BACKUP_SCRIPT_NAME
#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(filename='$BACKUP_SCRIPT_DIR/$BACKUP_LOG_NAME', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Variables (modify these as needed)
SOURCE = "$KLIPPER_CONFIG_DIR"
DEST = "$BACKUP_SCRIPT_DIR"
NAS_IP = "YOUR_NAS_IP"
NAS_SHARE = f"//{NAS_IP}/YOUR_SHARE_PATH"
NAS_USER = "YOUR_NAS_USERNAME"
NAS_PASS = "YOUR_NAS_PASSWORD"
MOUNT_POINT = "$NAS_MOUNT_POINT"

# ... (rest of the Python script goes here)

if __name__ == "__main__":
    backup_klipper_config()
EOF

# Set correct permissions for the backup script
chown $BACKUP_USER:$BACKUP_GROUP $BACKUP_SCRIPT_DIR/$BACKUP_SCRIPT_NAME
chmod +x $BACKUP_SCRIPT_DIR/$BACKUP_SCRIPT_NAME

# Add user to sudoers for mount commands
print_color $GREEN "Adding user to sudoers for mount commands..."
echo "$BACKUP_USER ALL=(ALL) NOPASSWD: /bin/mount, /bin/umount" | tee /etc/sudoers.d/klipper_backup

print_color $GREEN "Installation complete! Please edit $BACKUP_SCRIPT_DIR/$BACKUP_SCRIPT_NAME to set your NAS details."
print_color $GREEN "Refer to the instructions document for setting up the Klipper macro."
