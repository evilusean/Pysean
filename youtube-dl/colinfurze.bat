#downloads entire colinfruze channel in an archive
cd /D "%~dp0"
youtube-dl https://www.youtube.com/user/colinfurze/videos --format ("bestvideo[width>=1920]"/bestvideo)+bestaudio/best --download-archive archive.txt --output %%(uploader)s/%%(upload_date)s.%%(title)s.%%(id)s.%%(ext)s --restrict-filenames --merge-output-format mkv --ignore-errors
PAUSE
