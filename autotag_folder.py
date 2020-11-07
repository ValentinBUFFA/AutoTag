from autotag_core import *

failed = 0
files = os.listdir("Sources/")
files.pop(files.index('Put your audio files in this folder.txt'))
for file in files:
    infos = GetInfo(os.path.join("Sources", file))
    # If retries cap reached go to next song and note the error in console
    if infos[0] == 'null':
        print(f"Couldn't find data for file {file}")
        failed += 1
        continue
    # Download artwork
    dl_art(infos[2])
    # Set tags
    set_metadata(os.path.join("Sources",file), infos)
    print('\n')

print(f"Process finished, {len(files)-failed}/{len(files)} audio files modified")
