import re

from bson import ObjectId
from flask import Blueprint, request, jsonify, abort

import repositories.songs_repository as songs_repository
# from repositories.songs_repository import get_songs_data, search_song_by_keyword
from utils.response import Response

api = Blueprint('songs', __name__)


@api.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@api.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


@api.errorhandler(500)
def server_error(e):
    return jsonify(error=str(e)), 500


@api.route('/api/songs/', methods=['GET'])
def get_songs():
    page = request.args.get('page')

    try:
        page = int(page)
    except ValueError:
        abort(400, description="Query param 'page' value invalid")
    except TypeError: 
        pass # page param not present

    data = songs_repository.get_songs_data(page)

    return Response(data).json()


@api.route('/api/songs/avg/difficulty', methods=['GET'])
def get_average_difficulty():
    level = request.args.get('level')
    try:
        if level:
            level = int(level)
    except ValueError:
        abort(400, description="Query param 'level' value invalid")

    data = songs_repository.get_avg_difficulty(level)

    return Response(data).json()


@api.route('/api/songs/search', methods=['GET'])
def search_by_keyword():
    keyword = request.args.get('message')

    if not keyword:
        return Response([]).json()

    try:
        data = songs_repository.search_song_by_keyword(keyword)
    except Exception:
        abort(500, description="Error searching songs from Db")

    return Response(data).json()


@ api.route('/api/songs/rating/', methods=['POST'])
def post_rating():
    data = request.json

    try:
        rating = int(data.get('rating'))  # Raises value error
        if 1 > rating or rating > 5:
            raise ValueError()
    except ValueError:
        return Response('Invalid valid for "rating" param.').bad_request()
    except TypeError:
        return Response('Required "rating" not sent').bad_request()

    ratings_collection.insert({
        'value': rating,
        'song_id': song_id,
    })

    return Response.no_content()


@ api.route('/api/songs/avg/rating/<string:song_id>/', methods=['GET'])
def average_rating(song_id):
    pass
