#!/bin/bash

# Set the directory containing the WMA files
wma_directory="/mnt/sdb4/Lang/Slovake/KrizomKrazom/Audio/KK_A1_1"

# Set the output directory for MP3 files (optional, will use WMA directory if not set)
mp3_directory="${wma_directory}"

# Loop through each WMA file in the directory
for filename in "$wma_directory"/*.wma; do
  # Get the filename without extension
  base_filename=$(basename "$filename" .wma)

  # Construct the output MP3 filename
  output_filename="$mp3_directory/${base_filename}.mp3"

  # Use ffmpeg to convert WMA to MP3
  ffmpeg -i "$filename" -vn -ar 44100 -ac 2 -ab 192k -f mp3 "$output_filename"

  # Check if the conversion was successful
  if [ $? -eq 0 ]; then
    echo "Converted: $filename to $output_filename"
  else
    echo "Error converting: $filename"
  fi
done

echo "Conversion complete!"