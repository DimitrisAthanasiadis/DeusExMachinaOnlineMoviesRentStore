from flask import Blueprint, jsonify, request
from src.models import Movies, UserMovieRentals
from src.utils.movie_utils import MoviesTransactions
from src.utils.decorators import token_required


transaction_bp = Blueprint("transaction", __name__, url_prefix="/transaction")


@transaction_bp.route("/rent_info", methods=["POST"])
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

    return jsonify(
        {
            "movie": movie.to_json(),
            "days_to_rent": days_to_rent,
            "rent_price": rent_price,
        }
    )


@transaction_bp.route("/rent", methods=["POST"])
@token_required
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

    if (
        movie_transactions.user_can_rent_movie(user_id=user_id, movie_id=movie_id)
        is False
    ):
        return jsonify({"message": "You can't rent this movie."}), 400

    transaction = movie_transactions.rent_transaction(
        movie=movie,
        days_to_rent=days_to_rent,
        user_id=user_id,
    )

    return transaction


@transaction_bp.route("/get_rented_movies", methods=["POST"])
@token_required
def get_rented_movies():
    """
    fetches the rented movies for the given user.

    POST DATA:
        user_id (int): the user id

    Returns:
        json: the jsonified list of rented movies
    """

    user_id = request.get_json().get("user_id")

    if not user_id:
        return jsonify({"message": "Missing parameters"}), 400

    rented_movies = [
        movie.to_json()
        for movie in UserMovieRentals.query.filter_by(user_id=user_id)
        .order_by(UserMovieRentals.rental_date.desc())
        .all()
    ]

    if not rented_movies:
        return jsonify({"message": "No rented movies"}), 404

    return jsonify(rented_movies), 200


@transaction_bp.route("/get_not_returned_movies", methods=["POST"])
@token_required
def get_not_returned_movies():
    """
    fetches the not returned movies for the given user.

    POST DATA:
        user_id (int): the user id

    Returns:
        json: the jsonified list of not returned movies
    """

    user_id = request.get_json().get("user_id")

    if not user_id:
        return jsonify({"message": "Missing parameters"}), 400

    not_returned_movies = [
        movie.to_json()
        for movie in UserMovieRentals.query.filter_by(
            user_id=user_id, returned=False
        ).all()
    ]
    movies_transactions = MoviesTransactions()

    for movie in not_returned_movies:
        movie["extra_cost_penalty"] = movies_transactions.get_extra_cost_penalty(
            movie=movie
        )
        movie["total_cost"] = movies_transactions.get_total_cost(movie=movie)

    if not not_returned_movies:
        return jsonify({"message": "All movies are returned and paid"}), 404

    return jsonify(not_returned_movies), 200


@transaction_bp.route("/pay", methods=["POST"])
@token_required
def pay():
    """
    performs the payment for the given movie.

    POST DATA:
        transaction_id (int): transaction id
        user_id (int): user id
        euros (float or int): the amount of euros to pay

    Returns:
        json: the jsonified answer about the payment
    """

    user_id = request.get_json().get("user_id")
    transaction_id = request.get_json().get("transaction_id")
    euros = request.get_json().get("euros")

    if not user_id or not transaction_id or not euros:
        return jsonify({"message": "Missing parameters"}), 400

    movies_transactions = MoviesTransactions()
    paid_movie = movies_transactions.pay(
        user_id=user_id, transaction_id=transaction_id, euros=euros
    )

    return paid_movie
