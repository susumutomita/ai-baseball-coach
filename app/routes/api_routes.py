from app.api.endpoints.question import create_question_resource


def configure_api_routes(app, api, model, question_model, PROMPT_FOR_GENERATION_FORMAT, TEAM_RULES):
    QuestionResource = create_question_resource(
        api, model, question_model, PROMPT_FOR_GENERATION_FORMAT, TEAM_RULES
    )
    api.add_resource(QuestionResource, "/api/question")
