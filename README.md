# AutoTag
Tool that uses shazamAPI to edit metadatas

**autotag_core**
Executing this file won't do anything, it just contains all base functions.
*Dependencies:*
`requests`
`music_tag`
`pydub`


**autotag_folder**

*Usage:*
Put your audio files in Sources folder and run `python3 autotag_folder.py`. 
Metadatas will be changed on existing audio files, not creating duplicates.


**autotag_dl**

*Aditionnal dependencies:* `pyperclip` `youtube_dl` `time`

*Usage:*
Start the program using `python3 autotag_dl.py` and Ctrl+C youtube links to automatically download and correct metadata on it.
Note that to stop the process you can Ctrl+C `exit`.
