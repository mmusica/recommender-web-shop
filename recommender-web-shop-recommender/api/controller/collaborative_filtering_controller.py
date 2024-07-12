import flask
from api.service.collaborative_filtering_service import CollaborativeFilteringService

app = flask.Flask(__name__)

cfs = CollaborativeFilteringService()


@app.route("/collaborative_filtering/movie-movie")
def get_movie_movie_top_n():
    user_id = flask.request.args.get('userId')
    count = flask.request.args.get('count')
    return flask.jsonify(cfs.get_movie_movie_top_n(user_id, count))
