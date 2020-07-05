from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from .route.song import api
from .db import db
from . import config
from .utils import error_handler

app = Flask(__name__)
app.debug = config.DEBUG

CORS(app)

db.initialize()

app.register_error_handler(HTTPException, error_handler.handle_exception)
app.register_blueprint(api)
