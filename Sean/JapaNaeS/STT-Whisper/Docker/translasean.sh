#!/bin/bash

# Default language
LANGUAGE="jp"

# Default mode
MODE="single"

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -jp) LANGUAGE="jp"; shift ;;
        -sk) LANGUAGE="sk"; shift ;;
        -yt) MODE="youtube"; shift ;;
        -p) MODE="playlist"; shift ;;
        -m) MODE="mic"; shift ;;
        -l) MODE="local"; shift ;;
        *) URL="$1"; shift ;;
    esac
done

# Set the appropriate script based on the mode
if [[ "$MODE" == "youtube" ]]; then
    if [[ "$LANGUAGE" == "jp" ]]; then
        python3 /app/src/youtube-single.py "$URL" -jp
    else
        python3 /app/src/youtube-single.py "$URL" -sk
    fi
elif [[ "$MODE" == "playlist" ]]; then
    if [[ "$LANGUAGE" == "jp" ]]; then
        python3 /app/src/youtube-playlist.py "$URL" -jp
    else
        python3 /app/src/youtube-playlist.py "$URL" -sk
    fi
elif [[ "$MODE" == "mic" ]]; then
    if [[ "$LANGUAGE" == "jp" ]]; then
        python3 /app/src/realtime-mic.py -jp
    else
        python3 /app/src/realtime-mic.py -sk
    fi
else
    if [[ "$LANGUAGE" == "jp" ]]; then
        python3 /app/src/realtime-stream.py -jp
    else
        python3 /app/src/realtime-stream.py -sk
    fi
fi