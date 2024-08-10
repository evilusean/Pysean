import whisper
import os
#Just tested again, it's like 80% of the words, from what I can tell comparing the audio and romaji
# Pretty good, but not great - could I use this for work recording audio of meetings and then translate?
# Shows/Anime/Conversations/Daily use? It's too slow to be used live, future goals = TransLaSean
# add translation with a locally run free open source translator like 'Argos Translate' to the CSV

# Set paths
audio_file = '/home/ArchSean/Downloads/Egg-Sans-Diary.mp3'  #add a japanese audio file - audiophile?    
output_dir = '/mnt/4e1c82f2-2f37-4698-9019-ee96f71a51ca/Lang/OpenAI-Whisper/Output'  

# Load the Whisper model
model = whisper.load_model("medium", download_root="/mnt/4e1c82f2-2f37-4698-9019-ee96f71a51ca/Lang/OpenAI-Whisper")

# Transcribe the audio
result = model.transcribe(audio_file, language="ja")  # Specify Japanese language

# Extract the transcription results
text = result["text"]
segments = result["segments"]

# Save the transcription to a text file
with open(os.path.join(output_dir, "transcription-ja.txt"), "w", encoding="utf-8") as f:
    f.write(text)

# Save the segments to a CSV file
with open(os.path.join(output_dir, "segments-ja.csv"), "w", encoding="utf-8") as f:
    f.write("start,end,text,romaji,hiragana\n")
    for segment in segments:
        # Convert to romaji and hiragana (you'll need a library for this)
        # Example using the 'unidecode' library (install it first: pip install unidecode)
        from unidecode import unidecode
        romaji = unidecode(segment['text'])
        hiragana = segment['text']  # Assuming the text is already in hiragana

        f.write(f"{segment['start']},{segment['end']},{segment['text']},{romaji},{hiragana}\n")

def format_timestamp(seconds):
    """Formats a timestamp in seconds to the SRT format (HH:MM:SS,mmm)."""
    milliseconds = int(seconds * 1000)
    hours, remainder = divmod(milliseconds, 3600000)
    minutes, remainder = divmod(remainder, 60000)
    seconds, milliseconds = divmod(remainder, 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

# Save the segments to an SRT file
with open(os.path.join(output_dir, "transcription-ja.srt"), "w", encoding="utf-8") as f:
    for i, segment in enumerate(segments):
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text']

        # Format timestamps for SRT
        start_timestamp = format_timestamp(start_time)
        end_timestamp = format_timestamp(end_time)

        f.write(f"{i+1}\n")
        f.write(f"{start_timestamp} --> {end_timestamp}\n")
        f.write(f"{text}\n\n")

# Save the full results to a JSON file (optional)
with open(os.path.join(output_dir, "results-ja.json"), "w", encoding="utf-8") as f:
    import json
    json.dump(result, f, indent=4)

print("Japanese Transcription saved to:", os.path.join(output_dir, "transcription-ja.txt"))
print("Japanese Segments saved to:", os.path.join(output_dir, "segments-ja.csv"))
print("Japanese Segments saved to:", os.path.join(output_dir, "transcription-ja.srt"))
print("Japanese Full results saved to:", os.path.join(output_dir, "results-ja.json"))