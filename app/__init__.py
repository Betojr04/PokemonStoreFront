from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import (
    db,
)  # This should import the SQLAlchemy instance from your models file


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="../static")

    # Inline configuration (adjust these values as needed)
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///cards.db"  # or your preferred database URI
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "your_secret_key_here"

    # Initialize SQLAlchemy with this app
    db.init_app(app)

    from .routes import main

    app.register_blueprint(main)

    return app
