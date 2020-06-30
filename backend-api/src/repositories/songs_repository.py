import re
from utils.songs_iterator import SongsIterator
from db import get_collection
from utils import get_average
from bson import ObjectId


def get_songs_data(page) -> list:
    aggregator = SongsIterator().select_fields(
        _id=1,
        title=1,
        level=1,
        artist=1,
        # ratings=1,
        released=1,
        difficulty=1,
    ).join_ratings()

    if page:
        if page > 0:
            items_per_page = 10
            aggregator.skip((page - 1) * items_per_page).limit(items_per_page)

    data = []
    for song in aggregator.evaluate():
        # ratings = song.pop('ratings', None)
        data.append({
            'id': str(song.pop('_id')),
            # 'rating': get_average(ratings, key='value') if ratings else None,
            **song,
        })

    return data


def search_song_by_keyword(keyword) -> list:
    search_query = re.compile(keyword, re.IGNORECASE)
    where = {
        '$or': [
            {'title': search_query},
            {'artist': search_query},
        ]
    }

    data = SongsIterator().filter(**where).select_fields(
        title=1,
        level=1,
        artist=1,
        # ratings=1,
        released=1,
        difficulty=1,
    ).evaluate()

    return data


def get_avg_difficulty(level) -> list:
    fields = {'_id': 0, 'difficulty': 1}

    where = {}
    if level:
        where['level'] = level

    # Fetch only id and difficulty fields for songs in level equal to 'level'
    songs = list(
        map(lambda song: song['difficulty'], get_collection('songs').find(where, fields)))

    average = get_average(songs) if songs else 0

    return {'average': average}


def add_song_rating(data: any) -> any:
    song_id = ObjectId(data.get('song_id', ''))

    if not get_collection('songs').find({'_id': {'$exists': True, '$in': [song_id]}}):
        return
