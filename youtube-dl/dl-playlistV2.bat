@echo off
cd /D "%~dp0"
setlocal enableDelayedExpansion
set /p video="Paste the playlist link to download: "
youtube-dl ^
--format ("bestvideo[width>=1920]"/bestvideo)+bestaudio/best ^
--download-archive archive.txt ^
--restrict-filenames ^
--merge-output-format mkv ^
--ignore-errors ^
--output %%(playlist_uploader)s-%%(playlist_title)s/%%(upload_date)s.%%(title)s.%%(id)s.%%(ext)s ^
!video!
PAUSE
