#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import json
import multiprocessing
import os.path
import time
from functools import reduce
from typing import List

import mysql.connector
import wget

import secret
from youtube_audio_api import API, TrackType
from youtube_audio_api import TrackOrder, OrderField, OrderDirection

DOWNLOAD_PATH = "/Users/apple/Downloads/ytmusic/"

api = API(secret.channel_id, secret.authorization, secret.cookie)


def mysql_tracks(tracks: List):
    sql = """
REPLACE INTO `creator_audio`(
    `track_id`,
    `title`,
    `artist`,
    `duration`,
    `track_type`,
    `category`,
    `genres`,
    `moods`,
    `instruments`,
    `publish_time`,
    `viper_id`,
    `license_type`,
    `external_artist_url`
)
VALUES(
    %(track_id)s,
    %(title)s,
    %(artist)s,
    %(duration)s,
    %(track_type)s,
    %(category)s,
    %(genres)s,
    %(moods)s,
    %(instruments)s,
    %(publish_time)s,
    %(viper_id)s,
    %(license_type)s,
    %(external_artist_url)s
);
 """
    cnx = mysql.connector.connect(user='youtube', password='youtubeyoutube',
                                  host='127.0.0.1',
                                  database='youtube')
    cursor = cnx.cursor()

    for track in tracks:
        data = {
            "track_id": track.get("trackId"),
            "title": track.get("title"),
            "artist": track.get("artist"),
            "duration": int(track.get("duration", {}).get("seconds", 0)),
            "category": track.get("attributes", {}).get("category"),
            "genres": track.get("attributes", {}).get("genres"),
            "moods": track.get("attributes", {}).get("moods"),
            "instruments": track.get("attributes", {}).get("instruments"),
            "publish_time": datetime.datetime.fromtimestamp(int(track.get("publishTime", {}).get("seconds", 0))),
            "viper_id": track.get("viperId"),
            "license_type": track.get("licenseType"),
            "external_artist_url": track.get("externalArtistUrl")
        }
        if data["artist"] is not None:
            data["artist"] = json.dumps(data["artist"])
        if data["category"] is not None and data["category"] != "":
            data["track_type"] = TrackType.SOUNDEFFECT.value
        else:
            data["track_type"] = TrackType.MUSIC.value
        if data["genres"] is not None:
            data["genres"] = json.dumps(data["genres"])
        if data["moods"] is not None:
            data["moods"] = json.dumps(data["moods"])
        if data["instruments"] is not None:
            data["instruments"] = json.dumps(data["instruments"])

        cursor.execute(sql, data)
        cnx.commit()

    cursor.close()
    cnx.close()


def download_tracks(track_ids: list[str]):
    for track_id in track_ids:

        tmp_fname = DOWNLOAD_PATH + track_id + "." + str(
            reduce(lambda x, y: x + y, [c for c in "l" + track_id if c.islower()]))
        fname = tmp_fname + ".mp3"
        if os.path.exists(fname):
            print("downloaded " + fname)
            continue

        while True:
            try:
                resp = api.get_tracks([track_id])
                tracks = resp.get("tracks")
                if tracks is not None and len(tracks) > 0:
                    for track in tracks:
                        track_id = track.get("trackId")

                        tmp_fname = DOWNLOAD_PATH + track_id + "." + str(
                            reduce(lambda x, y: x + y, [c for c in "l" + track_id if c.islower()]))
                        fname = tmp_fname + ".mp3"
                        if os.path.exists(fname):
                            print("downloaded " + fname)
                            continue

                        track_url = track.get("streamingAudioUrl")
                        print("downloading " + tmp_fname)
                        wget.download(track_url, out=tmp_fname)
                        os.rename(tmp_fname, fname)
                        print("downloaded " + fname)
                break
            except Exception as e:
                print(e)


def track_list_gen() -> List:
    page_token = None
    while True:
        resp = api.list_tracks(track_type_in=[TrackType.MUSIC, TrackType.SOUNDEFFECT],
                               track_order=TrackOrder(orderField=OrderField.TRACK_TITLE,
                                                      orderDirection=OrderDirection.ASC),
                               page_token=page_token, page_size=50)
        page_token = resp.get("pageInfo", {}).get("nextPageToken")
        total_size = int(resp.get("pageInfo", {}).get("totalSizeInfo", {}).get("size", 0))
        print("total_size=", total_size, "  page_token=", page_token)

        tracks = resp.get("tracks")
        if tracks is not None and len(tracks) > 0:
            yield tracks
        if page_token is None or page_token == "" or total_size <= 0:
            break


def main():
    pool = multiprocessing.Pool(8)

    track_gen = track_list_gen()

    for tracks in track_gen:
        mysql_tracks(tracks)

        while pool._taskqueue.qsize() > 8:
            time.sleep(1)

        track_ids = [t["trackId"] for t in tracks]
        pool.apply_async(download_tracks, args=(track_ids,))

    print('Waiting for all subprocesses done...')
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
