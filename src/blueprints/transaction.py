from flask import Blueprint, jsonify, request
from src.models import Movies, User
from src.utils.movie_utils import MoviesTransactions


transaction_bp = Blueprint('transaction', __name__, url_prefix='/transaction')


@transaction_bp.route('/rent_info', methods=['POST'])
def rent_info():
    """
    searches for a specific movie and returns
    the rent info according to the given days.

    receives movie id and days for rental
    and calculates the cost.

    POST DATA:
        movie_id (int): movie id
        days_to_rent (int): number of days to rent

    Returns:
        json: dict that contains info about
            the rental of the specific movie
    """

    movie_id = request.get_json().get("movie_id")
    days_to_rent = request.get_json().get("days_to_rent")

    if not movie_id or not days_to_rent:
        return jsonify({"message": "Missing parameters"}), 400

    movie = Movies.query.filter_by(id=movie_id).first()
    if not movie:
        return jsonify({"message": "Movie not found"}), 404

    movie_transactions = MoviesTransactions()
    rent_price = movie_transactions.rent_price(days_to_rent=days_to_rent)

    return jsonify({
        "movie": movie.to_json(),
        "days_to_rent": days_to_rent,
        "rent_price": rent_price
    })


@transaction_bp.route('/rent', methods=['POST'])
def rent():
    """
    user rents the given movie for the given days.

    POST DATA:
        movie_id (int): movie id
        days_to_rent (int): number of days to rent
        user_id (int): the user that will rent the movie

    Returns:
        json: dict that contains the rental info for the
            given movie.
    """

    movie_id = request.get_json().get("movie_id")
    days_to_rent = request.get_json().get("days_to_rent")
    user_id = request.get_json().get("user_id")

    if not movie_id or not days_to_rent or not user_id:
        return jsonify({"message": "Missing parameters"}), 400

    movie = Movies.query.filter_by(id=movie_id).first()
    if not movie:
        return jsonify({"message": "Movie not found"}), 404

    movie_transactions = MoviesTransactions()
    transaction = movie_transactions.rent_transaction(
        movie=movie,
        days_to_rent=days_to_rent,
        user_id=user_id,
    )

    return transaction
