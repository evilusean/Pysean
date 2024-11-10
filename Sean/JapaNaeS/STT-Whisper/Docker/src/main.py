import whisper
import torch
import os
import time
from datetime import datetime

def process_audio(model, audio_file):
    # Get file name without extension
    base_name = os.path.splitext(os.path.basename(audio_file))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Process paths
    audio_path = f"/app/data/audio/temp/{audio_file}"
    transcription_path = f"/app/data/output/transcripts/{base_name}_{timestamp}.txt"
    translation_path = f"/app/data/output/translations/{base_name}_{timestamp}.txt"
    
    print(f"\nProcessing: {audio_file}")
    
    # Transcribe (Japanese to Japanese)
    print("Transcribing to Japanese...")
    result = model.transcribe(audio_path, language="ja")
    with open(transcription_path, "w", encoding="utf-8") as f:
        f.write(result["text"])
    print(f"Transcription saved to: {transcription_path}")
    print("\nTranscription:")
    print(result["text"])
    
    # Translate (Japanese to English)
    print("\nTranslating to English...")
    result = model.transcribe(audio_path, language="ja", task="translate")
    with open(translation_path, "w", encoding="utf-8") as f:
        f.write(result["text"])
    print(f"Translation saved to: {translation_path}")
    print("\nTranslation:")
    print(result["text"])
    
    # Move processed file to saved directory
    os.rename(audio_path, f"/app/data/audio/saved/{audio_file}")
    print(f"\nMoved audio file to saved directory")

def watch_directory():
    print("\nLoading Whisper model...")
    model = whisper.load_model("base")
    
    print("\nModel loaded. Watching for audio files...")
    print("Place your audio files in the /app/data/audio/temp directory")
    
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
                    process_audio(model, file)
            
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