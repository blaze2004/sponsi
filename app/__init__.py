"""Influencer Engagement and Sponsorship Coordination Platform"""

import os
from uuid import uuid4
from flask import Flask
from dotenv import load_dotenv
from app.utils import db, login_manager

load_dotenv()


def create_app():
    """Construct the core application."""
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", uuid4().hex)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

    db.init_app(app)
    login_manager.init_app(app)

    from app.views import main, auth  # pylint: disable=import-outside-toplevel

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix="/auth")

    return app
