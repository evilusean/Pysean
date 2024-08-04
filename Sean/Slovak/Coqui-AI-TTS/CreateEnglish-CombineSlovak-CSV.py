import os
import subprocess
import csv
import shutil

# Define the voices
english_voice = "tts_models/en/ljspeech/vits"
pause = "/media/sean/MusIX/Piper/silent_half-second.mp3"

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

def convert_to_mp3(input_file, output_file):
    subprocess.run([
        "ffmpeg",
        "-i", input_file,
        "-codec:a", "libmp3lame",
        "-qscale:a", "2",  # Adjust quality (2 is a good balance between size and quality)
        output_file
    ])

def combine_audio_files(category, csv_file):
    global pause
    output_dir = "/media/sean/MusIX/Coqui-AI/Slovak/1VocabLists"
    os.makedirs(output_dir, exist_ok=True)

    temp_file = os.path.join(output_dir, "temp_concat_list.txt")

    ffmpeg_command = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", temp_file,
        "-c:a", "libmp3lame",  # Use MP3 codec for output
        os.path.join(output_dir, f"{category}_combined.mp3"),
        "-loglevel", "error",
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
                    slovak_file = slovak_file[14:].rstrip(']')
                
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

    # Run FFmpeg and check for errors
    result = subprocess.run(ffmpeg_command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FFmpeg Error:\n{result.stderr}")
    else:
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

                # Convert English audio to MP3
                mp3_english_file_path = os.path.join(english_audio_dir, english_filename + ".mp3")
                convert_to_mp3(english_file_path, mp3_english_file_path)

                # Ensure the Slovak file exists before copying and converting
                if os.path.isfile(slovak_audio_file):
                    slovak_mp3_path = os.path.join(slovak_audio_dir, slovak_filename + ".mp3")
                    if not os.path.isfile(slovak_mp3_path):
                        convert_to_mp3(slovak_audio_file, slovak_mp3_path)
                else:
                    print(f"Warning: Slovak audio file not found: {slovak_audio_file}")

                writer.writerow([english_text, mp3_english_file_path, f"/media/sean/MusIX/Slovak.Czech/slovake.eu-audio/{category}/Slovak/{slovak_filename}.mp3"])

    combine_audio_files(category, output_csv_file)
    print(f"Translation and audio synthesis complete for {category}!")

category = "Dates"  # Replace with your directory / CSV name (must be the same)
process_csv(category)