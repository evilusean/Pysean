@echo off
cd /D "%~dp0"
setlocal enableDelayedExpansion
set /p video="Paste the music playlist link to download: "
youtube-dl ^
--restrict-filenames ^
--ignore-errors ^
--output Music/%%(playlist_uploader)s-%%(playlist_title)s/%%(title)s.%%(id)s.%%(ext)s ^
--format bestaudio/best ^
--extract-audio ^
--audio-format mp3 ^
--audio-quality 160K ^
--embed-thumbnail ^
!video!
PAUSE

