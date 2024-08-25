#!/bin/bash

# Input YouTube video URL
video_url="https://www.youtube.com/watch?v=dIu42GX9cqo"

# Output folder
output_folder="/mnt/sdb3/Videos/Youtube"

# Video quality (adjust this variable for different qualities)
video_quality="720p"

# Check if both arguments are provided
if [ -z "$video_url" ] || [ -z "$output_folder" ]; then
  echo "Usage: $0 <video_url> <output_folder>"
  exit 1
fi

# Extract video ID from the URL
video_id=$(youtube-dl --get-id "$video_url")

# Download the video with audio and visual, specifying the quality
yt-dlp -o "$output_folder/%(title)s.%(ext)s" \
  --format "bestvideo[height<=${video_quality}]+bestaudio" \
  "$video_url"

echo "Downloaded video to: $output_folder"