#!/usr/bin/env bash
# Updated script for region/fullscreen recording with audio support
# Screenshot to Clipboard (Region)
# 'bindd = Super+Shift, S, Screen snip, exec, pidof slurp || hyprshot --freeze --clipboard-only --mode region --silent'
# Region Recording (No sound)
#'bindd = Super+Alt, R, Record region (no sound), exec, ~/bin/record.sh'
# Fullscreen Recording (With sound)
#'bindd = Super+Shift+Alt, R, Record screen (with sound), exec, ~/bin/record.sh --fullscreen-sound'

get_date() {
    date '+%Y-%m-%d_%H.%M.%S'
}

get_default_audio_source() {
    # On Wayland/Pipewire, the default source is usually @DEFAULT_AUDIO_SOURCE@
    # If the default script uses a different method, you might need to adjust this.
    # We will use the common Pipewire default which is usually sufficient.
    echo "@DEFAULT_AUDIO_SOURCE@"
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
AUDIO_SOURCE=$(get_default_audio_source)

if pgrep wf-recorder > /dev/null; then
    notify-send "Recording Stopped ⏹️" "Recording saved to $RECORD_DIR" -a 'Recorder'
    pkill wf-recorder
else
    # Handle the different recording arguments
    case "$1" in
        --sound)
            if ! region="$(slurp 2>&1)"; then
                notify-send "Recording Cancelled ❌" "Selection was cancelled" -a 'Recorder'
                exit 1
            fi
            NOTIFY_MSG="Region recording with sound"
            wf-recorder --pixel-format yuv420p -f "$OUTPUT_FILE" -t --geometry "$region" --audio="$AUDIO_SOURCE" & disown
            ;;
        --fullscreen-sound)
            NOTIFY_MSG="Fullscreen recording with sound"
            wf-recorder -o $(get_active_monitor) --pixel-format yuv420p -f "$OUTPUT_FILE" -t --audio="$AUDIO_SOURCE" & disown
            ;;
        --fullscreen)
            NOTIFY_MSG="Fullscreen recording (no sound)"
            wf-recorder -o $(get_active_monitor) --pixel-format yuv420p -f "$OUTPUT_FILE" -t & disown
            ;;
        *)
            if ! region="$(slurp 2>&1)"; then
                notify-send "Recording Cancelled ❌" "Selection was cancelled" -a 'Recorder'
                exit 1
            fi
            NOTIFY_MSG="Region recording (no sound)"
            wf-recorder --pixel-format yuv420p -f "$OUTPUT_FILE" -t --geometry "$region" & disown
            ;;
    esac

    # Start notification (only if recording started)
    if pgrep wf-recorder > /dev/null; then
        notify-send "Starting Recording 🔴" "$NOTIFY_MSG: $OUTPUT_FILE" -a 'Recorder'
    fi
fi
