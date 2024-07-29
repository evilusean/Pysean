import piper
import csv
import os
import subprocess

# Define the voices
english_voice = "en_US-lessac-medium"
slovak_voice = "sk_SK-lili-medium"  # Assuming you have a Slovak model named 'sk_SK-lili-medium'

# Define the output directories for Slovak and English audio files
# Make the directory names dynamic
def get_audio_dirs(category):
    slovak_audio_dir = f"/media/sean/MusIX/Piper/Slovak/{category}/Slovak"
    english_audio_dir = f"/media/sean/MusIX/Piper/Slovak/{category}/English"
    return slovak_audio_dir, english_audio_dir

# Create the directories if they don't exist
def create_dirs(category):
    global slovak_audio_dir, english_audio_dir  # Declare variables as global
    slovak_audio_dir, english_audio_dir = get_audio_dirs(category)
    os.makedirs(slovak_audio_dir, exist_ok=True)
    os.makedirs(english_audio_dir, exist_ok=True)

# Define the CSV file paths, testing with 'slovak10.csv' before 'slovak1000.csv'
def get_csv_paths(category):
    input_csv_file = f"/media/sean/MusIX/Piper/Slovak/{category}/{category}.csv"  # Replace with your input CSV file path
    output_csv_file = f"/media/sean/MusIX/Piper/Slovak/{category}/{category}_anki.csv"
    return input_csv_file, output_csv_file

# Function to synthesize and save Slovak audio
def synthesize_slovak(text, filename):
    global slovak_audio_dir  # Declare variable as global
    # Use subprocess to run the piper command
    subprocess.run(
        [
            "piper",
            "-m",
            "/media/sean/MusIX/Piper/sk_SK-lili-medium.onnx",  # Replace with the path to your Slovak model
            "-c",
            "/media/sean/MusIX/Piper/sk_SK-lili-medium.onnx.json",  # Replace with the path to your Slovak config
            "-f",
            os.path.join(slovak_audio_dir, filename + ".wav"),
            # "-s",  # Remove the speaker argument as it's not needed
            "--sentence-silence",
            "0.5", # Add a 0.5 second silence between sentences
        ],
        input=text.encode("utf-8"),
    )
    print(f"Slovak audio saved to {os.path.join(slovak_audio_dir, filename + '.wav')}")

# Function to synthesize and save English audio
def synthesize_english(text, filename):
    global english_audio_dir  # Declare variable as global
    # Use subprocess to run the piper command
    subprocess.run(
        [
            "piper",
            "-m",
            "/media/sean/MusIX/Piper/en_US-lessac-medium.onnx",  # Replace with the path to your English model
            "-c",
            "/media/sean/MusIX/Piper/en_US-lessac-medium.onnx.json",  # Replace with the path to your English config
            "-f",
            os.path.join(english_audio_dir, filename + ".wav"),
            # "-s",  # Remove the speaker argument as it's not needed
            "--sentence-silence",
            "0.5",  # Add a 0.5 second silence between sentences
        ],
        input=text.encode("utf-8"),
    )
    print(f"English audio saved to {os.path.join(english_audio_dir, filename + '.wav')}")

# Function to write to the CSV
def write_to_csv(english_text, slovak_text, slovak_filename, english_filename):
    global output_csv_file, slovak_audio_dir  # Declare variables as global
    with open(output_csv_file, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([english_text, slovak_text, f"[sound:file://{os.path.join(slovak_audio_dir, slovak_filename + '.wav')}]"])  
        # Update CSV link to .wav

# Function to combine audio files into a single file using FFmpeg
def combine_audio_files(category):
    global slovak_audio_dir, english_audio_dir  # Declare variables as global
    slovak_audio_dir, english_audio_dir = get_audio_dirs(category)
    output_dir = os.path.join(f"/media/sean/MusIX/Piper/Slovak/{category}/", "combined")
    os.makedirs(output_dir, exist_ok=True)

    # Create a temporary file to store the file list
    temp_file = os.path.join(output_dir, "temp_concat_list.txt")

    # Write the file list to the temporary file
    with open(temp_file, "w") as f:
        # Get a list of all audio files in both folders
        slovak_files = [f for f in os.listdir(slovak_audio_dir) if f.endswith(".wav")]
        english_files = [f for f in os.listdir(english_audio_dir) if f.endswith(".wav")]

        # Sort the files numerically (assuming filenames start with numbers)
        slovak_files.sort()
        english_files.sort()

        # Write the file list to the temporary file
        for i in range(len(slovak_files)):
            slovak_file = slovak_files[i]
            english_file = english_files[i]
            f.write(f"file '{os.path.join(slovak_audio_dir, slovak_file)}'\n")
            f.write(f"file '{os.path.join(slovak_audio_dir, slovak_file)}'\n")
            f.write(f"file '{os.path.join(slovak_audio_dir, slovak_file)}'\n")
            f.write(f"file '{os.path.join(english_audio_dir, english_file)}'\n")

    # Construct the FFmpeg command to combine the files
    ffmpeg_command = [
        "ffmpeg",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        temp_file,
        "-filter_complex",
        # Repeat Slovak three times with a 1-second delay
        "[0:a]atrim=0:1,asetpts=PTS-STARTPTS[slovak1];"
        "[slovak1]adelay=1000|1000[slovak2];"
        "[slovak2]atrim=0:1,asetpts=PTS-STARTPTS[slovak3];"
        "[slovak3]adelay=1000|1000[slovak4];"
        "[slovak4]atrim=0:1,asetpts=PTS-STARTPTS[slovak5];"
        "[slovak5]adelay=1000|1000[slovak6];"
        # Combine Slovak and English
        "[slovak6][1:a]concat=n=2:v=0:a=1[out]",
        "-map",
        "[out]",
        "-c:a",
        "libmp3lame",
        os.path.join(output_dir, f"{category}_Combined.mp3"),  # Use category in the filename
    ]

    # Run the FFmpeg command
    subprocess.run(ffmpeg_command)

    print(f"Audio files combined into {category}_Combined.mp3 in {output_dir}")

    # Delete the temporary file
    os.remove(temp_file)

# Main function to process the CSV
def process_csv(category):
    global output_csv_file  # Declare variable as global
    create_dirs(category)
    input_csv_file, output_csv_file = get_csv_paths(category)
    #slovak_audio_dir, english_audio_dir = get_audio_dirs(category)  # No need to redefine here

    with open(input_csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row (if any)

        for i, row in enumerate(reader):
            slovak_text = row[0].strip()
            english_text = row[1].strip()

            # Create unique filenames with 4-digit formatting and words
            slovak_filename = f"{str(i+1).zfill(4)}"  # Only use the 4-digit number
            english_filename = f"{str(i+1).zfill(4)}"  # Only use the 4-digit number

            # Synthesize and save the Slovak audio
            synthesize_slovak(slovak_text, slovak_filename)

            # Synthesize and save the English audio
            synthesize_english(english_text, english_filename)

            # Write to the CSV
            write_to_csv(english_text, slovak_text, slovak_filename, english_filename)

    print(f"Translation and audio synthesis complete for {category}!")

    # Combine the audio files using FFmpeg
    combine_audio_files(category)

# Example usage:
category = "Numbers2"  # Replace with your directory / CSV name (must be the same)
process_csv(category)