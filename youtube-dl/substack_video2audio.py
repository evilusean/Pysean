#!/usr/bin/env python3
"""
# Substack Audio Downloader

A simple Python script that downloads videos from Substack articles and converts them to MP3 audio files.

## Requirements

- Python 3.6+
- yt-dlp
- ffmpeg (for audio conversion)

## Installation

1. Install Python dependencies:
```bash
pip install yt-dlp
```

2. Install ffmpeg:
   - On Ubuntu/Debian: `sudo apt install ffmpeg`
   - On Arch Linux: `sudo pacman -S ffmpeg`
   - On macOS: `brew install ffmpeg`
   - On Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

## Usage

### Interactive Mode

Run the script without arguments to use interactive mode:

```bash
python substack_audio_downloader.py
```

The script will prompt you for:
- The Substack URL containing the video
- The output folder where the MP3 should be saved (defaults to "downloaded_audio")

### Command Line Arguments

You can also provide the URL and output folder as command line arguments:

```bash
python substack_audio_downloader.py "https://example.substack.com/post-with-video" "my_audio_folder"
```

## How It Works

1. The script validates that the provided URL is from Substack
2. It extracts the video from the Substack page
3. It downloads the video and converts it to MP3 format
4. It embeds the thumbnail as cover art and adds metadata
5. The resulting MP3 file is saved to the specified output folder

## Troubleshooting

- **No downloadable media found**: Make sure the Substack post actually contains a video
- **Download fails**: Try updating yt-dlp with `pip install -U yt-dlp`
- **Audio conversion fails**: Make sure ffmpeg is properly installed and in your PATH 
"""
import os
import sys
import yt_dlp
import re
import platform
import shutil
from urllib.parse import urlparse

# Default download folder
DEFAULT_DOWNLOAD_FOLDER = "/home/ArchSean/Downloads/"

def validate_substack_url(url):
    """
    Validates if the URL is from Substack.
    
    Args:
        url (str): The URL to validate.
        
    Returns:
        bool: True if the URL is from Substack, False otherwise.
    """
    if not url or not isinstance(url, str):
        return False
        
    # Clean the URL
    url = url.strip()
    
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        
        # Check if the domain contains substack.com or ends with .substack.com
        return 'substack.com' in domain or domain.endswith('.substack.com')
    except Exception:
        return False

def check_dependencies():
    """
    Checks if required dependencies (ffmpeg) are installed.
    
    Returns:
        bool: True if all dependencies are installed, False otherwise.
    """
    if shutil.which('ffmpeg') is None:
        print("Error: ffmpeg is not installed or not in PATH.")
        print("Please install ffmpeg:")
        if platform.system() == "Linux":
            print("  For Ubuntu/Debian: sudo apt install ffmpeg")
            print("  For Arch Linux: sudo pacman -S ffmpeg")
        elif platform.system() == "Darwin":  # macOS
            print("  For macOS: brew install ffmpeg")
        elif platform.system() == "Windows":
            print("  For Windows: Download from https://ffmpeg.org/download.html and add to PATH")
        return False
    return True

def sanitize_filename(filename):
    """
    Sanitizes a filename by replacing non-ASCII characters.
    
    Args:
        filename (str): The filename to sanitize.
        
    Returns:
        str: The sanitized filename.
    """
    # Replace colons with hyphens (common in Substack titles)
    filename = filename.replace(':', '-')
    # Replace other problematic characters
    filename = re.sub(r'[\\/*?:"<>|]', '-', filename)
    return filename

