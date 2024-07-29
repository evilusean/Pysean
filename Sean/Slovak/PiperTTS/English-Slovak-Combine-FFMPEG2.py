import os
import subprocess

category = "Numbers"
slovak_audio_dir = f"/media/sean/MusIX/Piper/Slovak/{category}/Slovak"
slovak_file = os.path.join(slovak_audio_dir, "0001dva.wav")
output_file = os.path.join(slovak_audio_dir, "0001dva_repeated.wav")

# Construct the FFmpeg command
ffmpeg_command = [
    "ffmpeg",
    "-f",
    "concat",
    "-safe",
    "0",
    "-i",
    f"concat:{slovak_file}|{slovak_file}|{slovak_file}",  # Concatenate the file 3 times
    "-filter_complex",
    "[0:a]adelay=1000|1000[slovak1];"
    "[slovak1]adelay=1000|1000[slovak2];"
    "[slovak2]adelay=1000|1000[out]",
    "-map",
    "[out]",
    "-c:a",
    "copy",
    output_file,
]

# Run the FFmpeg command
subprocess.run(ffmpeg_command)

print(f"Audio file repeated and saved to {output_file}")