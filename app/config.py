# config.py

import os


class Config(object):
    SECRET_KEY = os.environ.get("APP_SECRET_KEY")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    API_AUDIENCE = os.getenv("API_AUDIENCE")
    DEFAULT_MODEL_TYPE = "gpt2"
    MODEL_TYPE = os.environ.get("MODEL_TYPE", DEFAULT_MODEL_TYPE)
    PORT = os.environ.get("PORT", 8080)
