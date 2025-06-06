#!/bin/bash
# Usage: ./save_folder_names.sh [directory]
# If no directory is provided, the current directory is used.

# Set the target directory (default: current directory)
TARGET_DIR="${1:-.}"

# Define the output file (placed in the target directory)
OUTPUT_FILE="${TARGET_DIR%/}/folder_names.txt"

# Remove an existing output file if present
rm -f "$OUTPUT_FILE"

# Find directories (excluding the TARGET_DIR itself) and save only folder names
find "$TARGET_DIR" -mindepth 1 -maxdepth 1 -type d -printf "%f\n" > "$OUTPUT_FILE"

echo "Folder names have been saved to: $OUTPUT_FILE"