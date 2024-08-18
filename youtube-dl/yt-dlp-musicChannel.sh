#!/bin/bash

# Replace these placeholders with your actual values
channel_url="https://www.youtube.com/@PouyaOfficial/videos"
output_folder="/mnt/sdb2/Media/Music/1Youtube" #removed final '/' slash, was causing issues with metadata
subfolder_name="Pouya"

# Create an array to store the temporary file names
temp_files=()
image_files=()  

# Get the list of videos from the channel
yt-dlp --flat-playlist --yes-playlist --get-id "$channel_url" | while read video_id; do
  # Check if the MP3 file already exists
  if [ -f "$output_folder/$subfolder_name/${video_id}.mp3" ]; then
    echo "Skipping video ID: $video_id (MP3 file already exists)"
    continue  # Skip to the next video
  fi  

  # Download the MP3 directly with higher quality
  yt-dlp -o "$output_folder/$subfolder_name/%(id)s.mp3" \
    --extract-audio \
    --audio-format mp3 \
    --audio-quality 0 \
    --embed-thumbnail \
    --add-metadata \
    --write-info-json \
    "$video_id"

  # Check if the info.json file exists
  if [ ! -f "$output_folder/$subfolder_name/${video_id}.info.json" ]; then
    echo "Error: Could not download metadata for video ID: $video_id"
    continue  # Skip to the next video
  fi

  # --- START OF REPEATABLE BLOCK ---
  # Extract upload date from the info.json file
  upload_date=$(jq -r '.upload_date' "$output_folder/$subfolder_name/${video_id}.info.json")
  upload_date=$(date -r "$upload_date" +"%Y-%m-%d")

  # Extract artist and song name from the title
  title=$(jq -r '.title' "$output_folder/$subfolder_name/${video_id}.info.json")
  artist=$(echo "$title" | awk -F' - ' '{print $1}')
  song_name=$(echo "$title" | awk -F' - ' '{print $2}')

  # If no dash found, use the entire title as the song name
  if [ -z "$song_name" ]; then
    song_name="$title"
    artist=""
  fi

  # Create a consistent filename
  filename="${artist} - ${song_name}.mp3"
  filename=$(echo "$filename" | sed 's/[^a-zA-Z0-9\-_\.]//g')  # Remove invalid characters

  # Update the album metadata in the info.json file
  jq --arg album "Youtube - Uploaded: $upload_date" '.album = $album' \
    "$output_folder/$subfolder_name/${video_id}.info.json" > \
    "$output_folder/$subfolder_name/${video_id}.info.json.tmp" && \
    mv "$output_folder/$subfolder_name/${video_id}.info.json.tmp" \
    "$output_folder/$subfolder_name/${video_id}.info.json"

  # Store the temporary file name in the array
  temp_files+=("$output_folder/$subfolder_name/${video_id}.info.json.tmp")
  temp_files+=("$output_folder/$subfolder_name/${video_id}.info.json") # Add the original .info.json file

  # Store the image file name in the array
  image_files+=("$output_folder/$subfolder_name/${video_id}.jpg")

  # Embed metadata and thumbnail into the MP3 file
  # Use the video ID for the MP3 filename to avoid issues with spaces
  ffmpeg -i "$output_folder/$subfolder_name/${video_id}.mp3" \
    -metadata title="$title" \
    -metadata artist="$artist" \
    -metadata album="Youtube - Uploaded: $upload_date" \
    -i "$output_f         older/$subfolder_name/${video_id}.jpg" \
    -map 0:a -map 1:v -c:v copy -c:a copy \
    "$output_folder/$subfolder_name/${video_id}.mp3"
  # --- END OF REPEATABLE BLOCK ---

done

# Delete all temporary files after the loop
for temp_file in "${temp_files[@]}"; do
  rm "$temp_file"
done

# Delete all image files after the loop
for image_file in "${image_files[@]}"; do
  rm "$image_file"
done