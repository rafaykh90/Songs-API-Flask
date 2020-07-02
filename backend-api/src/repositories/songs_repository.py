import re
from bson import ObjectId

from ..db.songs_iterator import SongsIterator
from ..db.db import songs_collection, ratings_collection
from ..utils.calculations import get_average


def get_songs_data(page: int, limit: int) -> list:
    aggregator = SongsIterator(songs_collection).select_fields(
        _id=1,
        title=1,
        level=1,
        artist=1,
        ratings=1,
        released=1,
        difficulty=1,
    ).join_ratings()

    if page:
        if page > 0:
            aggregator.skip((page - 1) * limit).limit(limit)
    
    if limit:
        aggregator.limit(limit)

    data = []
    for song in aggregator.evaluate():
        ratings = song.pop('ratings', None)
        data.append({
            'id': str(song.pop('_id')),
            'rating': get_average(ratings, key='value') if ratings else 0,
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

    data = SongsIterator(songs_collection).filter(**where).select_fields(
        title=1,
        level=1,
        artist=1,
        ratings=1,
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
        map(lambda song: song['difficulty'], songs_collection.find(where, fields)))

    average = get_average(songs) if songs else 0

    return {'average': average}


def add_song_rating(data: any) -> dict:
    song_id = ObjectId(data.get('song_id', ''))

    if not list(songs_collection.find({'_id': {'$exists': True, '$in': [song_id]}})):
        return None

    rating = int(data.get('rating'))

    item_to_insert = {
        'value': rating,
        'song_id': song_id,
    }
    ratings_collection.insert(item_to_insert)

    return item_to_insert


def get_song_metrics(song_id):
    _count = 0
    _sum = 0
    _max = 0
    _min = 0

    aggregator = SongsIterator(songs_collection).join_ratings()

    song = aggregator.filter(_id=ObjectId(song_id)).select_fields(
        _id=0, ratings=1).first().evaluate()

    if not song:
        return None

    for rating in song['ratings']:
        # Didn't investigate the issue of different types
        rating_value = rating['value'] if isinstance(rating, dict) else rating
        _count += 1
        _sum += rating_value
        _max = _max if _max > rating_value else rating_value
        _min = _min if _min < rating_value else rating_value

    avg = round(_sum / _count, 2) if _count else 0

    return {
        'min': _min,
        'max': _max,
        'average': avg,
    }
