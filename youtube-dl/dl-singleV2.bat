#without config file
@echo off
cd /D "%~dp0"
setlocal enableDelayedExpansion
set /p video="Paste the video link to download: "
youtube-dl ^
--format ("bestvideo[width>=1920]"/bestvideo)+bestaudio/best ^
--restrict-filenames ^
--merge-output-format mkv ^
--ignore-errors ^
--output SingleDownloads/%%(upload_date)s.%%(title)s.%%(id)s.%%(ext)s ^
--no-playlist ^
!video!
PAUSE
