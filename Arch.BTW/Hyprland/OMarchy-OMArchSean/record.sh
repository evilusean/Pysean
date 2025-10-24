#!/usr/bin/env bash
# Script for region/fullscreen recording with audio support using wf-recorder
# Location: ~/scripts/record.sh
# Keybindings:
# SUPER ALT + R: Region (No Sound)
# SUPER SHIFT + R: Region (With Sound)
# SUPER SHIFT ALT + R: Fullscreen (With Sound)

# Send all output/errors to /dev/null for silent operation
LOG_FILE="/dev/null"
exec > "$LOG_FILE" 2>&1

# --- CONFIGURATION ---
# The confirmed absolute path to the wf-recorder executable
WF_RECORDER_PATH="/usr/bin/wf-recorder" 
# Your system's specific monitor source (what you hear)
AUDIO_SOURCE="alsa_output.pci-0000_00_1b.0.analog-stereo.monitor" 
# Ensure wf-recorder uses a reliable encoder
VIDEO_CODEC="libx264"
PIXEL_FORMAT="yuv420p"

# --- Utility Functions ---

get_date() { 
    date '+%Y-%m-%d_%H.%M.%S'
}

get_active_monitor() { 
    hyprctl monitors -j | jq -r '.[] | select(.focused == true) | .name'
}

# Determine the Videos directory
xdg_videos="$(xdg-user-dir VIDEOS)"
if [[ -z "$xdg_videos" ]] || [[ "$xdg_videos" == "$HOME" ]]; then
    RECORD_DIR="$HOME/Videos"
else
    RECORD_DIR="$xdg_videos"
fi
mkdir -p "$RECORD_DIR"
cd "$RECORD_DIR" || exit 1

OUTPUT_FILE="./recording_$(get_date).mp4"

# --- Main Logic ---

# Use pgrep -f to check for an existing wf-recorder process (stop recording)
if pgrep -f "$WF_RECORDER_PATH" > /dev/null; then
    # Use pkill -f for graceful stop and save
    pkill -INT -f "$WF_RECORDER_PATH"
    notify-send "Recording Stopped ⏹️" "Recording saved to $RECORD_DIR" -a 'Recorder'
    exit 0
fi

# Determine type and arguments and start the recording (start recording)
case "$1" in
    --sound)
        # Region Recording with Sound
        REGION_GEOMETRY=$(slurp -d 2>/dev/null)
        if [ -z "$REGION_GEOMETRY" ]; then
            notify-send "Recording Cancelled ❌" "Selection was cancelled" -a 'Recorder'
            exit 1
        fi
        NOTIFY_MSG="Region recording with sound"
        "$WF_RECORDER_PATH" --codec "$VIDEO_CODEC" --pixel-format "$PIXEL_FORMAT" -f "$OUTPUT_FILE" -t --geometry "$REGION_GEOMETRY" --audio="$AUDIO_SOURCE" & disown
        ;;
    --fullscreen-sound)
        # Fullscreen Recording with Sound
        ACTIVE_MONITOR=$(get_active_monitor)
        NOTIFY_MSG="Fullscreen recording with sound"
        "$WF_RECORDER_PATH" --codec "$VIDEO_CODEC" -o "$ACTIVE_MONITOR" --pixel-format "$PIXEL_FORMAT" -f "$OUTPUT_FILE" -t --audio="$AUDIO_SOURCE" & disown
        ;;
    --fullscreen)
        # Fullscreen Recording (No Sound)
        ACTIVE_MONITOR=$(get_active_monitor)
        NOTIFY_MSG="Fullscreen recording (no sound)"
        "$WF_RECORDER_PATH" --codec "$VIDEO_CODEC" -o "$ACTIVE_MONITOR" --pixel-format "$PIXEL_FORMAT" -f "$OUTPUT_FILE" -t & disown
        ;;
    *)
        # Default: Region Recording (No Sound)
        REGION_GEOMETRY=$(slurp -d 2>/dev/null)
        if [ -z "$REGION_GEOMETRY" ]; then
            notify-send "Recording Cancelled ❌" "Selection was cancelled" -a 'Recorder'
            exit 1
        fi
        NOTIFY_MSG="Region recording (no sound)"
        "$WF_RECORDER_PATH" --codec "$VIDEO_CODEC" --pixel-format "$PIXEL_FORMAT" -f "$OUTPUT_FILE" -t --geometry "$REGION_GEOMETRY" & disown
        ;;
esac

# Final check and notification
sleep 0.2
if pgrep -f "$WF_RECORDER_PATH" > /dev/null; then
    notify-send "Starting Recording 🔴" "$NOTIFY_MSG: $OUTPUT_FILE" -a 'Recorder'
else
    # This should never happen if the script is working!
    notify-send "Recording Failed ❌" "Could not start wf-recorder. Check system status." -a 'Recorder'
fi
