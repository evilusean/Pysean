import piper
import csv
import os
import subprocess

#THIS IS THE WORKING VERSION TO USE FOR PARSING A CSV(SLOVAK[0]ENGLISH[1]), IT WILL CREATE A FAST SLOVAK AUDIO AND
#SLOW IT DOWN THEN DELETE THE FAST ONE (SLOWVAK) THEN UPDATE A CSV FOR ANKI WITH THE SOUND LOCATION
# IT WILL THEN TAKE THE SLOWVAK AUDIO, REPEAT it x3 TIMES WITH a PAUSE, AND ADD ENGLISH ONCE, SAVE THAT TO A CENTRAL LOCASEAN
# CREATING A VOCABULARY LIST OF THE WORDS FROM THE CSV - USES PIPER SLOVAK VOICE FOR CREATING THE AUDIO
# TO USE: PLACE THE CSV IN A FILE WITH THE SAME NAME '/{category}/category.csv' SCROLL TO BOTTOM, CHANGE THE 'CATEGORY=' TO CSV
# WITH SLOVAK / ENGLISH - MAKE SURE YOU HAVE THE PIPER VOICE MODELS DOWNLOADED - CHANGE DIRECTORIES IF USING ON NEW PC -

# Define the voices
english_voice = "en_US-lessac-medium"
slovak_voice = "sk_SK-lili-medium"  # Assuming you have a Slovak model named 'sk_SK-lili-medium'
pause = "/media/sean/MusIX/Piper/silent_half-second.wav"

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

# Function to synthesize and save Slovak audio with speed control
def synthesize_slovak(text, filename, speed_factor=1.0):
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

    # Modify the audio file using FFmpeg to change the speed
    input_file = os.path.join(slovak_audio_dir, filename + ".wav")
    output_file = os.path.join(slovak_audio_dir, filename + "_slow.wav")
    ffmpeg_command = [
        "ffmpeg",
        "-i",
        input_file,
        "-filter:a",
        f"atempo={speed_factor}",
        output_file,
    ]
    subprocess.run(ffmpeg_command)
    print(f"Slovak audio slowed down and saved to {output_file}")

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
        writer.writerow([english_text, slovak_text, f"[sound:file://{os.path.join(slovak_audio_dir, slovak_filename + '_slow.wav')}]"])  
        # Update CSV link to .wav, using the slowed down file

# Function to combine audio files into a single file using FFmpeg
def combine_audio_files(category):
    global slovak_audio_dir, english_audio_dir, pause  # Declare variables as global
    slovak_audio_dir, english_audio_dir = get_audio_dirs(category)
    output_dir = "/media/sean/MusIX/Piper/Slovak/1VocabLists"  # New output directory
    os.makedirs(output_dir, exist_ok=True)

    # Create a temporary file to store the file list
    temp_file = os.path.join(output_dir, "temp_concat_list.txt")

    # Write the file list to the temporary file
    with open(temp_file, "w") as f:
        # Get a list of all audio files in both folders
        slovak_files = [f for f in os.listdir(slovak_audio_dir) if f.endswith("_slow.wav")]  # Get slowed down Slovak files
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
            f.write(f"file '{os.path.join(slovak_audio_dir, slovak_file)}'\n")
            f.write(f"file '{pause}'\n")
            f.write(f"file '{os.path.join(slovak_audio_dir, slovak_file)}'\n")
            f.write(f"file '{pause}'\n")
            f.write(f"file '{os.path.join(slovak_audio_dir, slovak_file)}'\n")
            f.write(f"file '{pause}'\n")  # Add pause after each Slovak word
            f.write(f"file '{os.path.join(english_audio_dir, english_file)}'\n")  # Add English file path
            f.write(f"file '{pause}'\n")  # Add pause after each English word

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

    # Delete the original fast Slovak files
    for slovak_file in slovak_files:
        original_file = os.path.join(slovak_audio_dir, slovak_file.replace("_slow.wav", ".wav"))
        if os.path.exists(original_file):
            os.remove(original_file)
            print(f"Deleted original Slovak file: {original_file}")

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

            # Synthesize and save the Slovak audio with speed control
            synthesize_slovak(slovak_text, slovak_filename, speed_factor=0.7)  # Slow down the Slovak speaker

            # Synthesize and save the English audio
            synthesize_english(english_text, english_filename)

            # Write to the CSV
            write_to_csv(english_text, slovak_text, slovak_filename, english_filename)

    print(f"Translation and audio synthesis complete for {category}!")

    # Combine the audio files using FFmpeg
    combine_audio_files(category)

# going to use this for Slovake.eu course 'Slovake.eu-L1' = lesson 1
category = "2000"  # Replace with your directory / CSV name (must be the same)
process_csv(category)