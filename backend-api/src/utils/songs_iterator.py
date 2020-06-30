from pymongo.cursor import Cursor

from db import get_collection

songs_collection = get_collection('songs')

class SongsIterator:
    iter = None
    _limit = 0
    _skip = 0
    _where = {}
    _lookup = {}
    _columns = {}
    _first = False

    def __init__(self, cursor: Cursor = None):
        self.iter = cursor

    def __aggregate(self):
        cursor = self.iter or songs_collection
        items = []

        if self._skip:
            items.append({'$skip': self._skip})
        if self._limit:
            items.append({'$limit': self._limit})
        if self._where:
            items.append({'$match': self._where})
        if self._lookup:
            items.append({'$lookup': self._lookup})
        if self._columns:
            items.append({'$project': self._columns})

        result = cursor.aggregate(items)

        if self._first:
            for first_result in result:
                return first_result
        else:
            return result

    def evaluate(self) -> Cursor:
        if self._lookup:
            return self.__aggregate()

        lookup = songs_collection.find_one if self._first else songs_collection.find

        cursor = lookup(self._where, self._columns)

        if self._skip:
            cursor = cursor.skip(self._skip)
        if self._limit:
            cursor = cursor.limit(self._limit)

        return cursor

    def skip(self, number: int) -> 'SongsIterator':
        self._skip = number
        return self

    def first(self) -> 'SongsIterator':
        self._first = True
        return self

    def filter(self, **where) -> 'SongsIterator':
        self._where.update(where)
        return self

    def limit(self, number: int) -> 'SongsIterator':
        self._limit = number
        return self

    def join_ratings(self) -> 'SongsIterator':
        self._lookup = {
            'from': 'ratings',
            'localField': '_id',
            'foreignField': 'song_id',
            'as': 'ratings',
        }
        return self

    def select_fields(self, **fields) -> 'SongsIterator':
        self._columns.update(fields)
        return self
