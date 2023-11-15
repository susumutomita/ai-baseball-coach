# app/api/endpoints/question.py

from flask import jsonify, redirect, request, session
from flask_restx import Resource
from utils.helpers import error_response


def create_question_resource(api, model, question_model, PROMPT_FOR_GENERATION_FORMAT, TEAM_RULES):
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

    return QuestionResource
