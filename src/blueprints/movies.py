from flask import Blueprint, jsonify, request
from src.models import Movies


movies_bp = Blueprint('movies', __name__, url_prefix='/movies')


@movies_bp.route('/')
def movies_home():
    """
    fetches the entire dataset of movies
    in the video club

    Returns:
        json: list that contains all the movies
    """

    movies = Movies.query.all()

    return jsonify(movies=[movie.to_json() for movie in movies])


@movies_bp.route('/category', methods=['POST'])
def movie_by_category():
    """
    fetches movies by category id.

    receives an integer and searches
    the database in order to fetch
    the filtered dataset.

    POST DATA:
        category (int): category id

    Returns:
        json: list of filtered movies
    """

    category = request.get_json().get("category")
    movies = Movies.query.filter_by(movie_type=category).all()

    return jsonify(movies=[movie.to_json() for movie in movies]), 200


@movies_bp.route('/movie_info', methods=['POST'])
def movie_info():
    """
    fetches info about a specific movie.

    receives an integer and searches the
    database about the specific movie.

    POST DATA:
        movie_id (int): movie id

    Returns:
        json: dict that contains the movie info
    """

    movie_id = request.get_json().get("movie_id")
    movie = Movies.query.filter_by(id=movie_id).first()

    return jsonify(movie=movie.to_json()), 200


@movies_bp.route("/rating", methods=['POST'])
def movie_by_rating():
    """
    fetches movies filtered by rating.

    receives a float or integer and searches
    the database for movies with the specific rating.

    POST DATA:
        rating (float or int): movie rating

    Returns:
        json: list of movies with the specific rating
    """

    rating = request.get_json().get("rating")
    if not rating:
        return jsonify({"message": "Missing parameters"}), 400

    movies = Movies.query.filter_by(rating=rating).all()

    return jsonify(movies=[movie.to_json() for movie in movies]), 200
