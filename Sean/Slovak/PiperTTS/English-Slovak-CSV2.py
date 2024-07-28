import piper
import csv
import os
import subprocess

# Define the voices
english_voice = "en_US-lessac-medium"
slovak_voice = "sk_SK-lili-medium"  # Assuming you have a Slovak model named 'sk_SK-lili-medium'

# Define the output directories for Slovak and English audio files
slovak_audio_dir = "/media/sean/MusIX/Piper/Slovak/Basic/Slovak"
english_audio_dir = "/media/sean/MusIX/Piper/Slovak/Basic/English"

# Create the directories if they don't exist
os.makedirs(slovak_audio_dir, exist_ok=True)
os.makedirs(english_audio_dir, exist_ok=True)

# Define the CSV file paths, testing with 'slovak10.csv' before 'slovak1000.csv'
input_csv_file = "/media/sean/MusIX/Piper/Slovak/Basic/Basic.csv"  # Replace with your input CSV file path
output_csv_file = "/media/sean/MusIX/Piper/Slovak/Basic/Basic_anki.csv"

# Function to synthesize and save Slovak audio
def synthesize_slovak(text, filename):
    # Use subprocess to run the piper command
    subprocess.run(
        [
            "piper",
            "-m",
            "/media/sean/MusIX/Piper/sk_SK-lili-medium.onnx",  # Replace with the path to your Slovak model
            "-c",
            "/media/sean/MusIX/Piper/sk_SK-lili-medium.onnx.json",  # Replace with the path to your Slovak config
            "-f",
            os.path.join(slovak_audio_dir, filename + ".mp3"),
            # "-s",  # Remove the speaker argument as it's not needed
            "--sentence-silence",
            "0.5", # Add a 0.5 second silence between sentences
        ],
        input=text.encode("utf-8"),
    )
    print(f"Slovak audio saved to {os.path.join(slovak_audio_dir, filename + '.mp3')}")

# Function to synthesize and save English audio
def synthesize_english(text, filename):
    # Use subprocess to run the piper command
    subprocess.run(
        [
            "piper",
            "-m",
            "/media/sean/MusIX/Piper/en_US-lessac-medium.onnx",  # Replace with the path to your English model
            "-c",
            "/media/sean/MusIX/Piper/en_US-lessac-medium.onnx.json",  # Replace with the path to your English config
            "-f",
            os.path.join(english_audio_dir, filename + ".mp3"),
            # "-s",  # Remove the speaker argument as it's not needed
            "--sentence-silence",
            "0.5",  # Add a 0.5 second silence between sentences
        ],
        input=text.encode("utf-8"),
    )
    print(f"English audio saved to {os.path.join(english_audio_dir, filename + '.mp3')}")

# Function to write to the CSV
def write_to_csv(english_text, slovak_text, slovak_filename, english_filename):
    with open(output_csv_file, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([english_text, slovak_text, f"[sound:file://{os.path.join(slovak_audio_dir, slovak_filename + '.mp3')}]"])  
        # Update CSV link to .mp3

# Process the input CSV file
with open(input_csv_file, 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row (if any)

    for i, row in enumerate(reader):
        slovak_text = row[0].strip()
        english_text = row[1].strip()

        # Create unique filenames with 4-digit formatting and words
        slovak_filename = f"{str(i+1).zfill(4)}{slovak_text.replace(' ', '')}"
        english_filename = f"{str(i+1).zfill(4)}{english_text.replace(' ', '')}"

        # Synthesize and save the Slovak audio
        synthesize_slovak(slovak_text, slovak_filename)

        # Synthesize and save the English audio
        synthesize_english(english_text, english_filename)

        # Write to the CSV
        write_to_csv(english_text, slovak_text, slovak_filename, english_filename)

print("Translation and audio synthesis complete!")

# Commented out the ffmpeg command to combine audio files
# ffmpeg -f concat -i <(for f in *.wav; do echo "file '$f'"; done) -c copy combined_slovak.wav
