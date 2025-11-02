#!/usr/bin/env bash

# --- DEPENDENCIES: Install these packages on Arch/Omarchy if missing: ---
# For Xwayland authorization:
#   sudo pacman -S xorg-xauth xorg-xhost
# For PyAutoGUI (MouseInfo) GUI support:
#   sudo pacman -S tk

# --- Xwayland Authorization Fix (Required for PyAutoGUI/Xlib in Hyprland) ---

# 1. Set a temporary, writeable file location for XAUTHORITY.
# This prevents the "FileNotFoundError: /home/archsean/.Xauthority"
export XAUTHORITY=/tmp/hyprland-xauth-$(id -u)

# 2. Clear any previous data in the temporary authorization file.
rm -f "$XAUTHORITY"

# 3. Add the actual, currently valid MIT-MAGIC-COOKIE key to the temporary file.
# This fixes the "Invalid MIT-MAGIC-COOKIE-1 key" error.
# NOTE: The key and display name MUST match the output of 'xauth list $DISPLAY'
#       We are using the exact values retrieved from your session.
# Format: xauth add [DISPLAY] [PROTOCOL] [KEY]
xauth add ArchSean/unix:0 MIT-MAGIC-COOKIE-1 cd65fdcded2998eae80f6476f6513b9f

# 4. Grant access to the local user (helps bypass final connection checks).
xhost +si:localuser:$(whoami)

# --------------------------------------------------------------------------

# Change directory to the Pysean repo
cd "$HOME/Documents/GitHub/Pysean" || exit 1

# Activate the Python Virtual Environment
source "$HOME/venv/bin/activate"

# Replace the current process with the interactive shell
exec "$SHELL"
