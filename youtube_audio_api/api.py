#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import urllib.request
from collections import defaultdict
from typing import List

from .meta import Genre, Mood, LicenseType, TrackOrder, DurationRange, LIST_TRACKS_URL, \
    GET_TRACKS_URL, TrackType, SoundEffectCategory


class Api(object):
    '''
    channel_id: your channel id
    authorization: youtube website http header authorization
    cookie: youtube website http header cookie
    '''

    def __init__(self, channel_id: str, authorization: str, cookie: str):
        self.channel_id = channel_id
        self.authorization = authorization
        self.cookie = cookie

    def list_music(self,
                   page_token: str = None,
                   search_token: str = None,
                   title_contains: str = None,
                   genre_in: List[Genre] = None,
                   mood_in: List[Mood] = None,
                   artist_name_contains: str = None,
                   duration_range: DurationRange = None,
                   license_type_in: List[LicenseType] = None,
                   track_order: TrackOrder = None,
                   page_size: int = 100):
        return self.list_tracks(page_token=page_token,
                                search_token=search_token,
                                title_contains=title_contains,
                                genre_in=genre_in,
                                mood_in=mood_in,
                                artist_name_contains=artist_name_contains,
                                duration_range=duration_range,
                                license_type_in=license_type_in,
                                track_order=track_order,
                                page_size=page_size)

    def list_sound_effect(self,
                          page_token: str = None,
                          search_token: str = None,
                          title_contains: str = None,
                          sound_effect_category_in: List[SoundEffectCategory] = None,
                          duration_range: DurationRange = None,
                          track_order: TrackOrder = None,
                          page_size: int = 100):
        return self.list_tracks(page_token=page_token,
                                search_token=search_token,
                                title_contains=title_contains,
                                sound_effect_category_in=sound_effect_category_in,
                                duration_range=duration_range,
                                track_type_in=[TrackType.SOUNDEFFECT],
                                track_order=track_order,
                                page_size=page_size)

    def list_tracks(self,
                    page_token: str = None,
                    search_token: str = None,
                    title_contains: str = None,
                    sound_effect_category_in: List[SoundEffectCategory] = None,
                    genre_in: List[Genre] = None,
                    mood_in: List[Mood] = None,
                    artist_name_contains: str = None,
                    duration_range: DurationRange = None,
                    license_type_in: List[LicenseType] = None,
                    track_type_in: List[TrackType] = None,
                    track_order: TrackOrder = None,
                    page_size: int = 100) -> dict:

        data = self.create_body()
        if search_token:
            data["filter"]["searchToken"]["value"] = search_token
        if title_contains:
            data["filter"]["titleContains"]["value"] = title_contains
        if sound_effect_category_in:
            data["filter"]["soundEffectCategoryIn"]["values"] = [i.value for i in sound_effect_category_in]
        if genre_in and len(genre_in) > 0:
            data["filter"]["genreIn"]["values"] = [i.value for i in genre_in]
        if mood_in and len(mood_in) > 0:
            data["filter"]["moodIn"]["values"] = [i.value for i in mood_in]
        if artist_name_contains:
            data["filter"]["artistNameContains"]["value"] = artist_name_contains
        if duration_range:
            if duration_range.start:
                data["filter"]["durationRange"]["start"]["value"] = duration_range.start
            if duration_range.end:
                data["filter"]["durationRange"]["end"]["value"] = duration_range.end
        if license_type_in:
            data["filter"]["licenseTypeIn"]["values"] = [i.value for i in license_type_in]
        if track_type_in:
            data["filter"]["trackTypeIn"]["values"] = [i.value for i in track_type_in]
        if track_order:
            if track_order.orderField:
                data["trackOrder"]["orderField"] = track_order.orderField.value
            if track_order.orderDirection:
                data["trackOrder"]["orderDirection"] = track_order.orderDirection.value
        if page_size < 1 or page_size > 100:
            page_size = 100
        data["pageInfo"]["pageSize"] = page_size
        if page_token:
            data["pageInfo"]["pageToken"] = page_token

        body = json.dumps(data)

        req = self.get_request(LIST_TRACKS_URL, body.encode("utf-8"))

        resp = urllib.request.urlopen(req)
        obj = json.loads(resp.read().decode())
        return obj

    def get_tracks(self, track_ids: List[str]) -> dict:
        data = self.create_body()
        data["trackIds"] = track_ids
        data["mask"]["includeStreamingUrl"] = True

        body = json.dumps(data)

        req = self.get_request(GET_TRACKS_URL, body.encode("utf-8"))

        resp = urllib.request.urlopen(req)
        obj = json.loads(resp.read().decode())

        return obj

    def get_request(self, url: str, data: bytes) -> urllib.request.Request:
        return urllib.request.Request(url,
                                      data=data,
                                      headers={
                                          "Authorization": self.authorization,
                                          "Cookie": self.cookie,
                                          "Origin": "https://studio.youtube.com",
                                          "Content-Type": "application/json",
                                          "X-Goog-AuthUser": "1"
                                      },
                                      method="POST")

    def create_body(self) -> defaultdict:
        mydict = lambda: defaultdict(mydict)
        data = mydict()
        data["channelId"] = self.channel_id
        data["context"]["client"]["clientName"] = 62
        data["context"]["client"]["clientVersion"] = "1.20220112.02.00"
        return data
