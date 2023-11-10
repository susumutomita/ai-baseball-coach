import json
import os
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from config import Config
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from models import BaseModel, GptModel, PlamoModel

# 定数
SEARCH_DIRECTORY = "./app/"
PROMPT_TEMPLATE_PATH = "./prompt_template.txt"
DEFAULT_MODEL_TYPE = "gpt2"

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
api = Api(app)
print(app.config)
oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=app.config["AUTH0_CLIENT_ID"],
    client_secret=app.config["AUTH0_CLIENT_SECRET"],
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{app.config["AUTH0_DOMAIN"]}/.well-known/openid-configuration',
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


model_type = app.config["MODEL_TYPE"]

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


@app.before_request
def require_login():
    allowed_routes = ["callback", "login", "logout"]
    if request.endpoint not in allowed_routes:
        if "user" not in session:
            return redirect("/login")
    # Swaggerのページにも認証を要求
    if request.endpoint == "api.specs" or request.path.startswith("/swagger-ui/"):
        if "user" not in session:
            return redirect("/login")


# Controllers API
@app.route("/")
def home():
    return render_template(
        "home.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


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
    # Redirect URLを構築する
    return redirect(
        "https://"
        + app.config["AUTH0_DOMAIN"]
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": app.config["AUTH0_CLIENT_ID"],
            },
            quote_via=quote_plus,
        )
    )


@api.route("/api/question")
class QuestionResource(Resource):
    def check_auth(self):
        if "user" not in session:
            return redirect("/login")
        return None

    @api.expect(question_model, validate=True)
    def post(self):
        auth_result = self.check_auth()
        if auth_result:
            return auth_result
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["PORT"])
