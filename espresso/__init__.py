from flask import Flask
from espresso.extensions import db

from .api import blueprint
from .config import config_by_name

import secrets


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    secret = secrets.token_urlsafe(32)
    app.secret_key = secret

    # initialize plugins
    db.init_app(app)

    with app.app_context():
        # Register Blueprints
        app.register_blueprint(blueprint)

    return app
