import whisper
import torch
import pyaudio
import numpy as np
import threading
import queue
import os
from datetime import datetime

class RealtimeTranslator:
    def __init__(self, source_lang="ja"):
        print("\nInitializing Realtime Translator...")
        print(f"Language: {'Japanese' if source_lang == 'ja' else 'Slovak'}")
        
        self.source_lang = source_lang
        self.model = whisper.load_model("base")
        self.audio_queue = queue.Queue()
        self.running = True
        
        # Audio recording parameters
        self.CHUNK = 1024 * 4
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 16000
        
        # Initialize PyAudio
        self.p = pyaudio.PyAudio()
        
    def record_audio(self):
        stream = self.p.open(format=self.FORMAT,
                           channels=self.CHANNELS,
                           rate=self.RATE,
                           input=True,
                           frames_per_buffer=self.CHUNK)
        
        print("\nRecording... Press Ctrl+C to stop")
        
        while self.running:
            try:
                data = stream.read(self.CHUNK, exception_on_overflow=False)
                self.audio_queue.put(data)
            except Exception as e:
                print(f"Recording error: {e}")
                break
        
        stream.stop_stream()
        stream.close()
    
    def process_audio(self):
        audio_data = []
        last_process_time = datetime.now()
        
        while self.running:
            # Process every 3 seconds of audio
            if (datetime.now() - last_process_time).seconds >= 3:
                if audio_data:
                    try:
                        # Convert audio data to numpy array
                        audio_np = np.frombuffer(b''.join(audio_data), dtype=np.float32)
                        
                        # Transcribe
                        result = self.model.transcribe(audio_np, language=self.source_lang)
                        print(f"\nOriginal ({self.source_lang}): {result['text']}")
                        
                        # Translate
                        result = self.model.transcribe(audio_np, language=self.source_lang, task="translate")
                        print(f"English: {result['text']}")
                        print("-" * 50)
                        
                        # Clear audio buffer
                        audio_data = []
                        last_process_time = datetime.now()
                    except Exception as e:
                        print(f"Processing error: {e}")
            
            # Collect audio data
            try:
                data = self.audio_queue.get_nowait()
                audio_data.append(data)
            except queue.Empty:
                continue
    
    def start(self):
        try:
            # Start recording and processing threads
            record_thread = threading.Thread(target=self.record_audio)
            process_thread = threading.Thread(target=self.process_audio)
            
            record_thread.start()
            process_thread.start()
            
            # Wait for Ctrl+C
            record_thread.join()
            process_thread.join()
            
        except KeyboardInterrupt:
            print("\nStopping...")
            self.running = False
            self.p.terminate()

if __name__ == "__main__":
    # Test GPU first
    print("\nChecking GPU...")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU device: {torch.cuda.get_device_name(0)}")
    
    # Get language from environment variable
    source_lang = os.getenv('WHISPER_LANG', 'ja')
    
    # Start realtime translation
    translator = RealtimeTranslator(source_lang)
    translator.start()