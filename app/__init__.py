"""Module docstring: This module initializes the Flask application."""

# サードパーティ
from flask import Flask
from flask_cors import CORS
from flask_restx import Api, fields

# ローカルモジュール
from .auth.auth import setup_auth
from .config import Config
from .models import BaseModel, GptModel, PlamoModel
from .routes import configure_routes
from .utils.helpers import read_files


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    api = Api(app, doc="/api/docs", specification="static/ai_baseball_coach_api.yaml")
    oauth = setup_auth(app)

    model_type = app.config["MODEL_TYPE"]
    if model_type == "Plamo":
        model: BaseModel = PlamoModel(model_name="pfnet/plamo-13b")
    elif model_type == "gpt2":
        model: BaseModel = GptModel(model_name="gpt2")

    team_rules = read_files("./app/", ".ja_jp.md")
    prompt_for_generation_format = read_files("./prompt_template.txt", ".txt")

    question_model = api.model(
        "Question",
        {"question": fields.String(required=True, description="The question you want to ask")},
    )

    configure_routes(
        app, api, oauth, model, question_model, prompt_for_generation_format, team_rules
    )

    return app
