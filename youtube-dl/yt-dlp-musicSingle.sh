#!/bin/bash

# Input YouTube video URL
video_url="https://www.youtube.com/watch?v=fvEZ7OGwitU"

# Output folder
output_folder="/mnt/sdb2/Media/Music/1S1ngles"

# Check if both arguments are provided
if [ -z "$video_url" ] || [ -z "$output_folder" ]; then
  echo "Usage: $0 <video_url> <output_folder>"
  exit 1
fi

# Extract video ID from the URL
video_id=$(youtube-dl --get-id "$video_url")

# Create an array to store temporary file names
temp_files=()
image_files=()

# Download the MP3 directly with higher quality
yt-dlp -o "$output_folder/%(id)s.mp3" \
  --extract-audio \
  --audio-format mp3 \
  --audio-quality 0 \
  --embed-thumbnail \
  --add-metadata \
  --write-info-json \
  "$video_url"

# Check if the info.json file exists
if [ ! -f "$output_folder/${video_id}.info.json" ]; then
  echo "Error: Could not download metadata for video ID: $video_id"
  exit 1
fi

# Extract upload date from the info.json file
upload_date=$(jq -r '.upload_date' "$output_folder/${video_id}.info.json")
upload_date=$(date -r "$upload_date" +"%Y-%m-%d")

# Extract artist and song name from the title
title=$(jq -r '.title' "$output_folder/${video_id}.info.json")
artist=$(echo "$title" | awk -F' - ' '{print $1}')
song_name=$(echo "$title" | awk -F' - ' '{print $2}')

# If no dash found, use the entire title as the song name
if [ -z "$song_name" ]; then
  song_name="$title"
  artist=""
fi

# Create a consistent filename
filename="${artist} - ${song_name}.mp3"
filename=$(echo "$filename" | sed 's/[^a-zA-Z0-9\-_\.]//g')

# Update the album metadata in the info.json file
jq --arg album "Youtube - Uploaded: $upload_date" '.album = $album' \
  "$output_folder/${video_id}.info.json" > \
  "$output_folder/${video_id}.info.json.tmp" && \
  mv "$output_folder/${video_id}.info.json.tmp" \
  "$output_folder/${video_id}.info.json"

# Store temporary file names
temp_files+=("$output_folder/${video_id}.info.json.tmp")
temp_files+=("$output_folder/${video_id}.info.json")
image_files+=("$output_folder/${video_id}.jpg")

# Embed metadata and thumbnail into the MP3 file
ffmpeg -i "$output_folder/${video_id}.mp3" \
  -metadata title="$title" \
  -metadata artist="$artist" \
  -metadata album="Youtube - Uploaded: $upload_date" \
  -i "$output_folder/${video_id}.jpg" \
  -map 0:a -map 1:v -c:v copy -c:a copy \
  "$output_folder/${filename}"

# Delete temporary files
for temp_file in "${temp_files[@]}"; do
  rm "$temp_file"
done

# Delete image files
for image_file in "${image_files[@]}"; do
  rm "$image_file"
done

echo "Downloaded and embedded metadata for: $filename"
