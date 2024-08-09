import whisper
import os
# English Audio LocaSean : '/home/ArchSean/Downloads/TakenPhoneSpeech.mp3'
# Set paths
audio_file = '/home/ArchSean/Downloads/TakenPhoneSpeech.mp3'
output_dir = '/mnt/4e1c82f2-2f37-4698-9019-ee96f71a51ca/Lang/OpenAI-Whisper/Output'  

# Load the Whisper model
model = whisper.load_model("medium", download_root="/mnt/4e1c82f2-2f37-4698-9019-ee96f71a51ca/Lang/OpenAI-Whisper")

# Transcribe the audio
result = model.transcribe(audio_file)

# Extract the transcription results
text = result["text"]
segments = result["segments"]

# Save the transcription to a text file
with open(os.path.join(output_dir, "transcription.txt"), "w", encoding="utf-8") as f:
    f.write(text)

# Save the segments to a CSV file
with open(os.path.join(output_dir, "segments.csv"), "w", encoding="utf-8") as f:
    f.write("start,end,text\n")
    for segment in segments:
        f.write(f"{segment['start']},{segment['end']},{segment['text']}\n")

# Save the full results to a JSON file (optional)
with open(os.path.join(output_dir, "results.json"), "w", encoding="utf-8") as f:
    import json
    json.dump(result, f, indent=4)

print("Transcription saved to:", os.path.join(output_dir, "transcription.txt"))
print("Segments saved to:", os.path.join(output_dir, "segments.csv"))
print("Full results saved to:", os.path.join(output_dir, "results.json"))