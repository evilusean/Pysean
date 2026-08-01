#!/usr/bin/env python3
import subprocess
import os
import sys

def main():
    print("=== EPUB to Audiobook Automator ===")
    
    # Prompt for the EPUB file path (supports copy-pasting paths)
    epub_path = input("Enter or paste the path to the EPUB file: ").strip()
    
    # Clean up any surrounding quotes if pasted with them
    epub_path = epub_path.strip("'\"")
    
    if not os.path.isfile(epub_path):
        print(f"Error: File not found at '{epub_path}'. Please check the path.")
        sys.exit(1)
        
    # Define default output directory
    default_output = os.path.expanduser("~/Downloads/Audiobooks")
    
    output_folder = input(f"Enter output folder [Default: {default_output}]: ").strip()
    if not output_folder:
        output_folder = default_output
    else:
        output_folder = output_folder.strip("'\"")
        
    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Optional chapter range
    chapter_start = input("Enter starting chapter number (leave blank for start): ").strip()
    chapter_end = input("Enter ending chapter number (leave blank for end): ").strip()
    
    # Build command
    cmd = [
        "epub_to_audiobook",
        epub_path,
        output_folder,
        "--tts", "edge"
    ]
    
    if chapter_start:
        cmd.extend(["--chapter_start", chapter_start])
    if chapter_end:
        cmd.extend(["--chapter_end", chapter_end])
        
    print(f"\nRunning command:\n{' '.join(cmd)}\n")
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\nSuccess! Audiobook saved to: {output_folder}")
    except subprocess.CalledProcessError as e:
        print(f"\nError during conversion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
