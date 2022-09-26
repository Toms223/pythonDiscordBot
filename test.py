import json

from pytube import Playlist
from yt_dlp import YoutubeDL
import time

if __name__ == '__main__':
    """start = time.time()
    playlist = Playlist("https://www.youtube.com/watch?v=TZXdeumQFGE&list=PLFBHIu8sTMFKLxamcXnWmRmRhxWxmcsu6")
    playlist = playlist.videos
    for video in playlist:
        print(video.title)
    print(f"Done in {time.time() - start}")"""
    start = time.time()
    ydl_opts = ydl_opts = {
        'format': 'm4a/bestaudio/best',
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }
    url = ["https://www.youtube.com/watch?v=TZXdeumQFGE&list=PLFBHIu8sTMFKLxamcXnWmRmRhxWxmcsu6"]
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)
    print(f"Done in {time.time() - start}")
