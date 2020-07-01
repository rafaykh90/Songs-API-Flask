from flask import Flask
from flask_cors import CORS

from .route.song import api
from .db import db
from . import config

app = Flask(__name__)
app.debug = config.DEBUG

CORS(app)

db.initialize()

app.register_blueprint(api)
