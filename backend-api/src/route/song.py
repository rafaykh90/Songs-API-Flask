import re

from bson import ObjectId, errors as bsonErrors
from flask import Blueprint, request, jsonify, abort, json
from werkzeug.exceptions import HTTPException

from ..repositories import songs_repository
from ..utils.response import Response

api = Blueprint('songs', __name__)


@api.errorhandler(HTTPException)
def resource_not_found(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

# get_songs
#   Returns the list of songs as JSON using pagination
@api.route('/api/songs/', methods=['GET'])
def get_songs():
    page = request.args.get('page')
    limit = request.args.get('limit')

    try:
        if page:
            page = int(page)

        if limit:
            limit = int(limit)

        data = songs_repository.get_songs_data(page, limit)

        return Response(data).json()
    except ValueError:
        abort(400, description="Invalid query params")
    except Exception:
        abort(500, description="Error getting songs data")

# get_average_difficulty
#   Retruns the average difficulty for songs along with an optional parameter 'level' to select songs from particular level
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


# search_by_keyword
#   Returns a list of songs based on the query param 'message' which is searched in artist or title field
#   Returns empty list of 'message' param is empty or not present
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

# post_rating
#   Provides an API to add rating for a songs
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


# average_rating
#   Return a JSON object containing the average rating, max rating and min rating for a song
@api.route('/api/songs/avg/rating/<string:song_id>/', methods=['GET'])
def average_rating(song_id):
    try:
        response = songs_repository.get_song_metrics(song_id)

        if not response:
            abort(404, description="Songs with Id {} not found".format(song_id))

        return Response(response).json()
    except bsonErrors.InvalidId:
        abort(400, description="'songs_id' value is invalid")
