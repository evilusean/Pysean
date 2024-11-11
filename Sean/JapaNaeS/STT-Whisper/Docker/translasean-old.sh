#!/bin/bash

# Configuration
PROJECT_DIR="/mnt/sdb4/Code/Pysean/Sean/JapaNaeS/STT-Whisper/Docker"

function show_help {
    echo "Usage: translasean [options]"
    echo "Options:"
    echo "  -jp, --japanese    Use Japanese language"
    echo "  -sk, --slovak      Use Slovak language"
    echo "  -rt, --realtime    Use realtime translation mode"
    echo "  -h, --help         Show this help message"
    echo ""
    echo "Examples:"
    echo "  translasean -jp          # Japanese file translation"
    echo "  translasean -sk          # Slovak file translation"
    echo "  translasean -jp -rt      # Japanese realtime translation"
    echo "  translasean -sk -rt      # Slovak realtime translation"
}

# Verify project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Error: Project directory not found: $PROJECT_DIR"
    exit 1
fi

# Default values
LANG="ja"
MODE="file"
SCRIPT="main.py"  # Default script

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -jp|--japanese)
            LANG="ja"
            shift
            ;;
        -sk|--slovak)
            LANG="sk"
            shift
            ;;
        -rt|--realtime)
            MODE="realtime"
            SCRIPT="realtime.py"  # Switch to realtime script
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Export environment variables
export WHISPER_LANG=$LANG
export WHISPER_MODE=$MODE
export XDG_RUNTIME_DIR="/run/user/$(id -u)"

# Verify source file exists
SOURCE_FILE="${PROJECT_DIR}/src/${SCRIPT}"
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: Source file not found: $SOURCE_FILE"
    echo "Make sure main.py and realtime.py exist in ${PROJECT_DIR}/src/"
    exit 1
fi

# Start the container
cd "$PROJECT_DIR" && \
docker compose run --rm \
    -e WHISPER_LANG=$LANG \
    -e WHISPER_MODE=$MODE \
    -e XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR \
    whisper python3 "/app/src/${SCRIPT}"