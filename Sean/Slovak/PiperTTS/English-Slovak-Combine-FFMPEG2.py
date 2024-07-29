import os
import subprocess
import time

def combine_audio_files(category):
    """Combines audio files from Slovak and English folders into a single file,
    repeating Slovak words three times with a delay before playing the English word.

    Args:
        category (str): The category name (e.g., "Numbers", "Shopping").
    """

    slovak_audio_dir = f"/media/sean/MusIX/Piper/Slovak/{category}/Slovak"
    english_audio_dir = f"/media/sean/MusIX/Piper/Slovak/{category}/English"

    # Get a list of all audio files in both folders
    slovak_files = [f for f in os.listdir(slovak_audio_dir) if f.endswith(".wav")]
    english_files = [f for f in os.listdir(english_audio_dir) if f.endswith(".wav")]

    # Sort the files numerically (assuming filenames start with numbers)
    slovak_files.sort()
    english_files.sort()

    # Print the file paths for debugging
    print("Slovak Files:")
    for f in slovak_files:
        print(os.path.join(slovak_audio_dir, f))
    print("English Files:")
    for f in english_files:
        print(os.path.join(english_audio_dir, f))

    # Construct the FFmpeg command to combine the files
    ffmpeg_command = [
        "ffmpeg",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        "<(for f in " + " ".join(
            [os.path.join(slovak_audio_dir, f) for f in slovak_files]
        ) + "; do echo \"file '$f'\"; done)",
        "-i",
        "<(for f in " + " ".join(
            [os.path.join(english_audio_dir, f) for f in english_files]
        ) + "; do echo \"file '$f'\"; done)",
        # ... rest of your FFmpeg command ...
    ]

    # Run the FFmpeg command
    subprocess.run(ffmpeg_command)

    print(f"Audio files combined into {category}_Slovak_English_Combined.wav in /media/sean/MusIX/Piper/Slovak/{category}/")

# Example usage:
category = "Numbers"  # Replace with your category
combine_audio_files(category)
