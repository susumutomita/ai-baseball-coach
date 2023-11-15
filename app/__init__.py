"""
This is the initialization module for the AI Baseball Coach app.
It sets up the Flask app and its configurations.
"""
from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from app.auth.auth import setup_auth
from app.config import Config
from app.routes import configure_routes


def create_app():
    """
    Create and configure the Flask app.
    """

    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    api = Api(app, doc="/api/docs")
    oauth = setup_auth(app)

    configure_routes(app, api, oauth)

    return app
