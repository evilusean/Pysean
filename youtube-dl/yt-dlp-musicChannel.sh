#!/bin/bash

# Replace these placeholders with your actual values
channel_url="https://www.youtube.com/@irvingforce/videos"
output_folder="/mnt/sdb2/Media/Music/1Youtube/"
subfolder_name="IrvingForce"

# Create an array to store the temporary file names
temp_files=()

# Get the list of videos from the channel
yt-dlp --flat-playlist --yes-playlist --get-id "$channel_url" | while read video_id; do
  # Download the video with metadata
  yt-dlp -o "$output_folder/$subfolder_name/%(title)s - %(id)s.%(ext)s" \
    --embed-thumbnail \
    --add-metadata \
    --write-info-json \
    "$video_id"

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

  # Update the album metadata in the info.json file
  jq --arg album "Youtube - Uploaded: $upload_date" '.album = $album' \
    "$output_folder/$subfolder_name/${video_id}.info.json" > \
    "$output_folder/$subfolder_name/${video_id}.info.json.tmp" && \
    mv "$output_folder/$subfolder_name/${video_id}.info.json.tmp" \
    "$output_folder/$subfolder_name/${video_id}.info.json"

  # Store the temporary file name in the array
  temp_files+=("$output_folder/$subfolder_name/${video_id}.info.json.tmp")

  # Convert to MP3
  ffmpeg -i "$output_folder/$subfolder_name/${video_id}.%(ext)s" \
    -vn -acodec libmp3lame -ab 192k \
    "$output_folder/$subfolder_name/${video_id}.mp3"

  # Embed metadata and thumbnail into the MP3 file
  ffmpeg -i "$output_folder/$subfolder_name/${video_id}.mp3" \
    -metadata title="$title" \
    -metadata artist="$artist" \
    -metadata album="Youtube - Uploaded: $upload_date" \
    -i "$output_folder/$subfolder_name/${video_id}.jpg" \
    -map 0:a -map 1:v -c:v copy -c:a copy \
    "$output_folder/$subfolder_name/${video_id}.mp3"

  # Remove the original video file
  rm "$output_folder/$subfolder_name/${video_id}.%(ext)s"
done

# Delete all temporary files after the loop
for temp_file in "${temp_files[@]}"; do
  rm "$temp_file"
done