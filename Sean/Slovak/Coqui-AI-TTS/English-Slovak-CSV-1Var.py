import os
import subprocess
import csv

# Define the voices
english_voice = "tts_models/en/ljspeech/vits"  # taco bout it
slovak_voice = "tts_models/sk/cv/vits"  # Choose a Slovak model that works from the list
pause = "/media/sean/MusIX/Piper/silent_half-second.wav"

# Define the output directories for Slovak and English audio files
# Make the directory names dynamic
def get_audio_dirs(category):
    slovak_audio_dir = f"/media/sean/MusIX/Coqui-AI/Slovak/{category}/Slovak"
    english_audio_dir = f"/media/sean/MusIX/Coqui-AI/Slovak/{category}/English"
    return slovak_audio_dir, english_audio_dir

# Create the directories if they don't exist
def create_dirs(category):
    global slovak_audio_dir, english_audio_dir  # Declare variables as global
    slovak_audio_dir, english_audio_dir = get_audio_dirs(category)
    os.makedirs(slovak_audio_dir, exist_ok=True)
    os.makedirs(english_audio_dir, exist_ok=True)

# Define the CSV file paths, testing with 'slovak10.csv' before 'slovak1000.csv'
def get_csv_paths(category):
    input_csv_file = f"/media/sean/MusIX/Coqui-AI/Slovak/{category}/{category}.csv"  # Replace with your input CSV file path
    output_csv_file = f"/media/sean/MusIX/Coqui-AI/Slovak/{category}/{category}_anki.csv"
    return input_csv_file, output_csv_file

# Function to synthesize and save Slovak audio (no speed control)
def synthesize_slovak(text, filename):
    global slovak_audio_dir  # Declare variable as global
    # Use subprocess to run the coqui-ai-tts command
    subprocess.run(
        [
            "tts",
            "--text",
            text,
            "--model_name",
            slovak_voice,
            "--out_path",
            os.path.join(slovak_audio_dir, filename + ".wav"),
        ],
    )
    print(f"Slovak audio saved to {os.path.join(slovak_audio_dir, filename + '.wav')}")

def synthesize_english(text, filename, counter):
    global english_audio_dir  # Declare variable as global
    # Use subprocess to run the coqui-ai-tts command
    subprocess.run(
        [
            "tts",
            "--text",
            f"{counter}. {text}",  # Add the counter to the text
            "--model_name",
            english_voice,
            "--out_path",
            os.path.join(english_audio_dir, filename + ".wav"),
        ],
    )
    print(f"English audio saved to {os.path.join(english_audio_dir, filename + '.wav')}")


# Function to write to the CSV
def write_to_csv(english_text, slovak_text, slovak_filename, english_filename):
    global output_csv_file, slovak_audio_dir  # Declare variables as global
    with open(output_csv_file, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([english_text, slovak_text, f"[sound:file://{os.path.join(slovak_audio_dir, slovak_filename + '.wav')}]"])  
        # Update CSV link to .wav, using the slowed down file

# Function to combine audio files into a single file using FFmpeg
def combine_audio_files(category):
    global slovak_audio_dir, english_audio_dir, pause  # Declare variables as global
    slovak_audio_dir, english_audio_dir = get_audio_dirs(category)
    output_dir = "/media/sean/MusIX/Coqui-AI/Slovak/1VocabLists"  # New output directory
    os.makedirs(output_dir, exist_ok=True)

    # Create a temporary file to store the file list
    temp_file = os.path.join(output_dir, "temp_concat_list.txt")

    # Write the file list to the temporary file
    with open(temp_file, "w") as f:
        # Get a list of all audio files in both folders
        slovak_files = [f for f in os.listdir(slovak_audio_dir) if f.endswith(".wav")]  # Get slowed down Slovak files
        english_files = [f for f in os.listdir(english_audio_dir) if f.endswith(".wav")]

        # Sort the files numerically (assuming filenames start with numbers)
        slovak_files.sort()
        english_files.sort()

        # Ensure both lists have the same length
        min_length = min(len(slovak_files), len(english_files))

        # Write the file list to the temporary file
        for i in range(min_length):  # Iterate up to the shorter list's length
            slovak_file = slovak_files[i]
            english_file = english_files[i]
            f.write(f"file '{os.path.join(english_audio_dir, english_file)}'\n")  # Add English file path
            f.write(f"file '{pause}'\n")  # Add pause after each English word
            f.write(f"file '{os.path.join(slovak_audio_dir, slovak_file)}'\n")  # Add Slovak file path
            f.write(f"file '{pause}'\n")  # Add pause after each Slovak word
            f.write(f"file '{os.path.join(slovak_audio_dir, slovak_file)}'\n")  # Add Slovak file path
            f.write(f"file '{pause}'\n")  # Add pause after each Slovak word
            f.write(f"file '{os.path.join(slovak_audio_dir, slovak_file)}'\n")  # Add Slovak file path
            f.write(f"file '{pause}'\n")  # Add pause after each Slovak word

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
        # Reset timestamps for each segment
        "[0:a]asetpts=PTS-STARTPTS[out]",
        "-map",
        "[out]",
        "-c:a",
        "libmp3lame",
        os.path.join(output_dir, f"{category}.mp3"),  # Use category in the filename
        "-loglevel",
        "error",  # Suppress warning messages
    ]

    # Run the FFmpeg command
    subprocess.run(ffmpeg_command)

    print(f"Audio files combined into {category}.mp3 in {output_dir}")

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

        counter = 1  # Initialize the counter
        for i, row in enumerate(reader):
            slovak_text = row[0].strip()
            english_text = row[1].strip()

            # Create unique filenames with 4-digit formatting and words
            slovak_filename = f"{str(i+1).zfill(4)}"  # Only use the 4-digit number
            english_filename = f"{str(i+1).zfill(4)}"  # Only use the 4-digit number

            # Synthesize and save the Slovak audio (no speed control)
            synthesize_slovak(slovak_text, slovak_filename)

            # Synthesize and save the English audio with counter
            synthesize_english(english_text, english_filename, counter)

            # Write to the CSV
            write_to_csv(english_text, slovak_text, slovak_filename, english_filename)

            counter += 1  # Increment the counter

    print(f"Translation and audio synthesis complete for {category}!")

    # Combine the audio files using FFmpeg
    combine_audio_files(category)

# going to use this for Slovake.eu course 'Slovake.eu-L1' = lesson 1
category = "Slovake.eu-L13"  # Replace with your directory / CSV name (must be the same)
process_csv(category)