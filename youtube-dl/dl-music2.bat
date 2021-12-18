@echo off
cd /D "%~dp0"
setlocal enableDelayedExpansion
set /p video="Paste the music video link to download: "
youtube-dl ^
--restrict-filenames ^
--ignore-errors ^
--output Music/%%(uploader)s/%%(upload_date)s.%%(title)s.%%(id)s.%%(ext)s ^
--format bestaudio/best ^
--extract-audio ^
--audio-format mp3 ^
--audio-quality 160K ^
--embed-thumbnail ^
--no-playlist ^
!video!
PAUSE
