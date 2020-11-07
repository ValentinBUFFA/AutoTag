from autotag_core import *
import youtube_dl
import pyperclip
import time

audio_format = 'mp3'
audio_quality = '192'


def get_output_filename(d):
    if d['status'] == 'finished':
        global output_filename
        output_filename = d['filename']


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '/Downloaded/%(title)s.%(ext)s',
    'progress_hooks': [get_output_filename],
    'logger': MyLogger(),
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': audio_format,
        'preferredquality': audio_quality,
    }]}

ydl = youtube_dl.YoutubeDL(ydl_opts)
pyperclip.copy("")
clipboard = ""
while clipboard != "exit":
    clipboard = pyperclip.paste()
    if 'youtube.com' in clipboard:
        try:
            print(f"Downloading {clipboard}")
            ydl.download([clipboard])
        except:
            print("Downloading error. URL might be incorrect or not supported yet.")
            pyperclip.copy("")
            continue
        print("Download complete, now fetching metadatas.")
        output_filename = os.path.splitext(output_filename)[0] + "." + audio_format

        infos = GetInfo(output_filename)
        if infos[0] == 'null':
            print(f"Couldn't find data for file {file}")
        dl_art(infos[2])
        set_metadata(output_filename, infos)

        print(f"Downloaded {infos[0]} by {infos[1]}")
        pyperclip.copy("")

    time.sleep(1)
