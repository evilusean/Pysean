import os
import subprocess

category = "Numbers"
slovak_audio_dir = f"/media/sean/MusIX/Piper/Slovak/{category}/Slovak"
english_audio_dir = f"/media/sean/MusIX/Piper/Slovak/{category}/English"
output_dir = os.path.join(f"/media/sean/MusIX/Piper/Slovak/{category}/", "x3")

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

# Get the list of .mp3 files for Slovak and English
slovak_mp3_files = get_files_from_path(slovak_audio_dir, ext=".mp3")
english_mp3_files = get_files_from_path(english_audio_dir, ext=".mp3")

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Create a temporary file to store the file list
temp_file = os.path.join(output_dir, "temp_concat_list.txt")

# Write the file list to the temporary file
with open(temp_file, "w") as f:
    for i in range(len(slovak_mp3_files)):
        f.write(f"file '{slovak_mp3_files[i]}'\n")
        f.write(f"file '{slovak_mp3_files[i]}'\n")
        f.write(f"file '{slovak_mp3_files[i]}'\n")
        f.write(f"file '{english_mp3_files[i]}'\n")  # Add the English file

# Construct the FFmpeg command
output_file = os.path.join(output_dir, f"{category}_Combined.mp3")
ffmpeg_command = [
    "ffmpeg",
    "-f",
    "concat",
    "-safe",
    "0",
    "-i",
    temp_file,
    "-filter_complex",
    "[0:a]adelay=1000|1000[slovak1];"
    "[slovak1]adelay=1000|1000[slovak2];"
    "[slovak2]adelay=1000|1000[out]",
    "-map",
    "[out]",
    "-c:a",
    "libmp3lame",
    output_file,
]

# Run the FFmpeg command with error handling
try:
    subprocess.run(ffmpeg_command)
    print(f"Combined files saved to {output_file}")
except subprocess.CalledProcessError as e:
    print(f"Error processing files: {e}")
    print(f"Check the contents of '{temp_file}' for correct formatting.")

# Delete the temporary file
os.remove(temp_file)