#downloads a playlist according to config.txt as videos
@echo off
cd /D "%~dp0"
setlocal enableDelayedExpansion
set /p video="Paste the playlist link to download: "
youtube-dl ^
--config-location config.txt ^
--output %%(playlist_uploader)s-%%(playlist_title)s/%%(upload_date)s.%%(title)s.%%(id)s.%%(ext)s ^
!video!
PAUSE
