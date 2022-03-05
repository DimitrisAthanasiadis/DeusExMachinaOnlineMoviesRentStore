from flask import Blueprint, jsonify, request
from src.models import Movies


movies_bp = Blueprint('movies', __name__, url_prefix='/movies')


@movies_bp.route('/')
def movies_home():
    movies = Movies.query.all()

    return jsonify(movies=[movie.to_json() for movie in movies])


@movies_bp.route('/category', methods=['POST'])
def movie_by_category():
    category = request.get_json().get("category")
    movies = Movies.query.filter_by(movie_type=category).all()

    return jsonify(movies=[movie.to_json() for movie in movies])


@movies_bp.route('/movie_info', methods=['POST'])
def movie_info():
    movie_id = request.get_json().get("movie_id")
    movie = Movies.query.filter_by(id=movie_id).first()

    return jsonify(movie=movie.to_json())
