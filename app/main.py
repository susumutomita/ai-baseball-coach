import os

import flask_oauthlib.client
from flask import Flask, jsonify, redirect, request, session, url_for
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from models import BaseModel, GptModel, PlamoModel

# 定数
SEARCH_DIRECTORY = "./app/"
PROMPT_TEMPLATE_PATH = "./prompt_template.txt"
DEFAULT_MODEL_TYPE = "gpt2"

app = Flask(__name__)
app.secret_key = "this is secret"  # これを追加
CORS(app)
api = Api(app)

# OAuthの設定
oauth = flask_oauthlib.client.OAuth(app)
# 環境変数から読み込む
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "YourDefaultAUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET", "YourDefaultAUTH0_CLIENT_SECRET")
AUTH0_BASE_URL = os.environ.get("AUTH0_BASE_URL", "https://YourDefaultAuth0Domain/")
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE", "YourDefaultAuth0Audience")

auth0 = oauth.remote_app(
    "auth0",
    consumer_key=AUTH0_CLIENT_ID,
    consumer_secret=AUTH0_CLIENT_SECRET,
    request_token_params={"scope": "openid profile", "audience": AUTH0_AUDIENCE},
    base_url=AUTH0_BASE_URL,
    access_token_method="POST",
    access_token_url="/oauth/token",
    authorize_url="/authorize",
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


@app.route("/login")
def login():
    return auth0.authorize(callback=url_for("auth_callback", _external=True))


@app.route("/callback")
def auth_callback():
    resp = auth0.authorized_response()
    if resp is None:
        return "Access denied", 403
    session["profile"] = resp  # 例として、プロフィール情報をセッションに格納
    return redirect("/mypage")


@app.route("/mypage")
def mypage():
    if not session.get("profile"):
        return redirect("/login")
    return "This is mypage"


@app.route("/logout")
def logout():
    session.pop("profile", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0")
