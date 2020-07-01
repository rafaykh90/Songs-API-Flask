import json
from functools import reduce
from http import HTTPStatus
from typing import List, Union, Dict, Any

from bson.json_util import dumps as mongo_dumps
from bson.json_util import loads
from flask import jsonify
from flask.wrappers import Response as FlaskResponse
from pymongo.cursor import Cursor


class Response:
    def __init__(self, data: Union[str, Dict[str, Any], List[Any], Cursor]):
        self.data = data

    def json(self, error=False) -> FlaskResponse:
        data = json.loads(mongo_dumps(self.data)) if isinstance(
            self.data, Cursor) else self.data
        # data = {'message': data} if error else data
        return jsonify(data)

    @staticmethod
    def created() -> tuple:
        return '', HTTPStatus.CREATED
