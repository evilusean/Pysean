import yt_dlp
import whisper
import os
from datetime import datetime

class YouTubeSingleTranslator:
    def __init__(self, url, source_lang="ja"):
        self.url = url
        self.source_lang = source_lang
        
        print("\nInitializing YouTube Single Translator...")
        print(f"Language: {'Japanese' if source_lang == 'ja' else 'Slovak'}")
        print(f"URL: {url}")
        
    def download_audio(self):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': f'/app/data/audio/temp/%(title)s-{self.source_lang}.%(ext)s',
            'quiet': False,
            'no_warnings': True
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print("\nDownloading audio...")
                info = ydl.extract_info(self.url, download=True)
                return f"{info['title']}-{self.source_lang}.mp3"
        except Exception as e:
            print(f"Download error: {e}")
            return None

    def process_audio(self, audio_file):
        model = whisper.load_model("base")
        
        # Get file name without extension
        base_name = os.path.splitext(os.path.basename(audio_file))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Process paths
        audio_path = f"/app/data/audio/temp/{audio_file}"
        transcription_path = f"/app/data/output/transcripts/{base_name}_{timestamp}-transcription-{self.source_lang}.txt"
        translation_path = f"/app/data/output/translations/{base_name}_{timestamp}-translation-{self.source_lang}.txt"
        combined_path = f"/app/data/output/transcribed-translated/{base_name}_{timestamp}-combined-{self.source_lang}.txt"
        
        print(f"\nProcessing: {audio_file}")
        
        # Transcribe
        print(f"Transcribing to {self.source_lang}...")
        result = model.transcribe(audio_path, language=self.source_lang)
        
        # Write transcription with timestamps
        with open(transcription_path, "w", encoding="utf-8") as f:
            for segment in result["segments"]:
                start_time = format_timestamp(segment["start"])
                f.write(f"[{start_time}] {segment['text']}\n")
        
        print(f"Transcription saved to: {transcription_path}")
        
        # Translate to English
        print("\nTranslating to English...")
        result = model.transcribe(audio_path, language=self.source_lang, task="translate")
        
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
    source_lang = os.getenv('WHISPER_LANG', 'ja')
    youtube_url = os.getenv('YOUTUBE_URL')
    
    if youtube_url:
        translator = YouTubeSingleTranslator(youtube_url, source_lang)
        audio_file = translator.download_audio()
        if audio_file:
            translator.process_audio(audio_file)
    else:
        print("No YouTube URL provided")