def download_substack_audio(url, output_folder=DEFAULT_DOWNLOAD_FOLDER):
    """
    Downloads a video from Substack as an MP3 file.
    
    Args:
        url (str): The URL of the Substack page containing the video.
        output_folder (str): The folder where the MP3 will be saved.
        
    Returns:
        bool: True if download was successful, False otherwise.
    """
    if not validate_substack_url(url):
        print("Error: The URL does not appear to be from Substack.")
        return False
        
    if not check_dependencies():
        return False
        
    # Create output folder if it doesn't exist
    try:
        os.makedirs(output_folder, exist_ok=True)
    except PermissionError:
        print(f"Error: No permission to create directory {output_folder}")
        return False
    except Exception as e:
        print(f"Error creating output directory: {e}")
        return False
    
    # Define a custom progress hook to track the downloaded file path
    downloaded_file = None
    
    def progress_hook(d):
        nonlocal downloaded_file
        if d['status'] == 'finished':
            if 'filename' in d:
                downloaded_file = d['filename']
            print(f"Download complete. Converting to MP3...")
    
    # Define yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',  # Download best audio quality
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),  # Output filename format
        'noplaylist': True,  # Only download single video, not playlist
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }, {
            'key': 'EmbedThumbnail',  # Embed thumbnail in the audio as cover art
        }, {
            'key': 'FFmpegMetadata',  # Add metadata
        }],
        'writethumbnail': True,  # Download thumbnail
        'writeinfojson': True,  # Write info json
        'progress_hooks': [progress_hook],  # Add progress hook
        'ignoreerrors': True,  # Ignore errors
        'quiet': False,  # Show output
        'verbose': False,  # No verbose output
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info first to check if the URL contains downloadable media
            print(f"Checking URL: {url}")
            info = ydl.extract_info(url, download=False)
            
            if info:
                title = info.get('title', 'Unknown Title')
                sanitized_title = sanitize_filename(title)
                print(f"Found media: {title}")
                print(f"Duration: {info.get('duration_string', 'Unknown duration')}")
                print("Starting download...")
                
                # Now download the media
                ydl.download([url])
                print(f"Successfully downloaded and converted to MP3.")
                
                # Check for the MP3 file in the output folder
                expected_mp3 = os.path.join(output_folder, f"{sanitized_title}.mp3")
                if os.path.exists(expected_mp3):
                    print(f"Saved as: {expected_mp3}")
                else:
                    # Try looking for any MP3 file with a similar name
                    mp3_files = [f for f in os.listdir(output_folder) 
                                if f.endswith('.mp3') and title.lower() in f.lower()]
                    if mp3_files:
                        print(f"Saved as: {os.path.join(output_folder, mp3_files[0])}")
                
                # Clean up any leftover thumbnail or JSON files
                for ext in ['.png', '.jpg', '.webp', '.info.json']:
                    possible_file = os.path.join(output_folder, f"{sanitized_title}{ext}")
                    if os.path.exists(possible_file):
                        try:
                            os.remove(possible_file)
                        except Exception:
                            pass
                
                return True
            else:
                print("Error: No downloadable media found at the URL.")
                print("Make sure the Substack post contains a video.")
                return False
    except yt_dlp.utils.DownloadError as e:
        print(f"Download error: {e}")
        return False
    except yt_dlp.utils.ExtractorError as e:
        print(f"Extraction error: {e}")
        return False
    except Exception as e:
        print(f"Error downloading from Substack: {e}")
        return False

def main():
    # Print welcome message
    print("=== Substack Audio Downloader ===")
    
    if len(sys.argv) > 1:
        # If URL is provided as command line argument
        url = sys.argv[1]
        output_folder = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_DOWNLOAD_FOLDER
        success = download_substack_audio(url, output_folder)
    else:
        # Ask for URL interactively
        url = input("Enter the Substack URL containing the video: ")
        output_folder = input(f"Enter the output folder path (press Enter for default '{DEFAULT_DOWNLOAD_FOLDER}'): ")
        if not output_folder:
            output_folder = DEFAULT_DOWNLOAD_FOLDER
        
        success = download_substack_audio(url, output_folder)
    
    if success:
        print(f"Audio saved to: {os.path.abspath(output_folder)}")
    else:
        print("Failed to download audio from the provided URL.")
        
    print("=== Process complete ===")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1) 