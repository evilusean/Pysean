import os
import subprocess
import csv
import shutil

#created a script that combined the naturally spoken slovak I downloaded as individual MP3's, which then
#creates an english version from the CSV I used for ANKI, and combines the natural slovak with AI english into a vocabulary list
#keep getting below error :
# [concat @ 0x591cfeb16840] Impossible to open '/media/sean/MusIX/Coqui-AI/Slovak/1VocabLists/media/sean/MusIX/Slovak.Czech/slovake.eu-audio/Dates/január' /media/sean/MusIX/Coqui-AI/Slovak/1VocabLists/temp_concat_list.txt: No such file or directory
#[concat @ 0x59eef205d880] Impossible to open 'pipe:/media/sean/MusIX/Slovak.Czech/slovake.eu-audio/Dates/English/0001.wav'pipe:0: Invalid data found when processing input

# Define the voices
english_voice = "tts_models/en/ljspeech/vits"
pause = "/media/sean/MusIX/Piper/silent_half-second.wav"

def get_audio_dirs(category):
    english_audio_dir = f"/media/sean/MusIX/Slovak.Czech/slovake.eu-audio/{category}/English"
    slovak_audio_dir = f"/media/sean/MusIX/Slovak.Czech/slovake.eu-audio/{category}/Slovak"
    return english_audio_dir, slovak_audio_dir

def create_dirs(category):
    global english_audio_dir, slovak_audio_dir
    english_audio_dir, slovak_audio_dir = get_audio_dirs(category)
    os.makedirs(english_audio_dir, exist_ok=True)
    os.makedirs(slovak_audio_dir, exist_ok=True)

def synthesize_english(text, filename):
    global english_audio_dir
    out_path = os.path.join(english_audio_dir, filename + ".wav")
    subprocess.run(
        [
            "tts",
            "--text",
            text,
            "--model_name",
            english_voice,
            "--out_path",
            out_path,
        ],
    )
    print(f"English audio saved to {out_path}")
    return out_path

def combine_audio_files(category, csv_file):
    global pause
    output_dir = "/media/sean/MusIX/Coqui-AI/Slovak/1VocabLists"
    os.makedirs(output_dir, exist_ok=True)

    temp_file = os.path.join(output_dir, "temp_concat_list.txt")

    ffmpeg_command = [
        "ffmpeg",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        temp_file,
        "-filter_complex",
        "[0:a]asetpts=PTS-STARTPTS[out]",
        "-map",
        "[out]",
        "-c:a",
        "libmp3lame",
        os.path.join(output_dir, f"{category}_combined.mp3"),
        "-loglevel",
        "error",
    ]

    # Write the file list to the temporary file
    with open(temp_file, "w") as f:
        with open(csv_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row

            for row in reader:
                english_file = row[1].strip()
                slovak_file = row[2].strip()

                # Handle URLs for Slovak audio files
                if slovak_file.startswith("[sound:file:///"):
                    slovak_file = slovak_file[16:].rstrip(']')
                
                # Ensure the paths are correctly formatted
                english_file = os.path.abspath(english_file)
                slovak_file = os.path.abspath(slovak_file)

                # Log the paths being written to the temp file
                print(f"Adding to temp file: {english_file}")
                print(f"Adding pause: {pause}")
                print(f"Adding Slovak file: {slovak_file}")
                
                f.write(f"file '{english_file}'\n")
                f.write(f"file '{pause}'\n")
                f.write(f"file '{slovak_file}'\n")
                f.write(f"file '{pause}'\n")

    # Print the contents of the temp file for review
    with open(temp_file, 'r') as f:
        print("\nContents of temp_concat_list.txt:")
        print(f.read())

    subprocess.run(ffmpeg_command)
    print(f"Audio files combined into {category}_combined.mp3 in {output_dir}")
    os.remove(temp_file)

def process_csv(category):
    input_csv_file = f"/media/sean/MusIX/Slovak.Czech/slovake.eu-audio/{category}/{category}.csv"
    create_dirs(category)

    output_csv_file = f"/media/sean/MusIX/Slovak.Czech/slovake.eu-audio/{category}/{category}_combined_audio.csv"
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["English Text", "English Audio", "Slovak Audio"])

        with open(input_csv_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)

            for i, row in enumerate(reader):
                english_text = row[0].strip()
                slovak_audio_file = row[2].strip()

                # Remove '[sound:file:///' prefix and trailing ']'
                if slovak_audio_file.startswith("[sound:file:///"):
                    slovak_audio_file = slovak_audio_file[14:].rstrip(']')

                # Ensure that the full path is correctly formed
                slovak_audio_file = os.path.abspath(slovak_audio_file)

                # Extract the filename from the audio file path
                slovak_filename = os.path.splitext(os.path.basename(slovak_audio_file))[0]

                english_filename = f"{str(i+1).zfill(4)}"

                english_file_path = synthesize_english(english_text, english_filename)

                # Ensure the Slovak file exists before copying
                if os.path.isfile(slovak_audio_file):
                    shutil.copyfile(slovak_audio_file, os.path.join(slovak_audio_dir, slovak_filename + ".mp3"))
                else:
                    print(f"Warning: Slovak audio file not found: {slovak_audio_file}")

                writer.writerow([english_text, english_file_path, f"/media/sean/MusIX/Slovak.Czech/slovake.eu-audio/{category}/Slovak/{slovak_filename}.mp3"])

    combine_audio_files(category, output_csv_file)
    print(f"Translation and audio synthesis complete for {category}!")

category = "Dates"  # Replace with your directory / CSV name (must be the same)
process_csv(category)