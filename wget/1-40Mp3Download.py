import os
import wget

# Base URL of the website
base_url = "https://slovake.eu"

# Path to the directory where you want to save the files
download_dir = "/media/sean/MusIX/Slovak.Czech/slovake.eu-audio/ABECEDA"


# Create the download directory if it doesn't exist
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Loop through sound files 1-40
for i in range(1, 41):
    # Construct the URL for the current sound file
    file_url = f"{base_url}/sounds/pronunciation/mp3/sound{i}_lit.mp3"

    # Download the file using wget
    wget.download(file_url, out=os.path.join(download_dir, f"sound{i}_lit.mp3"))

    # Print a message to indicate the download is complete
    print(f"Downloaded sound{i}_lit.mp3")

print("All sound files downloaded successfully!")