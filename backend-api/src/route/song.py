import re

from bson import ObjectId, errors as bsonErrors
from flask import Blueprint, request, jsonify, abort

# import repositories.songs_repository as songs_repository
from ..repositories import songs_repository
from ..utils.response import Response

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
        pass  # page param not present

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


@ api.route('/api/songs/rating', methods=['POST'])
def post_rating():
    data = request.json

    try:
        rating = int(data.get('rating'))
        if 1 > rating or rating > 5:
            raise ValueError()

        response = songs_repository.add_song_rating(data)
        if not response:
            abort(404, description="Songs with Id {} not found".format(
                data.get('song_id')))

        return Response.created()

    except ValueError:
        abort(400, description="'rating' param invalid")
    except TypeError:
        abort(400, description="'rating' param required")
    except bsonErrors.InvalidId:
        abort(400, description="'songs_id' value is invalid")


@api.route('/api/songs/avg/rating/<string:song_id>/', methods=['GET'])
def average_rating(song_id):
    try:
        response = songs_repository.get_song_metrics(song_id)

        if not response:
            abort(404, description="Songs with Id {} not found".format(song_id))

        return Response(response).json()
    except bsonErrors.InvalidId:
        abort(400, description="'songs_id' value is invalid")
