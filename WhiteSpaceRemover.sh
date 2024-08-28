#!/bin/bash
#sudo chmod +x WhiteSpaceRemover.sh

# Set the directory containing the files you want to rename
directory="/mnt/sdb4/Lang/Slovake/KrizomKrazom/Audio/KK_A1_2" 

# Loop through each file in the directory
for filename in "$directory"/*; do
  # Use parameter expansion to replace spaces with underscores in the filename
  new_filename="${filename// /_}"

  # Rename the file
  mv "$filename" "$new_filename"
done

echo "Files renamed successfully!"