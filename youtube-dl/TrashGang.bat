@echo off
cd /D "%~dp0"
youtube-dl ^
--ignore-errors ^
--output "I:/Music/Trash/%%(title)s.%%(id)s.%%(ext)s" ^
--download-archive TrashGang.txt ^
--format bestaudio/best ^
--extract-audio ^
--audio-format mp3 ^
--audio-quality 160K ^
--embed-thumbnail ^
--restrict-filenames ^
"https://www.youtube.com/c/TRASH%%E6%%96%%B0%%E3%%83%%89%%E3%%83%%A9%%E3%%82%%B4%%E3%%83%%B3/videos" ^
!video!
PAUSE
