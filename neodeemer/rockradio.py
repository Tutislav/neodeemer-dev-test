import json
import os
import sys
import time
from urllib import request

sys.path.append(os.getcwd())
sys.path.append(os.path.abspath("neodeemer"))
if not os.path.exists("main.py"):
    os.chdir("neodeemer")
from neodeemer.download import Download
from neodeemer.songinfoloader import SpotifyLoader


download_queue_info = {
    "position": 0,
    "downloaded_b": 0,
    "total_b": 0
}
s = SpotifyLoader("CZ", "/home/pi/rockradio/music", True)
tracks = []

while True:
    acas = "\033[33m" + "[" + time.strftime("%H:%M:%S %d.%m.%y", time.localtime()) + "]" + "\033[0m"
    try:
        with request.urlopen("https://data.radia.cz/data/pravehraje/new-95-currentnext.json") as urldata:
            data = json.loads(urldata.read().decode())
            current = data["current"]
            artist_name = current["interpret"]
            track_name = current["song"]
            text = artist_name + " " + track_name
            if not text in tracks:
                tracks.append(text)
                print(acas + " Downloading " + artist_name + " - " + track_name)
                track_dict = s.tracks_search(text)[0]
                Download(track_dict, s, download_queue_info).download_track()
    except Exception as e:
        print(acas + " Error " + str(e))
    time.sleep(30)