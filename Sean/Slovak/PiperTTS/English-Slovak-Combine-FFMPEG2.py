import os
import subprocess

slovak_audio_dir = "/media/sean/MusIX/Piper/Slovak/Numbers/Slovak"
slovak_file = os.path.join(slovak_audio_dir, "0001dva.wav")
output_file = os.path.join(slovak_audio_dir, "0001dva_repeated.mp3")  # Change to .mp3

# Create a temporary file to store the file list
temp_file = os.path.join(slovak_audio_dir, "temp_concat_list.txt")

# Write the file list to the temporary file
with open(temp_file, "w") as f:
    f.write(f"file '{slovak_file}'\n")
    f.write(f"file '{slovak_file}'\n")
    f.write(f"file '{slovak_file}'\n")

# Construct the FFmpeg command
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
    print(f"Audio file repeated and saved to {output_file}")
except subprocess.CalledProcessError as e:
    print(f"Error processing file {slovak_file}: {e}")

# Delete the temporary file
os.remove(temp_file)