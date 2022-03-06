from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate(compare_type=True)


def create_app():
    app = Flask(__name__)
    db.init_app(app)
    migrate.init_app(app, db)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie_store.db'

    return app

def register_blueprints(app, *args):
    for arg in args:
        app.register_blueprint(arg)
