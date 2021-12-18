@echo off
cd /D "%~dp0"
youtube-dl ^
--ignore-errors ^
--output "I:/Music/Scroll/%%(playlist_uploader)s-%%(playlist_title)s/%%(title)s.%%(id)s.%%(ext)s" ^
--download-archive ScrollGang.txt ^
--format bestaudio/best ^
--extract-audio ^
--audio-format mp3 ^
--audio-quality 160K ^
--embed-thumbnail ^
--restrict-filenames ^
"https://www.youtube.com/c/scroll%%E5%%BF%%8D/videos" ^
!video!
PAUSE
