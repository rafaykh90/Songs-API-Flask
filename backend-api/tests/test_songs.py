from http import HTTPStatus
from werkzeug.exceptions import HTTPException

import pytest

from . import songs_collection, ratings_collection
from . import app
from . import get_songs, search_by_keyword, get_average_difficulty, post_rating, average_rating


class TestSongs:
    def test_get_songs_returns_ok_status(self, mocker):
        mocker.patch.object(songs_collection, 'find',
                            return_value=[{'_id': 'some_id'}])

        with app.test_request_context():
            response = get_songs()

        assert HTTPStatus.OK == response.status_code

    def test_get_songs_returns_data(self, mocker):

        # Arrange
        data = [{'_id': 'some_id', 'ratings': []}]
        mocker.patch.object(songs_collection, 'aggregate', return_value=data)

        # Act
        with app.test_request_context():
            response = get_songs()

        # Assert
        assert response.json == [{'id': 'some_id', 'rating': None}]

    def test_get_songs_wrong_parameter_bad_request_status(self, mocker):
        with app.test_request_context() as context:
            context.request.args = {'page': 'somgstring'}
            with pytest.raises(HTTPException) as httperror:
                get_songs()
            assert 400 == httperror.value.code

        with app.test_request_context() as context:
            context.request.args = {'limit': 'stringabc'}
            with pytest.raises(HTTPException) as httperror:
                get_songs()
            assert 400 == httperror.value.code

    def test_search_songs_ok_status(self, mocker):
        # Act
        with app.test_request_context() as context:
            context.request.args = {'message': 'text'}

            response = search_by_keyword()

        # Assert
        assert response.status_code == HTTPStatus.OK

    def test_search_songs_returns_data(self, mocker):
        # Arrange
        data = [{'key': 'value'}]
        mocker.patch.object(songs_collection, 'find', return_value=data)

        # Act
        with app.test_request_context() as context:
            context.request.args = {'message': 'text'}
            response = search_by_keyword()

        # Assert
        assert response.json == data

    def test_search_songs_no_message_empty_list(self, mocker):
        # Act
        with app.test_request_context() as context:
            context.request.args = {}
            response = search_by_keyword()

        # Assert
        assert response.json == []

    def test_search_songs_empty_message_empty_list(self, mocker):
        # Act
        with app.test_request_context() as context:
            context.request.args = {'message': ''}
            response = search_by_keyword()

        # Assert
        assert response.json == []

    def test_get_avg_difficulty_ok_status(self, mocker):
        # Act
        with app.test_request_context() as context:
            context.request.args = {}
            response = get_average_difficulty()

        assert response.status_code == HTTPStatus.OK

    def test_get_avg_difficulty_correct_value(self, mocker):
        # Arrange
        data = [{'difficulty': 3}, {'difficulty': 2}, {'difficulty': 1}]
        mocker.patch.object(songs_collection, 'find', return_value=data)

        # Act
        with app.test_request_context() as context:
            context.request.args = {}
            response = get_average_difficulty()

        # Assert
        assert response.json['average'] == 2

    def test_post_rating_without_rating_bad_request(self):
        song_id = '53cb6b9b4f4ddef1ad47f943'

        # Act
        with app.test_request_context(json={'song_id': song_id}):
            with pytest.raises(HTTPException) as httperror:
                post_rating()
            # Assert
            assert 400 == httperror.value.code

    def test_post_rating_out_of_bounds_bad_request(self):
        song_id = '53cb6b9b4f4ddef1ad47f943'

        # Act
        with app.test_request_context(json={'rating': 0, 'song_id': song_id}):
            with pytest.raises(HTTPException) as httperror:
                post_rating()
            # Assert
            assert 400 == httperror.value.code

        with app.test_request_context(json={'rating': 6, 'song_id': song_id}):
            with pytest.raises(HTTPException) as httperror:
                post_rating()
            # Assert
            assert 400 == httperror.value.code

    def test_post_invalid_song_id_bad_request(self, mocker):
        # Arrange
        song_id = '53cb6b9b4f4ddef1ad47'
        mocker.patch.object(songs_collection, 'find', return_value=False)

        # Act
        with app.test_request_context(json={'rating': 3, 'song_id': song_id}):
            with pytest.raises(HTTPException) as httperror:
                post_rating()
            # Assert
            assert httperror.value.code == 400

    def test_get_average_rating_ok_status(self, mocker):
        song_id = '53cb6b9b4f4ddef1ad47f943'
        mocker.patch.object(songs_collection, 'find', return_value=[
                            {'_id': '53cb6b9b4f4ddef1ad47f943', 'ratings': []}])

        mocker.patch.object(songs_collection, 'aggregate', return_value=[
                            {'_id': '53cb6b9b4f4ddef1ad47f943', 'ratings': []}])

        with app.test_request_context(song_id):
            response = average_rating(song_id)

        assert HTTPStatus.OK == response.status_code

    def test_get_average_rating_invalid_songs_id_bad_request(self, mocker):
        song_id = '53cb6b9b4f4ddef1ad47f'
        mocker.patch.object(songs_collection, 'aggregate', return_value=[
                            {'_id': '53cb6b9b4f4ddef1ad47f943', 'ratings': []}])

        # Act
        with app.test_request_context(song_id):
            with pytest.raises(HTTPException) as httperror:
                average_rating(song_id)
            # Assert
            assert httperror.value.code == 400

    def test_get_average_rating_song_id_not_found(self, mocker):
        song_id = '53cb6b9b4f4ddef1ad47f946'
        mocker.patch.object(songs_collection, 'find', return_value=[
                            {'_id': '53cb6b9b4f4ddef1ad47f943', 'ratings': []}])

        # Act
        with app.test_request_context(song_id):
            with pytest.raises(HTTPException) as httperror:
                average_rating(song_id)
            # Assert - Resource not found
            assert httperror.value.code == 404

    def test_get_average_ok_with_response(self, mocker):
        song_id = '53cb6b9b4f4ddef1ad47f943'
        data = [{'_id': '53cb6b9b4f4ddef1ad47f943', 'ratings': [3, 5, 2, 2]}]
        mocker.patch.object(songs_collection, 'find', return_value=data)

        mocker.patch.object(songs_collection, 'aggregate', return_value=data)

        # Act
        with app.test_request_context(song_id):
            response = average_rating(song_id)

        assert 'min' in response.json
        assert 'max' in response.json
        assert 'average' in response.json
        assert response.json['average'] == 3
