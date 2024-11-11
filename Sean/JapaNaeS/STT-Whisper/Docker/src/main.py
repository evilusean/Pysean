import os
import whisper
import numpy as np
import subprocess
from datetime import datetime

def format_timestamp(seconds):
    """Convert seconds to HH:MM:SS format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def process_audio(model, audio_file, source_lang="ja"):
    base_name = os.path.splitext(os.path.basename(audio_file))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Process paths
    audio_path = f"/app/data/audio/temp/{audio_file}"
    transcription_path = f"/app/data/output/transcripts/{base_name}_{timestamp}-transcription-{source_lang}.txt"
    translation_path = f"/app/data/output/translations/{base_name}_{timestamp}-translation-{source_lang}.txt"
    combined_path = f"/app/data/output/transcribed-translated/{base_name}_{timestamp}-combined-{source_lang}.txt"
    
    print(f"\nProcessing: {audio_file}")
    
    # Transcribe
    print(f"Transcribing to {source_lang}...")
    result = model.transcribe(audio_path, language=source_lang)
    
    # Write transcription with timestamps
    with open(transcription_path, "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            start_time = format_timestamp(segment["start"])
            f.write(f"[{start_time}] {segment['text']}\n")
    
    print(f"Transcription saved to: {transcription_path}")
    
    # Translate to English
    print("\nTranslating to English...")
    result = model.transcribe(audio_path, language=source_lang, task="translate")
    
    # Write translation with timestamps
    with open(translation_path, "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            start_time = format_timestamp(segment["start"])
            f.write(f"[{start_time}] {segment['text']}\n")
    
    print(f"Translation saved to: {translation_path}")
    
    # Combine transcriptions and translations
    with open(combined_path, "w", encoding="utf-8") as f:
        for i in range(len(result["segments"])):
            f.write(f"{result['segments'][i]['text']} (Translation: {result['segments'][i]['text']})\n")
    
    print(f"Combined transcription and translation saved to: {combined_path}")
    
    # Move processed file to saved directory
    os.rename(audio_path, f"/app/data/audio/saved/{audio_file}")
    print(f"\nMoved audio file to saved directory")

if __name__ == "__main__":
    # Load Whisper model
    model = whisper.load_model("base")
    
    # Watch for new files in the temp directory
    while True:
        audio_files = os.listdir("/app/data/audio/temp")
        for audio_file in audio_files:
            if audio_file.endswith(".mp3"):
                process_audio(model, audio_file, source_lang="ja")  # Default to Japanese