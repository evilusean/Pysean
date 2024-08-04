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

# Define the output directory for the new CSV file
output_csv_file = "/media/sean/MusIX/Coqui-AI/Slovak/1VocabLists/{category}_combined_audio.csv"

# Define the output directory for English audio files
# Make the directory names dynamic
def get_audio_dirs(category):
    english_audio_dir = f"/media/sean/MusIX/Slovak.Czech/slovake.eu-audio/{category}/English"
    return english_audio_dir

# Create the directories if they don't exist
def create_dirs(category):
    global english_audio_dir  # Declare variables as global
    english_audio_dir = get_audio_dirs(category)
    os.makedirs(english_audio_dir, exist_ok=True)

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
def combine_audio_files(category, csv_file):
    global pause  # Declare variable as global
    output_dir = "/media/sean/MusIX/Coqui-AI/Slovak/1VocabLists"  # New output directory
    os.makedirs(output_dir, exist_ok=True)

    # Create a temporary file to store the file list
    temp_file = os.path.join(output_dir, "temp_concat_list.txt")

    # Write the file list to the temporary file
    with open(temp_file, "w") as f:
        with open(csv_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row

            for row in reader:
                english_file = row[1]
                slovak_file = row[2]
                f.write(f"file '{english_file}'\n")  # Add English file path
                f.write(f"file '{pause}'\n")  # Add pause after each English word
                f.write(f"file '{slovak_file}'\n")  # Add Slovak file path
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
        os.path.join(output_dir, f"{category}_combined.mp3"),  # Use category in the filename
        "-loglevel",
        "error",  # Suppress warning messages
    ]

    # Run the FFmpeg command
    subprocess.run(ffmpeg_command)

    print(f"Audio files combined into {category}_combined.mp3 in {output_dir}")

    # Delete the temporary file
    os.remove(temp_file)

# Main function to process the CSV
def process_csv(category):
    global output_csv_file  # Declare variable as global
    input_csv_file = f"/media/sean/MusIX/Slovak.Czech/slovake.eu-audio/{category}/{category}.csv"  # Replace with your input CSV file path
    create_dirs(category)

    # Create the new CSV file
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["English Text", "English Audio", "Slovak Audio"])  # Write the header row

        with open(input_csv_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row

            for i, row in enumerate(reader):
                english_text = row[0].strip()  # Assuming English text is in the first column
                slovak_audio_file = row[2].strip()  # Assuming Slovak audio file location is in the third column

                # Extract the filename from the audio file location
                slovak_filename = slovak_audio_file.split("file:///")[1].replace("]", "")

                # Create unique filenames with 4-digit formatting and words
                english_filename = f"{str(i+1).zfill(4)}"  # Only use the 4-digit number

                # Synthesize and save the English audio (no speed control)
                english_file_path = synthesize_english(english_text, english_filename)

                # Write to the new CSV file
                writer.writerow([english_text, english_file_path, slovak_filename])

    # Combine the audio files using FFmpeg
    combine_audio_files(category, output_csv_file)

    print(f"Translation and audio synthesis complete for {category}!")

category = "Dates"  # Replace with your directory / CSV name (must be the same)
process_csv(category)