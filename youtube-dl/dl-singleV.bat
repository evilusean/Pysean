#download a single video using config.txt press windows+R to run and paste link
@echo off
cd /D "%~dp0"
setlocal enableDelayedExpansion
set /p video="Paste the video link to download: "
youtube-dl ^
--config-location config.txt ^
--output SingleDownloads/%%(upload_date)s.%%(title)s.%%(id)s.%%(ext)s ^
--no-playlist ^
!video!
PAUSE
