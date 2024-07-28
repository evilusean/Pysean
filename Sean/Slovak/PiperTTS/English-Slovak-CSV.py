import piper
import csv
import os

# Define the voices
english_voice = "en_US-lessac-medium"
slovak_voice = "sk_SK-lili-medium"  # Assuming you have a Slovak model named 'sk_SK-lili-medium'

# Define the output directories for Slovak and English audio files
slovak_audio_dir = "/media/sean/MusIX/Piper/TransLaSean/Slovak"
english_audio_dir = "/media/sean/MusIX/Piper/TransLaSean/English"

# Create the directories if they don't exist
os.makedirs(slovak_audio_dir, exist_ok=True)
os.makedirs(english_audio_dir, exist_ok=True)

# Define the CSV file path
csv_file = "/media/sean/MusIX/Piper/Slovak/translation_data.csv"

# Function to synthesize and save Slovak audio
def synthesize_slovak(text, filename):
    audio_data = piper.synthesize(text, slovak_voice)
    audio_path = os.path.join(slovak_audio_dir, filename + ".mp3")  # Save as .mp3
    with open(audio_path, "wb") as outfile:
        outfile.write(audio_data)
    print(f"Slovak audio saved to {audio_path}")

# Function to synthesize and save English audio
def synthesize_english(text, filename):
    audio_data = piper.synthesize(text, english_voice)
    audio_path = os.path.join(english_audio_dir, filename + ".mp3")  # Save as .mp3
    with open(audio_path, "wb") as outfile:
        outfile.write(audio_data)
    print(f"English audio saved to {audio_path}")

# Function to write to the CSV
def write_to_csv(english_text, slovak_text, filename):
    with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([english_text, filename, f"[sound:file://{os.path.join(slovak_audio_dir, filename + '.mp3')}]"])  
        # Update CSV link to .mp3

# Example usage:
english_lines = [
    "Hello, world!",
    "This is a test.",
    "How are you?",
    # ... add more English lines here
]

slovak_lines = [
    "Dobrý deň!",
    "Toto je test.",
    "Ako sa máš?",
    # ... add more Slovak lines here
]

# Loop through the English lines
for i, (english_text, slovak_text) in enumerate(zip(english_lines, slovak_lines)):
    # Create a unique filename with 4-digit formatting
    filename = f"{str(i+1).zfill(4)}"  # Pad with zeros to get 4-digit format

    # Synthesize and save the Slovak audio
    synthesize_slovak(slovak_text, filename)

    # Synthesize and save the English audio
    synthesize_english(english_text, filename)

    # Write to the CSV
    write_to_csv(english_text, slovak_text, filename)

print("Translation and audio synthesis complete!")

# Commented out the ffmpeg command to combine audio files
# ffmpeg -f concat -i <(for f in *.wav; do echo "file '$f'"; done) -c copy combined_slovak.wav
