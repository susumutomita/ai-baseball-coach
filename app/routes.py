import json
from urllib.parse import quote_plus, urlencode

from flask import jsonify, redirect, render_template, request, session, url_for
from flask_restx import Resource, fields
from models import BaseModel, GptModel, PlamoModel
from utils.helpers import error_response, read_files


def configure_routes(app, api, oauth):
    SEARCH_DIRECTORY = "./app/"
    PROMPT_TEMPLATE_PATH = "./prompt_template.txt"
    TEAM_RULES = read_files(SEARCH_DIRECTORY, ".ja_jp.md")
    PROMPT_FOR_GENERATION_FORMAT = read_files(PROMPT_TEMPLATE_PATH, ".txt")
    model_type = app.config["MODEL_TYPE"]

    if model_type == "Plamo":
        model: BaseModel = PlamoModel(model_name="pfnet/plamo-13b")
    elif model_type == "gpt2":
        model: BaseModel = GptModel(model_name="gpt2")

    question_model = api.model(
        "Question",
        {"question": fields.String(required=True, description="The question you want to ask")},
    )

    @app.route("/home")
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
        return redirect(session.pop("redirect_after_login", "/home"))

    @app.route("/login")
    def login():
        return oauth.auth0.authorize_redirect(redirect_uri=url_for("callback", _external=True))

    @app.route("/logout")
    def logout():
        session.clear()
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

            response_text = model.generate_text(
                prompt=f"{PROMPT_FOR_GENERATION_FORMAT}\n{user_input}\n{TEAM_RULES}",
                max_tokens=120,
                temperature=0.2,
            )

            response_only = (
                response_text.split("Response:")[1].strip()
                if "Response:" in response_text
                else response_text
            )
            return jsonify({"response": response_only})

    @app.before_request
    def require_login():
        allowed_routes = ["callback", "login", "logout", "home"]
        if request.endpoint not in allowed_routes:
            if "user" not in session:
                session["redirect_after_login"] = request.url
                return redirect("/login")
        if request.endpoint == "api.specs" or request.path.startswith("/swagger-ui/"):
            if "user" not in session:
                return redirect("/login")
