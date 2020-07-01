from src.db import songs_collection, ratings_collection
from src.app import app
from src.route.song import get_songs, search_by_keyword, get_average_difficulty, post_rating, average_rating