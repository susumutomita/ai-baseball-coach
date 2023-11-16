import json

from flask import render_template, session


def configure_home_routes(app):
    @app.route("/home")
    def home():
        return render_template(
            "home.html",
            session=session.get("user"),
            pretty=json.dumps(session.get("user"), indent=4),
        )
