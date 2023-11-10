from authlib.integrations.flask_client import OAuth


def setup_auth(app):
    oauth = OAuth(app)

    oauth.register(
        "auth0",
        client_id=app.config["AUTH0_CLIENT_ID"],
        client_secret=app.config["AUTH0_CLIENT_SECRET"],
        client_kwargs={"scope": "openid profile email"},
        server_metadata_url=f'https://{app.config["AUTH0_DOMAIN"]}/'
        ".well-known/openid-configuration",
    )

    return oauth
