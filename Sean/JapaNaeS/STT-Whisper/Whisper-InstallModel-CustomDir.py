#will attempt to download and install whispers large model to a custom directory with more storage space instead of default SSD
import whisper
model = whisper.load_model('medium', download_root='/mnt/4e1c82f2-2f37-4698-9019-ee96f71a51ca/Lang/OpenAI-Whisper')





