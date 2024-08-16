import flask
from api.service.collaborative_filtering_service import CollaborativeFilteringService
from api.service.matrix_factorization_service import MatrixFactorizationService
from api.service.dnn_service import DNNService

app = flask.Flask(__name__)

cfs = CollaborativeFilteringService()
mfs = MatrixFactorizationService()
dnns = DNNService()


@app.route("/collaborative-filtering/movie-movie")
def get_movie_movie_top_n():
    user_id = flask.request.args.get('userId')
    count = flask.request.args.get('count')
    return flask.jsonify(cfs.get_movie_movie_top_n(user_id, count))


@app.route("/collaborative-filtering/user-user")
def get_user_user_top_n():
    user_id = flask.request.args.get('userId')
    count = flask.request.args.get('count')
    return flask.jsonify(cfs.get_user_user_top_n(user_id, count))


@app.route("/matrix-factorization/ALS")
def get_top_n_movies_for_user():
    user_id = flask.request.args.get('userId')
    count = flask.request.args.get('count')
    return flask.jsonify(mfs.get_top_n_movies_for_user_bmfr(user_id, count))


@app.route("/deep-neural-network")
def get_deep_neural_network_rating():
    user_id = flask.request.args.get('userId')
    count = flask.request.args.get('count')
    return flask.jsonify(dnns.get_top_n_movies_for_user(user_id, count))


@app.route("/deep-neural-network/batch")
def get_deep_neural_network_rating_batch():
    user_id = flask.request.args.get('userId')
    count = flask.request.args.get('count')
    return flask.jsonify(dnns.get_top_n_movie_for_user_batch(user_id, count))
