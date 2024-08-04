import os
import subprocess
import csv

#created a script that combined the naturally spoken slovak I downloaded as individual MP3's, which then
#creates an english version from the CSV I used for ANKI, and combines the natural slovak with AI english into a vocabulary list
#keep getting below error :
# [concat @ 0x591cfeb16840] Impossible to open '/media/sean/MusIX/Coqui-AI/Slovak/1VocabLists/media/sean/MusIX/Slovak.Czech/slovake.eu-audio/Dates/január' /media/sean/MusIX/Coqui-AI/Slovak/1VocabLists/temp_concat_list.txt: No such file or directory

# Define the voices
english_voice = "tts_models/en/ljspeech/vits"  # taco bout it
pause = "/media/sean/MusIX/Piper/silent_half-second.wav"

# Define the output directories for Slovak and English audio files
# Make the directory names dynamic
def get_audio_dirs(category):
    english_audio_dir = f"/media/sean/MusIX/Slovak.Czech/slovake.eu-audio/{category}/English"
    return english_audio_dir

# Create the directories if they don't exist
def create_dirs(category):
    global english_audio_dir  # Declare variables as global
    english_audio_dir = get_audio_dirs(category)
    os.makedirs(english_audio_dir, exist_ok=True)

# Define the CSV file paths
def get_csv_paths(category):
    input_csv_file = f"/media/sean/MusIX/Slovak.Czech/slovake.eu-audio/{category}/{category}.csv"  # Replace with your input CSV file path
    return input_csv_file

# Function to synthesize and save English audio (no speed control)
def synthesize_english(text, filename):
    global english_audio_dir  # Declare variable as global
    # Use subprocess to run the coqui-ai-tts command
    subprocess.run(
        [
            "tts",
            "--text",
            text,
            "--model_name",
            english_voice,
            "--out_path",
            os.path.join(english_audio_dir, filename + ".wav"),
        ],
    )
    print(f"English audio saved to {os.path.join(english_audio_dir, filename + '.wav')}")
    return os.path.join(english_audio_dir, filename + ".wav")  # Return the full path

# Function to combine audio files into a single file using FFmpeg
def combine_audio_files(category, english_filenames, slovak_filenames):
    global english_audio_dir, pause  # Declare variables as global
    english_audio_dir = get_audio_dirs(category)
    # Removed: output_dir = "/media/sean/MusIX/Coqui-AI/Slovak/1VocabLists"  # New output directory
    # Removed: os.makedirs(output_dir, exist_ok=True)

    # Create a temporary file to store the file list
    temp_file = os.path.join(english_audio_dir, "temp_concat_list.txt")  # Use english_audio_dir

    # Write the file list to the temporary file
    with open(temp_file, "w") as f:
        # Ensure both lists have the same length
        min_length = len(english_filenames)

        # Write the file list to the temporary file
        for i in range(min_length):  # Iterate up to the shorter list's length
            # English - Slovak - English - Slovak order
            f.write(f"file '{english_filenames[i]}'\n")  # Add English file path
            f.write(f"file '{pause}'\n")  # Add pause after each English word
            f.write(f"file '{slovak_filenames[i]}'\n")  # Add Slovak file path (directly from the list)
            f.write(f"file '{pause}'\n")  # Add pause after each Slovak word
            if i < min_length - 1:  # Add another English-Slovak pair if not the last one
                f.write(f"file '{english_filenames[i + 1]}'\n")  # Add English file path
                f.write(f"file '{pause}'\n")  # Add pause after each English word
                f.write(f"file '{slovak_filenames[i + 1]}'\n")  # Add Slovak file path (directly from the list)
                f.write(f"file '{pause}'\n")  # Add pause after each Slovak word
                i += 1  # Skip the next iteration to avoid repetition

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
        os.path.join(english_audio_dir, f"{category}_combined.mp3"),  # Use english_audio_dir
        "-loglevel",
        "error",  # Suppress warning messages
    ]

    # Run the FFmpeg command
    subprocess.run(ffmpeg_command)

    print(f"Audio files combined into {category}_combined.mp3 in {english_audio_dir}")  # Use english_audio_dir

    # Delete the temporary file
    os.remove(temp_file)

# Main function to process the CSV
def process_csv(category):
    global english_audio_dir  # Declare variable as global
    create_dirs(category)
    input_csv_file = get_csv_paths(category)

    slovak_filenames = []  # Create a list to store Slovak filenames
    english_filenames = []  # Create a list to store English filenames

    # Create the temporary file outside the loop
    # Removed: output_dir = "/media/sean/MusIX/Coqui-AI/Slovak/1VocabLists"  # New output directory
    # Removed: os.makedirs(output_dir, exist_ok=True)
    temp_file = os.path.join(english_audio_dir, "temp_concat_list.txt")  # Use english_audio_dir
    with open(temp_file, "w") as f:
        with open(input_csv_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)

            for i, row in enumerate(reader):
                english_text = row[0].strip()  # Assuming English text is in the first column
                slovak_audio_file = row[2].strip()  # Assuming Slovak audio file location is in the third column

                # Extract the filename from the audio file location
                slovak_filename = slovak_audio_file.split("file:///")[1].replace("]", "")
                slovak_filenames.append(slovak_filename)  # Add the filename to the list

                # Create unique filenames with 4-digit formatting and words
                english_filename = f"{str(i+1).zfill(4)}"  # Only use the 4-digit number

                # Synthesize and save the English audio (no speed control)
                english_file_path = synthesize_english(english_text, english_filename)
                english_filenames.append(english_file_path)  # Add the filename to the list

                # Write the English and Slovak filenames to the temp file
                f.write(f"file '{english_file_path}'\n")
                f.write(f"file '{pause}'\n")
                f.write(f"file '{slovak_filenames[i]}'\n")
                f.write(f"file '{pause}'\n")

        # Print the slovak_filenames list for debugging
        print("slovak_filenames:", slovak_filenames)
        # Print the contents of the temp_concat_list.txt file
        print("temp_concat_list.txt contents:")
        with open(temp_file, "r") as f:
            print(f.read())

    # Combine all audio files into one file after the loop
    combine_audio_files(category, english_filenames, slovak_filenames)  # Pass the list of Slovak filenames

    print(f"Translation and audio synthesis complete for {category}!")

category = "Dates"  # Replace with your directory / CSV name (must be the same)
process_csv(category)