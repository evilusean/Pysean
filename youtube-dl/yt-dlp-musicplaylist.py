import os
import yt_dlp
import re
import datetime

def download_playlist(playlist_url, output_folder, subfolder_name):
    """Downloads a YouTube playlist and saves metadata and cover art.

    Args:
        playlist_url (str): The URL of the YouTube playlist.
        output_folder (str): The main folder to save the downloaded files and metadata.
        subfolder_name (str): The name of the subfolder within the main folder.     
    """

    # Create the output folder if it doesn't exist
    os.makedirs(os.path.join(output_folder, subfolder_name), exist_ok=True)

    # Define yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',  # Download best audio quality
        'outtmpl': os.path.join(output_folder, subfolder_name, '%(title)s - %(id)s.%(ext)s'),  # Output filename format
        'writethumbnail': True,  # Download thumbnail
        'extract_flat': True,  # Extract playlist items individually
        'ignoreerrors': True,  # Ignore errors for individual videos
        'quiet': True,  # Suppress output
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(playlist_url, download=True)
            for entry in info['entries']:
                # Extract metadata
                title = entry['title']
                artist, song_name = extract_artist_song(title)
                thumbnail = entry['thumbnails'][0]['url'] if 'thumbnails' in entry else None
                upload_date_str = entry['upload_date']
                upload_date = datetime.datetime.strptime(upload_date_str, '%Y%m%d').strftime('%Y-%m-%d')

                # Create a file for metadata
                metadata_file = os.path.join(output_folder, subfolder_name, f"{title} - {song_name}.txt")
                with open(metadata_file, 'w', encoding='utf-8') as f:
                    f.write(f"Title: {title}\n")
                    f.write(f"Artist: {artist}\n")
                    f.write(f"Song Name: {song_name}\n")
                    f.write(f"Album: Youtube - Uploaded: {upload_date}\n")  # Add the album "Youtube" to the metadata

                # Save the thumbnail
                if thumbnail:
                    thumbnail_file = os.path.join(output_folder, subfolder_name, f"{title} - {song_name}.jpg")
                    ydl.download([thumbnail], outfile=thumbnail_file)

        except Exception as e:
            print(f"Error downloading playlist: {e}")

def extract_artist_song(title):
    """Extracts artist and song name from a title in the format 'Artist - SongName'.

    Args:
        title (str): The title string.

    Returns:
        tuple: A tuple containing the artist and song name, or (None, title) if no dash is found.
    """
    parts = title.split(' - ')
    if len(parts) == 2:
        return parts[0], parts[1]
    else:
        return None, title

# Example usage:
playlist_url = "https://www.youtube.com/playlist?list=PL..."  # Replace with your playlist URL
output_folder = "Downloaded_Music"  # Replace with your desired output folder
subfolder_name = "MyPlaylist"  # Replace with your desired subfolder name

download_playlist(playlist_url, output_folder, subfolder_name)
