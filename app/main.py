import os
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, jsonify, redirect, request, session, url_for
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from models import BaseModel, GptModel, PlamoModel

# 定数
SEARCH_DIRECTORY = "./app/"
PROMPT_TEMPLATE_PATH = "./prompt_template.txt"
DEFAULT_MODEL_TYPE = "gpt2"

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")
CORS(app)
api = Api(app)

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)


def read_files(directory_path, file_extension):
    content = ""
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            if filename.endswith(file_extension):
                filepath = os.path.join(root, filename)
                with open(filepath, "r", encoding="utf-8") as file:
                    content += file.read() + "\n\n"
    return content


def error_response(message, status_code):
    return jsonify({"error": message}), status_code


model_type = os.environ.get("MODEL_TYPE", DEFAULT_MODEL_TYPE)

if model_type == "Plamo":
    model: BaseModel = PlamoModel(model_name="pfnet/plamo-13b")
elif model_type == "gpt2":
    model: BaseModel = GptModel(model_name="gpt2")

TEAM_RULES = read_files(SEARCH_DIRECTORY, ".ja_jp.md")
PROMPT_FOR_GENERATION_FORMAT = read_files(PROMPT_TEMPLATE_PATH, ".txt")

question_model = api.model(
    "Question",
    {"question": fields.String(required=True, description="The question you want to ask")},
)


@api.route("/api/question")
class QuestionResource(Resource):
    @api.expect(question_model, validate=True)
    def post(self):
        if not request.json:
            return error_response("Invalid input, JSON expected", 400)

        user_input = request.json.get("question")
        if not user_input:
            return error_response("Missing 'question' field in input JSON", 400)

        return self.generate_response(user_input)

    def generate_response(self, user_input):
        full_prompt = f"{PROMPT_FOR_GENERATION_FORMAT}\n{user_input}\n{TEAM_RULES}"
        response_text = model.generate_text(prompt=full_prompt, max_tokens=120, temperature=0.2)

        response_only = (
            response_text.split("Response:")[1].strip()
            if "Response:" in response_text
            else response_text
        )
        return jsonify({"response": response_only})


# Controllers API
@app.route("/")
def home():
    return redirect("/")


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(redirect_uri=url_for("callback", _external=True))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0")
