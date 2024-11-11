import whisper
import torch
import os
import time
from datetime import datetime
import sys

def format_timestamp(seconds):
    """Convert seconds to HH:MM:SS format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def process_audio(model, audio_file, source_lang="ja"):
    # Get file name without extension
    base_name = os.path.splitext(os.path.basename(audio_file))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Process paths
    audio_path = f"/app/data/audio/temp/{audio_file}"
    transcription_path = f"/app/data/output/transcripts/{base_name}_{timestamp}.txt"
    translation_path = f"/app/data/output/translations/{base_name}_{timestamp}.txt"
    
    print(f"\nProcessing: {audio_file}")
    
    # Transcribe with timestamps
    print(f"Transcribing to {source_lang}...")
    result = model.transcribe(audio_path, language=source_lang)
    
    # Write transcription with timestamps
    with open(transcription_path, "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            start_time = format_timestamp(segment["start"])
            f.write(f"[{start_time}] {segment['text']}\n")
    
    print(f"Transcription saved to: {transcription_path}")
    print("\nTranscription with timestamps:")
    for segment in result["segments"]:
        start_time = format_timestamp(segment["start"])
        print(f"[{start_time}] {segment['text']}")
    
    # Translate to English with timestamps
    print("\nTranslating to English...")
    result = model.transcribe(audio_path, language=source_lang, task="translate")
    
    # Write translation with timestamps
    with open(translation_path, "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            start_time = format_timestamp(segment["start"])
            f.write(f"[{start_time}] {segment['text']}\n")
    
    print(f"Translation saved to: {translation_path}")
    print("\nTranslation with timestamps:")
    for segment in result["segments"]:
        start_time = format_timestamp(segment["start"])
        print(f"[{start_time}] {segment['text']}")
    
    # Move processed file to saved directory
    os.rename(audio_path, f"/app/data/audio/saved/{audio_file}")
    print(f"\nMoved audio file to saved directory")

def watch_directory():
    print("\nLoading Whisper model...")
    model = whisper.load_model("base")
    
    print("\nModel loaded. Watching for audio files...")
    print("Place your audio files in the /app/data/audio/temp directory")
    
    # Get language from environment variable or default to Japanese
    source_lang = os.getenv('WHISPER_LANG', 'ja')
    print(f"\nUsing language: {'Japanese' if source_lang == 'ja' else 'Slovak'}")
    
    while True:
        try:
            # Check for audio files
            files = [f for f in os.listdir("/app/data/audio/temp") 
                    if f.endswith(('.mp3', '.wav', '.m4a'))]
            
            if files:
                print(f"\nFound {len(files)} new audio file(s):")
                for i, file in enumerate(files, 1):
                    print(f"{i}. {file}")
                
                # Process each file
                for file in files:
                    process_audio(model, file, source_lang)
            
            time.sleep(5)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    # Test GPU first
    print("\nChecking GPU...")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU device: {torch.cuda.get_device_name(0)}")
    
    # Start watching directory
    watch_directory()