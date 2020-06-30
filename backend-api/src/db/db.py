import json
import os
import re
from typing import Optional

import config

from pymongo import MongoClient, TEXT
from pymongo.collection import Collection

DATABASE_URL = config.DATABASE_URL

if not DATABASE_URL:
    raise EnvironmentError(
        'DATABASE_URL is required to be set in the environment')

DATABASE_NAME = config.DATABASE_NAME
DB_CONNECTION = MongoClient(DATABASE_URL)[DATABASE_NAME]


def initialize():
    collection = get_collection('songs')

    if collection:
        return collection

    collection = DB_CONNECTION['songs']

    json_path = os.path.join(os.path.dirname(__file__), 'songs.json')

    songs = []
    with open(json_path, 'r') as f:
        for line in f:
            songs.append(json.loads(line))

    collection.insert_many(songs)

    collection.create_index(
        [('title', TEXT), ('artist', TEXT)], default_language='english')


def get_collection(collection_name: str, create_if_not_exit: bool = False) -> Optional[Collection]:
    collections = DB_CONNECTION.collection_names()

    if create_if_not_exit or collection_name in collections:
        return DB_CONNECTION[collection_name]


songs_collection = get_collection('songs', create_if_not_exit=True)
ratings_collection = get_collection('ratings', create_if_not_exit=True)
