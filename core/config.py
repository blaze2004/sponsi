"""
Flask Environment Configuration
"""

import os
from uuid import uuid4


class Config:
    """Base config"""

    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", uuid4().hex)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Dev config."""

    DEBUG = True
    ENV = "development"


class ProductionConfig(Config):
    """Prod config."""

    DEBUG = False
    ENV = "production"


CONFIGS = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}


def get_config():
    """Get flask environment config."""
    env = os.getenv("FLASK_ENV", "development")
    return CONFIGS.get(env, DevelopmentConfig)
