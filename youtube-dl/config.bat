#downloads channel using config.txt parameters as video
cd /D "%~dp0"
youtube-dl https://www.youtube.com/user/EngineeringExplained/videos --config-location config.txt
PAUSE
