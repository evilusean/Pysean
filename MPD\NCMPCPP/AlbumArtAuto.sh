#!/bin/bash

# Requires mpc, kitty and exiftool

# Set the directory where your music is stored
MUSIC_DIR="/mnt/sdb2/Media/Music/1Youtube"

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

# Function to update album art when a song changes
function update_album_art {
  # Get the current song's file path
  file=$(mpc --format %file% current)

  # Check if the file exists
  if [[ ! -f "$file" ]]; then
    echo "Error: Current song file not found."
    return 1
  fi

  # Extract embedded album art using exiftool
  src=$(exiftool -b -Picture "$file" 2>/dev/null)
  display_album_art "$src" "$COVER"

  # If no embedded album art is found, search for album art in the directory
  if [[ ! -f "$COVER" ]]; then
    album_dir="${file%/*}"
    [[ -z "$album_dir" ]] && return 1
    album_dir="$MUSIC_DIR/$album_dir"

    covers="$(find "$album_dir" -type d -exec find {} -maxdepth 1 -type f -iregex ".*/.*\(${album}\|cover\|folder\|artwork\|front\).*[.]\(jpe?g\|png\|gif\|bmp\)" \; )"
    src="$(echo -n "$covers" | head -n 1)"
    display_album_art "$src" "$COVER"
  fi
}

# Function to refresh kunst
function refresh_kunst {
  # Send a SIGUSR1 signal to kunst to refresh
  pkill -USR1 kunst
}

# Run the update_album_art function when a song changes
mpc | while read line; do
  if [[ "$line" =~ "Playing" ]]; then
    # Run the update_album_art function in the background
    update_album_art &
    # Refresh kunst
    refresh_kunst &
  fi
done

# Reset the terminal background when the script exits
reset_background
Explanation:

refresh_kunst Fun