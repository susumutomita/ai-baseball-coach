from urllib.parse import quote_plus, urlencode

from flask import redirect, request, session, url_for


def configure_auth_routes(app, oauth):
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
