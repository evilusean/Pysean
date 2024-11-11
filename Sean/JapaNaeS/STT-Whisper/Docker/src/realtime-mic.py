import whisper
import pyaudio
import numpy as np
import threading
import queue
import os
from datetime import datetime

class MicTranslator:
    def __init__(self, source_lang="ja"):
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
        
        print("\nRecording from microphone... Press Ctrl+C to stop")
        
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
            if (datetime.now() - last_process_time).seconds >= 3:
                if audio_data:
                    try:
                        audio_np = np.frombuffer(b''.join(audio_data), dtype=np.float32)
                        result = self.model.transcribe(audio_np, language=self.source_lang)
                        print(f"\nOriginal ({self.source_lang}): {result['text']}")
                        
                        result = self.model.transcribe(audio_np, language=self.source_lang, task="translate")
                        print(f"English: {result['text']}")
                        print("-" * 50)
                        
                        audio_data = []
                        last_process_time = datetime.now()
                    except Exception as e:
                        print(f"Processing error: {e}")
            
            try:
                data = self.audio_queue.get_nowait()
                audio_data.append(data)
            except queue.Empty:
                continue
    
    def start(self):
        try:
            record_thread = threading.Thread(target=self.record_audio)
            process_thread = threading.Thread(target=self.process_audio)
            
            record_thread.start()
            process_thread.start()
            
            record_thread.join()
            process_thread.join()
            
        except KeyboardInterrupt:
            print("\nStopping...")
            self.running = False
            self.p.terminate()

if __name__ == "__main__":
    source_lang = os.getenv('WHISPER_LANG', 'ja')
    translator = MicTranslator(source_lang)
    translator.start()