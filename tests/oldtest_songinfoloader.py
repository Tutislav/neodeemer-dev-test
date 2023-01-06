import os
import sys
import tempfile
import unittest
import time
from yt_dlp import YoutubeDL

sys.path.append(os.path.abspath("../neodeemer"))
sys.path.append(os.path.abspath("../neodeemer/neodeemer"))
os.chdir(os.path.abspath("../neodeemer/neodeemer"))
from neodeemer.songinfoloader import SpotifyLoader
from neodeemer.tools import TrackStates


class MDLabel():
    text = ""

class TestSongInfoLoader(unittest.TestCase):
    label_loading_info = MDLabel()
    s = SpotifyLoader("CZ", tempfile.mkdtemp(), True, label_loading_info)

    def test_a_track_find_video_id(self):
        soucet = 0
        max = 0
        tracks = [
            ["KABÁT Dole v dole", "HVK1Pxl2ZvI"],
            ["Dymytry Černí Andělé", "lERlw3gWR_8"],
            ["Trautenberk Ticho nad pekáčem", "kz9KPrzMZ9A"],
            ["Morčata Na Útěku Outro", "l1mA5Mry268"],
            ["TRAKTOR Amygdala", "YQcGUGmXGvw"],
            ["Laura Branigan Self Control", "Ucmo6hDZRSY"],
            ["Journey Don't Stop Believin'", "PIFUWHvSixw"],
            ["Wanastovi Vjeci Otevrena zlomenina srdecniho svalu", "yH4BnE2S3Vo"],
            ["Imagine Dragons Enemy", "IOrbP1OqNsg"],
            ["Jason Charles Miller Rules of Nature", "jOpzP33_USs"],
            ["Lynyrd Skynyrd Sweet Home Alabama", "4FUBK4r2fzI"],
            ["Harlej Hodný holky zlý kluky chtěj", "94ISFE-s2qo"],
            ["Dymytry Strazna Vez", "qVgG_s2n6LM"],
            ["Sweet The Ballroom Blitz", "4Jar6gxlbFs"],
            ["a-ha Take on Me", "HzdD8kbDzZA"],
            ["Morčata na útěku Máme je krátký", "zRifScA_EOA"],
            ["Mr. President Coco Jamboo", "_Jl-QpJNKiQ"]
        ]
        for track in tracks:
            start = time.time()
            track_dict = (self.s.tracks_search(track[0]))[0]
            print((track_dict["artist_name"] + " - " + track_dict["track_name"]).ljust(50, " "), end=" ")
            self.s.track_find_video_id(track_dict)
            if track_dict["state"].value != TrackStates.UNAVAILABLE.value:
                print("https://youtu.be/" + track_dict["video_id"] + " | " + track[1])
                self.assertEqual(track_dict["video_id"], track_dict["video_id"])
                cas = (time.time() - start)
                soucet += cas
                if cas > max:
                    max = cas
                print("--- %s s ---" % cas)
            else:
                print("UNAVAILABLE")
        prumer = soucet / 17
        print("--- PRUMER %s s ---" % prumer)
        print("--- MAX %s s ---" % max)

    def test_b_playlist_tracks(self):
        playlist_id = "1ZcxlfLrehWkhM3ac1ghOR"
        print("Loading playlist...")
        tracks = self.s.playlist_tracks(playlist_id)
        print("Playlist loaded.")
        with open("../tests/test_songinfoloader.log", "w", encoding="utf-8") as log_file:
            with YoutubeDL({"quiet": True}) as ydl:
                for track in tracks:
                    print((track["artist_name"] + " - " + track["track_name"]).ljust(50, " "), end=" ")
                    self.s.track_find_video_id(track)
                    if track["state"].value != TrackStates.UNAVAILABLE.value:
                        video_url = "https://youtu.be/" + track["video_id"]
                        print(video_url.ljust(35, " "), end=" ")
                        video_info = ydl.extract_info(video_url, False)
                        print(video_info["uploader"] + " - " + video_info["title"])
                        log_file.write((track["artist_name"] + " - " + track["track_name"]).ljust(50, " ") + video_url.ljust(35, " ") + video_info["uploader"] + " - " + video_info["title"] + "\n")
                        #log_file.write(video_url + "\n")
                        self.assertTrue(len(track["video_id"]) > 0)
                    else:
                        print("UNAVAILABLE")

if __name__ == "__main__":
    unittest.main(verbosity=2)
