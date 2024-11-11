'docker compose up' from this directory, will take all files in the 'data/audio/temp' and first transcribe them, translate them, and then combine them in this format:</br>
[TimeStamp] - Hiragana/Kanji(Japanese Letters) - Romaji(romanized Japanese) - English Translation</br>
I also created a bash script that will allow you to launch it from any terminal, it will upload the translations as soon as they are done to the terminal as well. You can run it with the command :</br>
'translasean -jp -rt -m' #will run the file '/src/realtime-mic.py' and translate in real time, from the computer microphone  </br>
'translasean -sk -rt -m' #same as above, but for slovakian</br>
'translasean -jp -yt YOUTUBE_URL' #replace the <Youtube URL> with your own and it will download the audio, transcribe it, translate it, and combine it, then save the audio file for later</br>
'translasean -sk -yt -p YOUTUBE_PLAYLIST_URL' #will transcribe, translate, combine with timestamps, in slovakian an entire youtube playlist</br>
Having some trouble with the streaming from my linux PC to translation, goes too slow and lags out where the audio doesn't work and becomes unintelligible, future Sean problem </br>
the main functionality works, but I've only put 2 days into it(outside of learning python/docker/STT Models). It could still use some polish, and more work, but overall, I'm happy with it for now, cool project</br>
