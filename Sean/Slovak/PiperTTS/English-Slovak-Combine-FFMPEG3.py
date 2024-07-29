import os
import subprocess

category = "Numbers"
slovak_audio_dir = f"/media/sean/MusIX/Piper/Slovak/{category}/Slovak"
english_audio_dir = f"/media/sean/MusIX/Piper/Slovak/{category}/English"
output_dir = os.path.join(f"/media/sean/MusIX/Piper/Slovak/{category}/", "x3")  # Define the output directory

def get_files_from_path(path: str = ".", ext=None) -> list:
    result = []
    for subdir, dirs, files in os.walk(path):
        for fname in files:
            filepath = f"{subdir}{os.sep}{fname}"
            if ext == None:
                result.append(filepath)
            elif type(ext) == str and fname.lower().endswith(ext.lower()):
                result.append(filepath)
            elif type(ext) == list:
                for item in ext:
                    if fname.lower().endswith(item.lower()):
                        result.append(filepath)
    return result

# Get the list of .wav files for Slovak and English
slovak_wav_files = get_files_from_path(slovak_audio_dir, ext=".wav")
english_wav_files = get_files_from_path(english_audio_dir, ext=".wav")

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Create a temporary file to store the file list
temp_file = os.path.join(output_dir, "temp_concat_list.txt")

# Write the file list to the temporary file
with open(temp_file, "w") as f:
    for i in range(len(slovak_wav_files)):
        f.write(f"file '{slovak_wav_files[i]}'\n")
        f.write(f"file '{slovak_wav_files[i]}'\n")
        f.write(f"file '{slovak_wav_files[i]}'\n")
        f.write(f"file '{english_wav_files[i]}'\n")  # Add the English file

# Construct the FFmpeg command
output_file = os.path.join(output_dir, f"{category}_Combined.mp3")  # Change to .mp3
ffmpeg_command = [
    "ffmpeg",
    "-f",
    "concat",
    "-safe",
    "0",
    "-i",
    temp_file,  # Use the temporary file as input
    "-filter_complex",
    "[0:a]adelay=1000|1000[slovak1];"
    "[slovak1]adelay=1000|1000[slovak2];"
    "[slovak2]adelay=1000|1000[out]",
    "-map",
    "[out]",
    "-c:a",
    "libmp3lame",  # Use the MP3 codec (libmp3lame)
    output_file,
]

# Run the FFmpeg command with error handling
try:
    subprocess.run(ffmpeg_command)
    print(f"Combined files saved to {output_file}")
except subprocess.CalledProcessError as e:
    print(f"Error processing files: {e}")

# Delete the temporary file
os.remove(temp_file)