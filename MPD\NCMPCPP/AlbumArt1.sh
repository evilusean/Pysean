#!/bin/bash

#this script, isn't checking, would need to update either mpd.conf or ncmpcpp.config to run on change
# Requires mpc, kitty and exiftool

# Set the directory where your music is stored
MUSIC_DIR=$HOME/docum 

# Set the temporary file for the extracted album art
COVER=/tmp/cover.jpg

# Function to reset the terminal background
function reset_background {
  printf "\e]20;;100x100+1000+1000\a"
}

# Function to display the album art in the kitty terminal
function display_album_art {
  local src="$1"
  local cover="$2"

  rm -f "$cover"
  if [[ -n "$src" ]]; then
    # Save the extracted album art to a temporary file
    echo "$src" > "$cover"
    if [[ -f "$cover" ]]; then
      # Display the album art in the kitty terminal
      kitty +kitten icat "$cover"
    else
      reset_background
    fi
  else
    reset_background
  fi
}

# Get the current song's file path
file=$(mpc --format %file% current)

# Check if the file exists
if [[ ! -f "$file" ]]; then
  echo "Error: Current song file not found."
  exit 1
fi

# Extract embedded album art using exiftool
src=$(exiftool -b -Picture "$file" 2>/dev/null)
display_album_art "$src" "$COVER"

# If no embedded album art is found, search for album art in the directory
if [[ ! -f "$COVER" ]]; then
  album_dir="${file%/*}"
  [[ -z "$album_dir" ]] && exit 1
  album_dir="$MUSIC_DIR/$album_dir"

  covers="$(find "$album_dir" -type d -exec find {} -maxdepth 1 -type f -iregex ".*/.*\(${album}\|cover\|folder\|artwork\|front\).*[.]\(jpe?g\|png\|gif\|bmp\)" \; )"
  src="$(echo -n "$covers" | head -n1)"
  display_album_art "$src" "$COVER"
fi

# Keep the album art displayed until the next song starts
while true; do
  if [[ $(mpc status | grep "playing") ]]; then
    sleep 1
  else
    break
  fi
done

# Reset the terminal background when the song ends
reset_background