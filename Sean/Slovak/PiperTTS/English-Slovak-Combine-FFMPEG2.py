import os
import subprocess

slovak_audio_dir = "/media/sean/MusIX/Piper/Slovak/Numbers/Slovak"
output_dir = "/media/sean/MusIX/Piper/Slovak/Numbers/3x"  # Output directory

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

# Get the list of .wav files for Slovak
slovak_wav_files = get_files_from_path(slovak_audio_dir, ext=".wav")

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterate through each Slovak file
for i, slovak_file in enumerate(slovak_wav_files):
    print(f"Processing file: {slovak_file}")  # Print the file path for debugging

    # Construct the FFmpeg command
    output_file = os.path.join(output_dir, f"{os.path.basename(slovak_file).replace('.wav', '_repeated.mp3')}")
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
        "libmp3lame",  # Use the MP3 codec (libmp3lame)
        output_file,
    ]

    # Run the FFmpeg command with error handling
    try:
        subprocess.run(ffmpeg_command)
        print(f"Audio file repeated and saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing file {slovak_file}: {e}")