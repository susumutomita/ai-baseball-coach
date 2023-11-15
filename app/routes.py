# app/routes.py

import json
from urllib.parse import quote_plus, urlencode

from flask import redirect, render_template, request, session, url_for

from app.api.endpoints.question import create_question_resource


def configure_routes(
    app, api, oauth, model, question_model, PROMPT_FOR_GENERATION_FORMAT, TEAM_RULES
):
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

    # Question APIの設定
    QuestionResource = create_question_resource(
        api, model, question_model, PROMPT_FOR_GENERATION_FORMAT, TEAM_RULES
    )
    api.add_resource(QuestionResource, "/api/question")
