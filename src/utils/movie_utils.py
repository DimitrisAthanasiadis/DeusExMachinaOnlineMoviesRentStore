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