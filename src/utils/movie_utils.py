from flask import jsonify
from src import db

class MoviesTransactions:
    def __init__(self):
        pass

    def rent_price(self, **kwargs):
        """
        calculates the cost of the rental
        according to the given days.

        kwargs:
            days_to_rent (int): number of days to rent

        Returns:
            int: the rental cost
        """

        days_to_rent = kwargs.get("days_to_rent")

        if days_to_rent <= 3:
            price = days_to_rent
        else:
            price = 3
            for i in range(4, days_to_rent+1):
                price += 0.5

        return price

    def rent_transaction(self, **kwargs):
        """
        performs the rental transaction with
        the database.

        kwargs:
            days_to_rent (int): number of days to rent
            movie (int): movie id

        Returns:
            json: dict that contains the rental info
        """

        from src.models import UserMovieRentals
        from datetime import datetime

        days_to_rent = kwargs.get("days_to_rent")
        movie = kwargs.get("movie")

        try:
            rental_date = datetime.now()
            rent_transaction = UserMovieRentals(
                user_id=kwargs.get("user_id"),
                movie_id=movie.id,
                rental_date=rental_date,
                days_to_rent=days_to_rent,
            )
            db.session.add(rent_transaction)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({
                "message": "Error saving transaction",
                "error": str(e)
            }), 500

        return jsonify({
            "message": "Rent transaction successful",
            "movie": movie.to_json(),
            "days_to_rent": days_to_rent,
            "rent_price": self.rent_price(days_to_rent=days_to_rent),
            "rental_date": rental_date.strftime("%Y-%m-%d %H:%M:%S")
        }), 200

    def get_extra_cost_penalty(self, **kwargs):
        """
        calculates the possible extra cost penalty
        if the user hasn't returned the movie in time.

        kwargs:
            movie (Movie object): movie object

        Returns:
            int: depicts the extra cost penalty in euros.
                the penalty is 2 euros per extra day.
        """

        from datetime import datetime, timedelta

        movie = kwargs.get("movie")
        extra_cost_penalty = 0

        if movie.get("returned") is True:
            return extra_cost_penalty

        rental_date = datetime.strptime(movie.get("rental_date"), "%Y-%m-%d %H:%M:%S").date()
        now = datetime.now().date()
        supposed_return_date = rental_date + timedelta(days=movie.get("days_to_rent"))

        if now < supposed_return_date:
            return extra_cost_penalty

        try:
            day_difference = (now - supposed_return_date).days
        except Exception as e:
            print(f"EXCEPTION IN GET EXTRA COST PENALTY: {e}")
            day_difference = 0

        extra_cost_penalty = day_difference * 2

        return extra_cost_penalty

    def get_total_cost(self, **kwargs):
        movie = kwargs.get("movie")
        rent_price = self.rent_price(days_to_rent=movie.get("days_to_rent"))
        extra_cost_penalty = self.get_extra_cost_penalty(movie=movie)

        total_cost = rent_price + extra_cost_penalty

        return total_cost

    def user_can_rent_movie(self, **kwargs):
        """
        returns the ability of the user to rent a movie.

        it depends on the existence of the movie in the
        user_movie_rentals table. if the movie is absent from
        the table or the user has returned the movie, the user
        can rent the movie

        kwargs:
            movie_id (int): movie id
            user_id (int): user id

        Returns:
            bool: the user can rent the movie or not
        """

        from src.models import UserMovieRentals

        movie_id = kwargs.get("movie_id")
        user_id = kwargs.get("user_id")

        user_rented_movie = UserMovieRentals.query.filter_by(user_id=user_id, movie_id=movie_id).order_by(UserMovieRentals.rental_date.desc()).first()
        if not user_rented_movie or user_rented_movie.returned is True:
            return True
        else:
            return False

    def pay(self, **kwargs):
        """
        performs the payment of the rental.

        accepts movie id, user id and amount to pay.
        checks if the user has rented the movie and
        if the amount of money is enough to pay the
        rented movie. the movie is then marked as
        returned and the returned date is the current
        datetime.

        Returns:
            json: the final jsonified answer of the payment
        """

        from src.models import UserMovieRentals
        from datetime import datetime

        transaction_id = kwargs.get("transaction_id")
        user_id = kwargs.get("user_id")
        euros = kwargs.get("euros")

        user_rented_movie = UserMovieRentals.query.filter_by(user_id=user_id, id=transaction_id).first()

        if not user_rented_movie or user_rented_movie.returned is True:
            return jsonify({"message": "You haven't rented this movie or you have already paid for it in the last transaction."}), 400

        total_cost = self.get_total_cost(movie=user_rented_movie.to_json())
        if euros < total_cost:
            return jsonify({
                "message": f"You don't have enough money to pay for this movie. Total cost is {total_cost} euros",
            }), 400
        change = euros - total_cost

        try:
            user_rented_movie.returned = True
            user_rented_movie.return_date = datetime.now()
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({
                "message": "Error paying the movie",
                "error": e
            }), 500


        return jsonify({
            "message": "Movie paid successfully",
            "movie_id": transaction_id,
            "user_id": user_id,
            "return_date": user_rented_movie.return_date.strftime("%Y-%m-%d %H:%M:%S"),
            "returned": user_rented_movie.returned,
            "change": change
        }), 200
