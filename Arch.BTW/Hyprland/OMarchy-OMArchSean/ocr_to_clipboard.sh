#!/bin/bash
# Script for OCR capture and clipboard copy (Fixed for Omarchy/Hyprland)

# 📦 REQUIRED PACKAGES (Install with pacman -S):
# sudo pacman -S tesseract grim slurp wl-clipboard
# sudo pacman -S tesseract-data-eng tesseract-data-jpn (or other languages)

# !!! CRITICAL FIX: Set TESSDATA_PREFIX to the correct location for Tesseract !!!
# This ensures Tesseract can find its language files when run via a Hyprland bind.
export TESSDATA_PREFIX="/usr/share/tessdata"

# Optional: Using full paths for robustness in Hyprland binds
# VERIFY these paths with 'which <command>' on your system!
MKTEMP_CMD="/usr/bin/mktemp"
TRAP_CMD="/usr/bin/rm"
SLURP_CMD="/usr/bin/slurp"
GRIM_CMD="/usr/bin/grim"
TESSERACT_CMD="/usr/bin/tesseract"
WLCOPY_CMD="/usr/bin/wl-copy"
NOTIFY_SEND_CMD="/usr/bin/notify-send"

# 1. Setup temp file and cleanup trap
TEMP_FILE="$($MKTEMP_CMD --suffix=.png)"
# Ensure the temp file is deleted even if the script fails or is interrupted.
trap '$TRAP_CMD -f "$TEMP_FILE"' EXIT

# 2. Get screen selection geometry
GEOMETRY="$($SLURP_CMD)"
if [ -z "$GEOMETRY" ]; then
    $NOTIFY_SEND_CMD -t 1000 -a 'Hyprland' "OCR selection cancelled."
    exit 0
fi

# 3. Capture selected area
$GRIM_CMD -g "$GEOMETRY" "$TEMP_FILE"

# Check if grim succeeded in creating the file
if [ ! -f "$TEMP_FILE" ]; then
    $NOTIFY_SEND_CMD -t 1000 -a 'Hyprland' "Screen capture (grim) failed."
    exit 1
fi

# 4. Run Tesseract OCR and copy to clipboard
# Outputs the result to stdout ('-'), suppressing stderr (2>/dev/null) to keep output clean.
if $TESSERACT_CMD "$TEMP_FILE" stdout -l eng 2>/dev/null | $WLCOPY_CMD; then
    $NOTIFY_SEND_CMD -t 1000 -a 'Hyprland' "Text captured via OCR and copied to clipboard."
else
    $NOTIFY_SEND_CMD -t 1000 -a 'Hyprland' "OCR or clipboard copy failed."
    exit 1
fi
