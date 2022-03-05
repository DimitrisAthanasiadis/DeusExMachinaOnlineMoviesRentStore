from atexit import register
from src import create_app, register_blueprints
from src.models import *
from src.blueprints.movies import movies_bp


app = create_app()
register_blueprints(app, movies_bp)

if __name__ == '__main__':
    app.run(debug=True)