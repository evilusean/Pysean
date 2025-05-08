#!/bin/bash

# since hyprland doesn't save the last audio level before you muted, and you have to raise
# it all the way back to 80% or whatever after pressing, simple script to fix that

sink_name="@DEFAULT_AUDIO_SINK@"
previous_volume_file="/tmp/previous_volume.txt"

# Function to get the current volume and mute status
get_sink_info() {
  local output
  output=$(wpctl get-volume "$sink_name" 2>/dev/null)
  if [[ $? -ne 0 ]]; then
    echo "Error getting sink information."
    return 1
  fi

  volume=$(echo "$output" | grep -oP 'Volume: (\d+\%)' | awk -F': ' '{print $2}' | sed 's/%//' | awk '{printf "%.2f\n", $1 / 100}')
  muted=$(echo "$output" | grep -oP 'Mute: (yes|no)' | awk -F': ' '{print $2}')

  if [[ -z "$volume" || -z "$muted" ]]; then
    echo "Could not parse sink information."
    return 1
  fi

  echo "$volume" "$muted"
}

# Function to set the volume
set_volume() {
  wpctl set-volume "$sink_name" "$1%" 2>/dev/null
}

# Function to set the mute status
set_mute() {
  wpctl set-mute "$sink_name" "$1" 2>/dev/null
}

# Get current volume and mute status
if read -r current_volume current_muted < <(get_sink_info); then
  if [[ "$current_muted" == "yes" ]]; then
    if [[ -f "$previous_volume_file" ]]; then
      previous_volume=$(cat "$previous_volume_file")
      set_volume "$previous_volume"
      echo "Unmuted, restoring volume to $(printf "%.0f" $(echo "$previous_volume * 100" | bc))%"
    else
      set_volume 80
      echo "Unmuted, setting volume to 80%"
    fi
  else
    echo "$current_volume" > "$previous_volume_file"
    set_mute toggle
    echo "Muted, saved volume at $(printf "%.0f" $(echo "$current_volume * 100" | bc))%"
  fi
else
  echo "Failed to get audio status."
fi
