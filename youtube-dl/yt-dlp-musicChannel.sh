#!/bin/bash

# Replace these placeholders with your actual values
channel_url="https://www.youtube.com/@irvingforce/videos"
output_folder="/mnt/sdb2/Media/Music/1Youtube/"
subfolder_name="IrvingForce"

# Get the list of videos from the channel
yt-dlp --flat-playlist --yes-playlist --get-id "$channel_url" | while read video_id; do
  # Download the video with metadata
  yt-dlp -o "$output_folder/$subfolder_name/%(title)s - %(id)s.%(ext)s" \
    --embed-thumbnail \
    --add-metadata \
    --metadata-from-title "Artist - SongName" \
    --write-info-json \
    "$video_id"

  # Extract upload date from the info.json file
  upload_date=$(jq -r '.upload_date' "$output_folder/$subfolder_name/${video_id}.info.json")
  upload_date=$(date -r "$upload_date" +"%Y-%m-%d")

  # Update the album metadata in the info.json file
  jq --arg album "Youtube - Uploaded: $upload_date" '.album = $album' \
    "$output_folder/$subfolder_name/${video_id}.info.json" > \
    "$output_folder/$subfolder_name/${video_id}.info.json.tmp" && \
    mv "$output_folder/$subfolder_name/${video_id}.info.json.tmp" \
    "$output_folder/$subfolder_name/${video_id}.info.json"
done