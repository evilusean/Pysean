#!/bin/bash
# Script for OCR capture and clipboard copy
# save the script to '~/bin/ocr_to_clipboard.sh' 

# Capture selected screen area to a temp file, run Tesseract OCR, copy to clipboard, and delete the temp file.
TEMP_FILE="$(mktemp --suffix=.png)"

# Use slurp to select area, grim to capture, tesseract for OCR, wl-copy for clipboard
grim -g "$(slurp)" "$TEMP_FILE" && \
tesseract "$TEMP_FILE" - | wl-copy && \
rm "$TEMP_FILE"

# Optional: send a silent notification if successful
if [ $? -eq 0 ]; then
    notify-send -t 1000 -a 'Hyprland' "Text captured via OCR and copied to clipboard."
fi
