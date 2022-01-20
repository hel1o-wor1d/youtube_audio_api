#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime

from meta import TrackOrder, OrderField, OrderDirection, TrackType
from youtube_audio_api.api import Api

if __name__ == '__main__':

    import mysql.connector

    cnx = mysql.connector.connect(user='youtube', password='youtubeyoutube',
                                  host='127.0.0.1',
                                  database='youtube')
    cursor = cnx.cursor()
    sql = "INSERT INTO creator_music(track_id, title, artist, duration, track_type, " \
          "category, genres, moods, instruments, streaming_audio_url, publish_time, " \
          "viper_id, license_type, external_artist_url) VALUES (%(track_id)s, %(title)s, %(artist)s, %(duration)s," \
          " %(track_type)s, %(category)s, %(genres)s, %(moods)s, %(instruments)s, %(streaming_audio_url)s," \
          " %(publish_time)s, %(viper_id)s, %(license_type)s, %(external_artist_url)s)"

    api = Api("jjjjjjjjjjjj",
              "SAPISIDHASH",
              "HomRayC4OraJTj6")
    track_order = TrackOrder(orderField=OrderField.TRACK_TITLE, orderDirection=OrderDirection.ASC)
    page_token = None
    total_size = 1
    while True:
        resp = api.list_sound_effect(track_order=track_order, page_token=page_token, page_size=50)
        if "tracks" in resp and len(resp["tracks"]) > 0:
            trackIds = []
            for t in resp["tracks"]:
                trackIds.append(t["trackId"])
            tt = api.get_tracks(trackIds)
            print(json.dumps(tt))
            if "tracks" in tt and len(tt) > 0:
                for t in tt["tracks"]:
                    data = {
                        "track_id": t.get("trackId"),
                        "title": t.get("title"),
                        "artist": json.dumps(t.get("artist")),
                        "duration": t.get("duration").get("seconds"),
                        "track_type": TrackType.SOUNDEFFECT.value,
                        "category": t.get("attributes").get("category"),
                        "genres": json.dumps(t.get("attributes").get("genres")),
                        "moods": json.dumps(t.get("attributes").get("moods")),
                        "instruments": json.dumps(t.get("attributes").get("instruments")),
                        "streaming_audio_url": t.get("streamingAudioUrl"),
                        "publish_time": datetime.fromtimestamp(int(t.get("publishTime").get("seconds"))),
                        "viper_id": t.get("viperId"),
                        "license_type": t.get("licenseType"),
                        "external_artist_url": t.get("externalArtistUrl")
                    }
                    cursor.execute(sql, data)
                    cnx.commit()
        page_token = None
        if "pageInfo" in resp and "nextPageToken" in resp["pageInfo"]:
            page_token = resp["pageInfo"]["nextPageToken"]
        total_size = 0
        if "pageInfo" in resp and "totalSizeInfo" in resp["pageInfo"] and "size" in resp["pageInfo"]["totalSizeInfo"]:
            total_size = int(resp["pageInfo"]["totalSizeInfo"]["size"])

        print("total_size=", total_size, "  page_token=", page_token)

        if page_token is None or page_token == "" or total_size <= 0:
            break

    cursor.close()
    cnx.close()
