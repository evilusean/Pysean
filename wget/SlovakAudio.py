import os
import wget
import re
import csv
#This script, should find the sound file, from an inspected element, get the URL, download the .mp3, and save that data to a .CSV
#I should be able to just 'inspect' -> 'copy' -> 'paste' an element I see on the page, to download an MP3 for ANKI deck

# Base URL of the website
base_url = "https://slovake.eu"

# Path to the directory where you want to save the files
download_dir = "/media/sean/MusIX/Slovak.Czech/slovake.eu-audio/Introductions"

# Path to the CSV file
csv_file = "/media/sean/MusIX/Slovak.Czech/slovake.eu-audio/Introductions/Introductions.csv"

# Function to extract the data-sound URL from a span tag
def extract_sound_url(span_tag):
    match = re.search(r'data-sound="([^"]+)"', span_tag)
    if match:
        return match.group(1)
    else:
        return None

# Function to download the sound file and add to CSV
def download_sound(sound_url, filename):
    file_url = f"{base_url}{sound_url}"
    wget.download(file_url, out=os.path.join(download_dir, filename))
    print(f"Downloaded {filename}")

    # Add filename and location to CSV in the desired format
    with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["", filename, f"[sound:file://{os.path.join(download_dir, filename)}]"])

# Create the download directory if it doesn't exist
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Example usage:
# Assuming you have the HTML content in a variable called 'html_content'
html_content = """
<span id="sound_yw381722641002" class="sound" data-sound="/sounds/phrases/introduction/mp3/sound19.mp3">
        <span class="glyphicon glyphicon-volume-up"></span>
        <span class="orig">A vy?</span>
    </span>
"""

# Extract the data-sound URL
sound_url = extract_sound_url(html_content)

# Download the sound file and add to CSV
if sound_url:
    filename = os.path.basename(sound_url)
    download_sound(sound_url, filename)