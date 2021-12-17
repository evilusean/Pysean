"""
Save it in a file named getvideo.py and run it like py -3 getvideo.py AjFfsOA7AQI 3dDtACSYVx0 G17E4Muylis to download all three videos!
used in cmd
"""
import sys
from youtube_dl import YoutubeDL

if __name__ == '__main__':
    if len(sys.argv) > 1:
        ydl_opts = {}
        ydl = YoutubeDL(ydl_opts)
        ydl.download(sys.argv[1:])
    else:
        print("Enter list of urls to download")
        exit(0)
