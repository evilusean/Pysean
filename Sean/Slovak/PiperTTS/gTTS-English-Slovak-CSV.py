import gTTS
import csv
import os

# Define the voices
english_voice = "en-US"  # English voice
slovak_voice = "sk"  # Slovak voice

# Define the output directories for Slovak and English audio files
slovak_audio_dir = "/media/sean/MusIX/Piper/TestWords/Slovak"
english_audio_dir = "/media/sean/MusIX/Piper/TestWords/English"

# Create the directories if they don't exist
os.makedirs(slovak_audio_dir, exist_ok=True)
os.makedirs(english_audio_dir, exist_ok=True)

# Define the CSV file paths, testing with 'slovak10.csv' before 'slovak1000.csv'
input_csv_file = "/media/sean/MusIX/Piper/TestWords/slovak10.csv"  # Replace with your input CSV file path
output_csv_file = "/media/sean/MusIX/Piper/TestWords/slovak10_anki.csv"

# Function to synthesize and save Slovak audio
def synthesize_slovak(text, filename):
    tts = gTTS(text=text, lang=slovak_voice)
    audio_path = os.path.join(slovak_audio_dir, filename + ".mp3")  # Save as .mp3
    tts.save(audio_path)
    print(f"Slovak audio saved to {audio_path}")

# Function to synthesize and save English audio
def synthesize_english(text, filename):
    tts = gTTS(text=text, lang=english_voice)
    audio_path = os.path.join(english_audio_dir, filename + ".mp3")  # Save as .mp3
    tts.save(audio_path)
    print(f"English audio saved to {audio_path}")

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
