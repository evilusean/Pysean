#!/bin/bash

# Input YouTube video URL
video_url="https://www.youtube.com/watch?v=YOUR_VIDEO_ID"

# Output folder
output_folder="/path/to/your/output/folder"

# Extract video ID from the URL
video_id=$(youtube-dl --get-id "$video_url")

# Download the transcript as a text file
yt-dlp -o "$output_folder/%(id)s.txt" --write-sub --sub-format vtt "$video_url"

# Convert the VTT file to plain text (optional)
# This will remove the timing information and just keep the text
# You can use other tools like 'ffmpeg' or 'vtt2txt' if you prefer
# vtt2txt is a command-line tool that can be installed with 'pip install vtt2txt'
vtt2txt "$output_folder/$video_id.vtt" > "$output_folder/$video_id.txt"

echo "Downloaded transcript to: $output_folder/$video_id.txt"
