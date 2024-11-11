#!/bin/bash

# This script works, and it will record sections which are hotkeyed to 'Ctrl' +'[' to start and 'Ctrl' + ']' to stop
# it starts the mp3 in a temporary temp file, then moves it to the temp folder, which is then read by the STT openAI whisper docker container
# that is then transcribed, translated, and combined with english, 
# I can now record entire convos, and translate them automatically, with one button, pretty cool

# Define the temporary output directory and final output directory
TEMP_OUTPUT_DIR="/mnt/sdb4/Code/Pysean/Sean/JapaNaeS/STT-Whisper/Docker/data/audio/temp/temp_recordings"
FINAL_OUTPUT_DIR="/mnt/sdb4/Code/Pysean/Sean/JapaNaeS/STT-Whisper/Docker/data/audio/temp"
LOG_FILE="/tmp/audio_record.log"

# Create the temporary output directory if it doesn't exist
mkdir -p "$TEMP_OUTPUT_DIR"

# Function to move all files from temporary to final output directory
move_files() {
    echo "$(date): Moving files from $TEMP_OUTPUT_DIR to $FINAL_OUTPUT_DIR" >> $LOG_FILE
    # Check if there are any files in the temporary directory
    if [ "$(ls -A $TEMP_OUTPUT_DIR 2>/dev/null)" ]; then
        # Move all files to the final output directory
        if mv "$TEMP_OUTPUT_DIR"/* "$FINAL_OUTPUT_DIR"; then
            echo "All files moved successfully from $TEMP_OUTPUT_DIR to $FINAL_OUTPUT_DIR." >> $LOG_FILE
        else
            echo "Failed to move files. Permission issue." >> $LOG_FILE
        fi
    else
        echo "No files found in $TEMP_OUTPUT_DIR to move." >> $LOG_FILE
    fi
}

# Check if the first argument is "start" or "stop"
if [ "$1" == "start" ]; then
    echo "$(date): Starting recording" >> $LOG_FILE
    # Start recording from the specified audio output monitor and save as MP3 in the temporary directory
    TEMP_FILENAME="$TEMP_OUTPUT_DIR/recording_$(date +%Y%m%d_%H%M%S).mp3"  # Temporary filename
    ffmpeg -f pulse -i alsa_output.pci-0000_00_1f.3.analog-stereo.monitor -acodec libmp3lame "$TEMP_FILENAME" &
    echo $! > /tmp/recording_pid
    notify-send "Recording Started" "Recording audio to: $TEMP_FILENAME"
    echo "Recording started: $TEMP_FILENAME"
elif [ "$1" == "stop" ]; then
    echo "$(date): Stopping recording" >> $LOG_FILE
    # Stop recording
    if [ -f /tmp/recording_pid ]; then
        PID=$(cat /tmp/recording_pid)
        echo "Attempting to kill process with PID: $PID" >> $LOG_FILE
        kill $PID
        if [ $? -eq 0 ]; then
            rm /tmp/recording_pid
            # Move the completed files to the final output directory
            move_files
            notify-send "Recording Stopped" "Audio recording has been stopped and files moved."
            echo "Recording stopped." >> $LOG_FILE
        else
            echo "Failed to stop recording. Process may not exist." >> $LOG_FILE
        fi
    else
        echo "No recording in progress." >> $LOG_FILE
    fi
else
    echo "Usage: $0 {start|stop}" >> $LOG_FILE
fi
