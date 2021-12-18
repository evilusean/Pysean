#downloads a single song as mp3
@echo off
cd /D "%~dp0"
setlocal enableDelayedExpansion
set /p video="Paste the music video link to download: "
youtube-dl ^
--config-location config.txt ^
--output Music/%%(title)s.%%(id)s.%%(ext)s ^
--format bestaudio/best ^
--extract-audio ^
--no-playlist ^
!video!
PAUSE
