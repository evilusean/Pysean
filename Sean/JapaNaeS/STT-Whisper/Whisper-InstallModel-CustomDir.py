#will attempt to download and install whispers large model to a custom directory with more storage space instead of default SSD
import whisper
model = whisper.load_model('large', download_root='/media/sean/MusIX/OpenAI-Whisper/pip')