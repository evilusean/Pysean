@echo off
cd /D "%~dp0"
youtube-dl ^
--restrict-filenames ^
--ignore-errors ^
--output "I:/Music/IdleGlance/%%(playlist_uploader)s-%%(playlist_title)s/%%(title)s.%%(id)s.%%(ext)s" ^
--download-archive IdleGlance.txt ^
--format bestaudio/best ^
--extract-audio ^
--audio-format mp3 ^
--audio-quality 160K ^
--embed-thumbnail ^
--restrict-filenames ^
"https://www.youtube.com/c/idleglance/videos" ^
!video!
PAUSE


