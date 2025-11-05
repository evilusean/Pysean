#!/bin/bash
# Script for Japanese and English OCR capture and clipboard copy (Accuracy Improved)

# 📦 REQUIRED PACKAGES (Install with pacman -S):
# sudo pacman -S tesseract grim slurp wl-clipboard
# sudo pacman -S tesseract-data-eng tesseract-data-jpn

# !!! CRITICAL FIX: Set TESSDATA_PREFIX for Tesseract language files !!!
export TESSDATA_PREFIX="/usr/share/tessdata"

# Optional: Using full paths for robustness in Hyprland binds
MKTEMP_CMD="/usr/bin/mktemp"
TRAP_CMD="/usr/bin/rm"
SLURP_CMD="/usr/bin/slurp"
GRIM_CMD="/usr/bin/grim"
TESSERACT_CMD="/usr/bin/tesseract"
WLCOPY_CMD="/usr/bin/wl-copy"
NOTIFY_SEND_CMD="/usr/bin/notify-send"

# --- Main Script ---

# 1. Setup temp file and cleanup trap
TEMP_FILE="$($MKTEMP_CMD --suffix=.png)"
trap '$TRAP_CMD -f "$TEMP_FILE"' EXIT

# 2. Get screen selection geometry and handle cancellation
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

# 4. Run Tesseract OCR (jpn+eng) and copy to clipboard
# KEY CHANGE: Changed -l eng+jpn to -l jpn+eng to prioritize Japanese recognition.
if $TESSERACT_CMD "$TEMP_FILE" stdout -l jpn+eng --psm 6 --oem 1 2>/dev/null | $WLCOPY_CMD; then
    $NOTIFY_SEND_CMD -t 1000 -a 'Hyprland' "Bilingual (JPN+ENG) text captured and copied to clipboard."
else
    $NOTIFY_SEND_CMD -t 1000 -a 'Hyprland' "OCR or clipboard copy failed."
    exit 1
fi
