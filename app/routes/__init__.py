from .api_routes import configure_api_routes
from .auth_routes import configure_auth_routes
from .home_routes import configure_home_routes


def configure_routes(
    app, api, oauth, model, question_model, prompt_for_generation_format, team_rules
):
    configure_auth_routes(app, oauth)
    configure_home_routes(app)
    configure_api_routes(app, api, model, question_model, prompt_for_generation_format, team_rules)
