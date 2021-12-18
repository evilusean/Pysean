#downloads an entire playlist as mp3
@echo off
cd /D "%~dp0"
setlocal enableDelayedExpansion
set /p video="Paste the music playlist link to download: "
youtube-dl ^
--config-location config.txt ^
--download-archive archive.txt ^
--output Music/%%(playlist_uploader)s-%%(playlist_title)s/%%(title)s.%%(id)s.%%(ext)s ^
--format bestaudio/best ^
--extract-audio ^
!video!
PAUSE
