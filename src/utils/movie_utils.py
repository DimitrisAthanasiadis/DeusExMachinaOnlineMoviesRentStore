from flask import jsonify
from src import db

class MoviesTransactions:
    def __init__(self):
        pass

    def rent_price(self, **kwargs):
        days_to_rent = kwargs.get("days_to_rent")

        if days_to_rent <= 3:
            price = days_to_rent
        else:
            price = 3
            for i in range(4, days_to_rent+1):
                price += 0.5

        return price

    def rent_transaction(self, **kwargs):
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
            return jsonify({"message": "Error saving transaction"}), 500

        return jsonify({
            "message": "Rent transaction successful",
            "movie": movie.to_json(),
            "days_to_rent": days_to_rent,
            "rent_price": self.rent_price(days_to_rent=days_to_rent),
            "rental_date": rental_date.strftime("%Y-%m-%d %H:%M:%S")
        }), 200