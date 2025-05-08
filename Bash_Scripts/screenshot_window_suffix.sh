#!/bin/bash

#a simple script for taking a screenshot, selecting an area, and adding a suffix to it
# can change the prefix by changing 'BASE_FILENAME'

# --- Configuration ---
SCREENSHOT_FOLDER="$HOME/Pictures/WindowShots"
BASE_FILENAME="screenshot"

# --- Ensure the output folder exists ---
mkdir -p "$SCREENSHOT_FOLDER"

# --- Get the window geometry using interactive slurp ---
window_geometry=$(slurp)

if [ -n "$window_geometry" ]; then
    # --- Create a temporary filename for the initial capture ---
    temp_file=$(mktemp /tmp/window_screenshot_XXXXXX.png)

    # --- Take the screenshot of the selected window ---
    grim -g "$window_geometry" "$temp_file"

    if [ -f "$temp_file" ]; then
        # --- Get the current timestamp ---
        timestamp=$(date '+%Y-%m-%d_%H-%M-%S')

        # --- Prompt the user for a suffix using zenity (or yad) ---
        suffix=$(zenity --entry --title="Add Suffix" --text="Enter text to add to the filename:")
        if [ $? -ne 0 ]; then
            suffix=$(yad --title="Add Suffix" --text="Enter text to add to the filename:" --entry)
        fi

        # --- Sanitize the suffix for the filename (remove spaces and special chars) ---
        sanitized_suffix=$(echo "$suffix" | sed -e 's/[^a-zA-Z0-9_-]/_/g')

        # --- Construct the final filename ---
        filename="${SCREENSHOT_FOLDER}/${BASE_FILENAME}_${timestamp}${sanitized_suffix:+_$sanitized_suffix}.png"

        # --- Move the temporary file to the final destination with the new name ---
        mv "$temp_file" "$filename"

        echo "Screenshot saved as: $filename"
        notify-send "Screenshot Saved" "$filename"
    else
        echo "Error: Failed to capture window screenshot."
        notify-send "Screenshot Error" "Failed to capture window."
    fi
else
    echo "Error: No region selected with slurp."
    notify-send "Screenshot Error" "No region selected."
fi
