from src import db


class UserTypes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(20), unique=True)

    def to_json(self):
        return {
            'id': self.id,
            'user_type': self.user_type
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(128))
    surname = db.Column(db.String(128))
    user_type = db.Column(db.Integer, db.ForeignKey('user_types.id'))

    @property
    def is_admin(self):
        return self.user_type == 'Admin'

    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'surname': self.surname,
            'user_type': self.user_type
        }


class MovieTypes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_type = db.Column(db.String(20), unique=True)

    def to_json(self):
        return {
            'id': self.id,
            'movie_type': self.movie_type
        }


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.String(128))
    movie_type = db.Column(db.Integer, db.ForeignKey('movie_types.id'))
    rating = db.Column(db.Float)

    __table_args__ = (db.CheckConstraint('rating >= 1.0 AND rating <= 10.0'),)

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'movie_type': self.movie_type,
            'rating': self.rating
        }


class UserMovie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    rating = db.Column(db.Float)
    comments = db.Column(db.String(1000))

    __table_args__ = (db.CheckConstraint('rating >= 1.0 AND rating <= 10.0'),)

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'rating': self.rating,
            'comments': self.comments
        }


class UserMovieRentals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    rental_date = db.Column(db.DateTime, nullable=False)
    days_to_rent = db.Column(db.Integer)
    returned = db.Column(db.Boolean, default=False)
    return_date = db.Column(db.DateTime, default=None)

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'days_to_rent': self.days_to_rent,
            'returned': self.returned
        }
