from atexit import register
from src import create_app, register_blueprints
from src.blueprints.movies import movies_bp
from src.blueprints.transaction import transaction_bp
from src.models import *


app = create_app()
register_blueprints(app, movies_bp, transaction_bp)

if __name__ == "__main__":
    app.run(debug=True)
