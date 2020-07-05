import json
import os
from typing import Optional

from .. import config
from pymongo import MongoClient, TEXT
from pymongo.collection import Collection

DATABASE_URL = config.DATABASE_URL

if not DATABASE_URL:
    raise EnvironmentError(
        'DATABASE_URL should be provided')

DATABASE_NAME = config.DATABASE_NAME
_client = MongoClient(DATABASE_URL)[DATABASE_NAME]

SONGS = 'songs'
RATINGS = 'ratings'


def initialize():
    _songs_collection = get_collection(SONGS)

    if _songs_collection:
        return _songs_collection

    _songs_collection = _client[SONGS]

    json_path = os.path.join(os.path.dirname(__file__), 'songs.json')

    songs = []
    with open(json_path, 'r') as f:
        for line in f:
            songs.append(json.loads(line))

    _songs_collection.insert_many(songs)

    _songs_collection.create_index(
        [('title', TEXT), ('artist', TEXT)], default_language='english')


def get_collection(collection_name: str,
                   create_if_not_exit: bool = False) -> Optional[Collection]:
    collections = _client.list_collection_names()

    if create_if_not_exit or collection_name in collections:
        return _client[collection_name]


songs_collection = get_collection(SONGS, create_if_not_exit=True)
ratings_collection = get_collection(RATINGS, create_if_not_exit=True)
