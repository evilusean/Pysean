import os
import subprocess
import time

def combine_audio_files(category):
    """Combines audio files from Slovak and English folders into a single file,
    repeating Slovak words three times with a delay before playing the English word.

    Args:
        category (str): The category name (e.g., "Numbers", "Shopping").
    """

    slovak_audio_dir = f"/media/sean/MusIX/Piper/Slovak/{category}/Slovak"
    english_audio_dir = f"/media/sean/MusIX/Piper/Slovak/{category}/English"

    # Get a list of all audio files in both folders
    slovak_files = [f for f in os.listdir(slovak_audio_dir) if f.endswith(".wav")]
    english_files = [f for f in os.listdir(english_audio_dir) if f.endswith(".wav")]

    # Sort the files numerically (assuming filenames start with numbers)
    slovak_files.sort()
    english_files.sort()

    # Construct the FFmpeg command to combine the files
    ffmpeg_command = [
        "ffmpeg",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        "<(for f in " + " ".join(
            [os.path.join(slovak_audio_dir, f) for f in slovak_files]
        ) + "; do echo \"file '$f'\"; done)",
        "-i",
        "<(for f in " + " ".join(
            [os.path.join(english_audio_dir, f) for f in english_files]
        ) + "; do echo \"file '$f'\"; done)",
        "-filter_complex",
        # Repeat Slovak three times with a 1-second delay
        "[0:a]atrim=0:1,asetpts=PTS-STARTPTS[slovak1];"
        "[slovak1]adelay=1000|1000[slovak2];"
        "[slovak2]atrim=0:1,asetpts=PTS-STARTPTS[slovak3];"
        "[slovak3]adelay=1000|1000[slovak4];"
        "[slovak4]atrim=0:1,asetpts=PTS-STARTPTS[slovak5];"
        "[slovak5]adelay=1000|1000[slovak6];"
        # Combine Slovak and English
        "[slovak6][1:a]concat=n=2:v=0:a=1[out];"
        "[out]aformat=s16le[out1];"
        "[out1]aresample=44100[out2];"
        "[out2]volume=0.5[out3];"
        "[out3]showwaves=s=1920x1080:mode=full:colors=cyan:scale=10:rate=25[out4];"
        "[out4]format=yuv420p[out5];"
        "[out5]scale=1920x1080[out6];"
        "[out6]fps=25[out7];"
        "[out7]pad=1920:1080:0:0:black[out8];"
        "[out8]drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeMono.ttf:text='{value}':x=(w-text_w)/2:y=(h-text_h)/2:fontsize=48:fontcolor=white:shadowcolor=black:shadowx=2:shadowy=2:box=1:boxcolor=black@0.5:boxborderw=5:boxbordercolor=white[out9];"
        "out9",
        "-map",
        "[out9]",
        "-c:v",
        "libx264",
        "-preset",
        "ultrafast",
        "-crf",
        "23",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-movflags",
        "+faststart",
        os.path.join(f"/media/sean/MusIX/Piper/Slovak/{category}/", f"{category}_Slovak_English_Combined.wav"),  # Use category in the filename
    ]

    # Run the FFmpeg command
    subprocess.run(ffmpeg_command)

    print(f"Audio files combined into {category}_Slovak_English_Combined.wav in /media/sean/MusIX/Piper/Slovak/{category}/")

# Example usage:
category = "Numbers"  # Replace with your category
combine_audio_files(category)