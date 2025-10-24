#!/bin/bash
# Script for Japanese and English OCR capture and clipboard copy
# Prerequisites: tesseract, tesseract-data-jpn, tesseract-data-eng, grim, slurp, wl-clipboard
# Keybinding to execute Japanese/English OCR
# bindd = SUPER ALT SHIFT, T, OCR Japanese to Clipboard, exec, ~/scripts/ocr_to_clipboard_jpn.sh
# chmod +x ~/scripts/ocr_to_clipboard_jpn.sh

# Create a temporary file for the screen capture
TEMP_FILE="$(mktemp --suffix=.png)"

# Capture selected area with grim, run Tesseract OCR using both English (eng) and Japanese (jpn),
# copy the output to wl-clipboard, and delete the temporary file.
grim -g "$(slurp)" "$TEMP_FILE" && \
tesseract "$TEMP_FILE" -l eng+jpn - | wl-copy && \
rm "$TEMP_FILE"

# Send a silent notification if the command was successful
if [ $? -eq 0 ]; then
    notify-send -t 1000 -a 'Hyprland' "Japanese/English text captured via OCR and copied to clipboard."
fi
