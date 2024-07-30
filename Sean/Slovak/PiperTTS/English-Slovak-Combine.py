import piper
import csv
import os
import subprocess
import time
#trying to create a single audio file for all the vocabulary, repeat x3 times the slovak with a 1 second delay,
# then the English part and save as one file, will work on this tommorrow
#tried to make a playlist, but I'm using a 15 year old sony vaio (nihon sei) with lubuntu as a media player, so it lags
#some words don't even get played by the time the next one get's put in the qeue

# Define the voices
english_voice = "en_US-lessac-medium"
slovak_voice = "sk_SK-lili-medium"  # Assuming you have a Slovak model named 'sk_SK-lili-medium'

# Define the CSV file paths, testing with 'slovak10.csv' before 'slovak1000.csv'
def get_csv_paths(category):
    input_csv_file = f"/media/sean/MusIX/Piper/Slovak/{category}/{category}.csv"  # Replace with your input CSV file path
    return input_csv_file

# Function to synthesize audio and return the data
def synthesize_audio(text, voice, output_dir, filename):
    # Use subprocess to run the piper command
    process = subprocess.run(
        [
            "piper",
            "-m",
            f"/media/sean/MusIX/Piper/{voice}.onnx",  # Replace with the path to your model
            "-c",
            f"/media/sean/MusIX/Piper/{voice}.onnx.json",  # Replace with the path to your config
            "-f",
            os.path.join(output_dir, filename + ".wav"),  # Save to output_dir
            # "-s",  # Remove the speaker argument as it's not needed
            "--sentence-silence",
            "0.5", # Add a 0.5 second silence between sentences
        ],
        input=text.encode("utf-8"),
        capture_output=True,  # Capture the output
    )
    if process.returncode == 0:
        print(f"{voice} audio saved to {os.path.join(output_dir, filename + '.wav')}")
        return process.stdout  # Return the audio data
    else:
        print(f"Error synthesizing {voice} audio: {process.stderr.decode('utf-8')}")
        return None

# Main function to process the CSV
def process_csv(category, output_filename):  # Add output_filename parameter
    input_csv_file = get_csv_paths(category)  # Get only the input CSV path
    output_dir = os.path.dirname(input_csv_file)  # Get the directory of the CSV

    with open(input_csv_file, 'r', encoding='utf-8') as csvfile, open(os.path.join(output_dir, output_filename), 'wb') as outfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row (if any)

        for i, row in enumerate(reader):
            slovak_text = row[0].strip()
            english_text = row[1].strip()

            # Synthesize and save the Slovak audio three times with a delay
            for _ in range(3):
                audio_data = synthesize_audio(slovak_text, slovak_voice, output_dir, f"{str(i+1).zfill(4)}{slovak_text.replace(' ', '')}")
                if audio_data:
                    outfile.write(audio_data)
                    time.sleep(1)  # 1-second delay

            # Synthesize and save the English audio
            audio_data = synthesize_audio(english_text, english_voice, output_dir, f"{str(i+1).zfill(4)}{english_text.replace(' ', '')}")
            if audio_data:
                outfile.write(audio_data)

    print(f"Translation and audio synthesis complete for {category}!")

# Example usage:
category = "Numbers"  # Replace with your directory / CSV name (must be the same)
output_filename = "combined_audio.wav"  # Change this to your desired filename
process_csv(category, output_filename)