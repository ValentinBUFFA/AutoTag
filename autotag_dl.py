from autotag_core import *
import youtube_dl
from youtube_dl.postprocessor.common import PostProcessor
import pyperclip
import time

audio_format = 'mp3'
audio_quality = '192'


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


class AutotagPP(PostProcessor):
    def run(self, information):
        print("Download complete, now fetching metadatas.")
        output_filename = information['filepath']

        infos = GetInfo(output_filename)
        if infos[0] == 'null':
            print(f"Couldn't find data for file {file}")
        dl_art(infos[2])
        set_metadata(output_filename, infos)

        print(f"Downloaded {infos[0]} by {infos[1]}")
        print("\n")
        return [], information


ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '/Downloaded/%(title)s.%(ext)s',
    'logger': MyLogger(),
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': audio_format,
        'preferredquality': audio_quality,
    }]}

ydl = youtube_dl.YoutubeDL(ydl_opts)
ydl.add_post_processor(AutotagPP(None))
pyperclip.copy("")
clipboard = ""
while clipboard != "exit":
    clipboard = pyperclip.paste()
    if 'youtube.com' in clipboard:
        try:
            print(f"Downloading {clipboard}")
            print('\n')
            ydl.download([clipboard])
        except:
            print("Downloading error. URL might be incorrect or not supported yet.")
            pyperclip.copy("")
            continue
        pyperclip.copy("")
    time.sleep(1)
