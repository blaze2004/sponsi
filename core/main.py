"""App Entrypoint"""

import os
from flask import Flask
from dotenv import load_dotenv

from api.models.user import create_admin
from config import get_config
from middleware import middleware
from utils import db, login_manager

load_dotenv()


def create_app():
    """Construct the core application."""
    app = Flask(__name__)

    app.config.from_object(get_config())

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()
        create_admin()

    @app.before_request
    def before_request():
        return middleware()

    from api.routes import (
        main,
        api,
    )  # pylint: disable=import-outside-toplevel

    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix="/api")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=os.getenv("FLASK_ENV", "development").lower() == "development")
