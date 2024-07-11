from flask import Flask, request
from service.collaborative_filtering_service import CollaborativeFilteringService
app = Flask(__name__)

cfs = CollaborativeFilteringService()

@app.route("/collaborative_filtering/movie-movie")
def get_movie_movie_top_n():
    count = request.args.get('count')
    user_id = request.args.get('userId')
    return cfs.get_movie_movie_top_n(user_id, count)