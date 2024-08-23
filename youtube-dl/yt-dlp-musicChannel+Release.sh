#!/bin/bash

# Replace these placeholders with your actual values
channel_url="https://www.youtube.com/@witchouse40k/videos"  # This is the "Videos" URL
channel_url_releases="https://www.youtube.com/@witchouse40k/releases"  # This is the "Releases" URL
output_folder="/mnt/sdb2/Media/Music/1Youtube"
subfolder_name="WitchHouse40k"

# Create an array to store the temporary file names
temp_files=()
image_files=()

# Function to download and embed metadata for a single video
download_and_embed_metadata() {
  local video_id="$1"
  local upload_date="$2"
  local title="$3"
  local artist="$4"
  local song_name="$5"

  # Check if the MP3 file already exists
  if [ -f "$output_folder/$subfolder_name/${video_id}.mp3" ]; then
    echo "Skipping video ID: $video_id (MP3 file already exists)"
    return
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
    return
  fi

  # Create a consistent filename
  filename="${artist} - ${song_name}.mp3"
  filename=$(echo "$filename" | sed 's/[^a-zA-Z0-9\-_\.]//g')

  # Update the album metadata in the info.json file
  jq --arg album "Youtube - Uploaded: $upload_date" '.album = $album' \
    "$output_folder/$subfolder_name/${video_id}.info.json" > \
    "$output_folder/$subfolder_name/${video_id}.info.json.tmp" && \
    mv "$output_folder/$subfolder_name/${video_id}.info.json.tmp" \
    "$output_folder/$subfolder_name/${video_id}.info.json"

  # Store temporary file names
  temp_files+=("$output_folder/$subfolder_name/${video_id}.info.json.tmp")
  temp_files+=("$output_folder/$subfolder_name/${video_id}.info.json")
  image_files+=("$output_folder/$subfolder_name/${video_id}.jpg")

  # Embed metadata and thumbnail into the MP3 file
  ffmpeg -i "$output_folder/$subfolder_name/${video_id}.mp3" \
    -metadata title="$title" \
    -metadata artist="$artist" \
    -metadata album="Youtube - Uploaded: $upload_date" \
    -i "$output_folder/$subfolder_name/${video_id}.jpg" \
    -map 0:a -map 1:v -c:v copy -c:a copy \
    "$output_folder/$subfolder_name/${video_id}.mp3"
}

# Download videos from the "Videos" section
yt-dlp --flat-playlist --yes-playlist --get-id "$channel_url" | while read video_id; do
  # Extract upload date and title
  upload_date=$(jq -r '.upload_date' "$output_folder/$subfolder_name/${video_id}.info.json")
  upload_date=$(date -r "$upload_date" +"%Y-%m-%d")
  title=$(jq -r '.title' "$output_folder/$subfolder_name/${video_id}.info.json")
  artist=$(echo "$title" | awk -F' - ' '{print $1}')
  song_name=$(echo "$title" | awk -F' - ' '{print $2}')

  # If no dash found, use the entire title as the song name
  if [ -z "$song_name" ]; then
    song_name="$title"
    artist=""
  fi

  download_and_embed_metadata "$video_id" "$upload_date" "$title" "$artist" "$song_name"
done

# Download videos from the "Releases" section
yt-dlp --flat-playlist --yes-playlist --get-id "$channel_url_releases" | while read video_id; do
  # Extract upload date and title
  upload_date=$(jq -r '.upload_date' "$output_folder/$subfolder_name/${video_id}.info.json")
  upload_date=$(date -r "$upload_date" +"%Y-%m-%d")
  title=$(jq -r '.title' "$output_folder/$subfolder_name/${video_id}.info.json")
  artist=$(echo "$title" | awk -F' - ' '{print $1}')
  song_name=$(echo "$title" | awk -F' - ' '{print $2}')

  # If no dash found, use the entire title as the song name
  if [ -z "$song_name" ]; then
    song_name="$title"
    artist=""
  fi

  download_and_embed_metadata "$video_id" "$upload_date" "$title" "$artist" "$song_name"
done

# Delete all temporary files after the loop
for temp_file in "${temp_files[@]}"; do
  rm "$temp_file"
done

# Delete all image files after the loop
for image_file in "${image_files[@]}"; do
  rm "$image_file"
done        