import requests
import os
import json
import shutil
import base64
import music_tag
from pydub import AudioSegment
url = "https://rapidapi.p.rapidapi.com/songs/detect"
headers = {
    'x-rapidapi-key': '3e7ab7e94emshca396c25538373fp14c862jsna3dd4addf531',
    'content-type': 'text/plain',
    'useQueryString': 'true',
    'x-rapidapi-host': 'shazam.p.rapidapi.com'
}


def GetInfo(file, start, duration, try_nb=0):
    song = AudioSegment.from_file(file)
    # Get song in the right duration and format
    s_slice = song[start:start + duration]
    s_slice.set_sample_width(2)
    s_slice = s_slice.set_frame_rate(44100)
    s_slice = s_slice.split_to_mono()[0]
    # export
    s_slice.export("temp/output.raw", format="raw")

    data = s_slice.raw_data
    payload_bytes = base64.b64encode(data)
    payload = payload_bytes.decode('utf-8')

    with open("temp/output.txt", "w") as b64file:
        b64file.write(payload)
        b64file.close()
    try:
        response = requests.request("POST", url, data=payload, headers=headers)
        text = json.loads(response.text)

        infolist = [text["track"]["title"], text["track"]["subtitle"], text["track"]["images"]["coverarthq"]]
        print(infolist[0])  # Titre
        print(infolist[1])  # Artiste
        print(infolist[2])  # Pochette
    except KeyError:
        if try_nb < 6:
            # If recognition didn't suceed try again with next part of the song
            print("Invalid chunk, retrying")
            infolist = GetInfo(file, start + 3500, 3500, try_nb + 1)
        else:
            # Retries cap to prevent overflowing
            infolist = ['null', 'null', 'null']

    return infolist


for file in os.listdir("Sources/"):
    print('\n')
    infos = GetInfo(os.path.join("Sources", file), 0, 3500)
    # If retries cap reached go to next song and note the error in console
    if infos[0] == 'null':
        print(f"Couldn't find data for file {file}")
        continue
    # Download artwork
    img_url = infos[2]
    art = requests.get(img_url, stream=True)
    if art.status_code == 200:
        art.raw.decode_content
        with open(os.path.join("Artworks", infos[0] + "_art.jpg"), 'wb') as f:
            shutil.copyfileobj(art.raw, f)

    # Set tags
    song = music_tag.load_file(os.path.join("Sources", file))

    song['title'] = infos[0]
    song['artist'] = infos[1]
    with open(os.path.join("Artworks", infos[0] + "_art.jpg"), 'rb') as artwork:
        song['artwork'] = artwork.read()
    song.save()
