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
        auth,
        # admin,
        # sponsor,
        # influencer,
    )  # pylint: disable=import-outside-toplevel

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix="/auth")
    # app.register_blueprint(admin, url_prefix="/admin")
    # app.register_blueprint(sponsor, url_prefix="/sponsor")
    # app.register_blueprint(influencer, url_prefix="/influencer")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=os.getenv("FLASK_ENV", "development").lower() == "development")
