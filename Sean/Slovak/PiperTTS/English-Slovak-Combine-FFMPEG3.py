import os
import subprocess

category = "Numbers"
slovak_audio_dir = f"/media/sean/MusIX/Piper/Slovak/{category}/Slovak"
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

# Get the list of .wav files for Slovak
slovak_wav_files = get_files_from_path(slovak_audio_dir, ext=".wav")

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# List to store combined file names
combined_files = []

# Iterate through each Slovak file
for i, slovak_file in enumerate(slovak_wav_files):
    print(f"Processing file: {slovak_file}")  # Print the file path for debugging

    # Create a temporary file to store the file list
    temp_file = os.path.join(output_dir, f"temp_concat_list_{i+1:04d}.txt")

    # Write the file list to the temporary file
    with open(temp_file, "w") as f:
        f.write(f"file '{slovak_file}'\n")
        f.write(f"file '{slovak_file}'\n")
        f.write(f"file '{slovak_file}'\n")

    # Construct the FFmpeg command
    output_file = os.path.join(output_dir, f"{category}_{i+1:04d}_Combined.wav")
    ffmpeg_command = [
        "ffmpeg",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        temp_file,  # Use the temporary file as input
        "-c:a",
        "copy",
        output_file,
    ]

    # Run the FFmpeg command with error handling
    try:
        subprocess.run(ffmpeg_command)
        combined_files.append(output_file)
    except subprocess.CalledProcessError as e:
        print(f"Error processing file {slovak_file}: {e}")

    # Delete the temporary file
    os.remove(temp_file)

# Print the list of combined files
print("Combined Files:")
for file in combined_files:
    print(file)