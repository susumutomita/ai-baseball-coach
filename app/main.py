import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from models import BaseModel, GptModel, PlamoModel

app = Flask(__name__)
CORS(app)
api = Api(app)


def read_all_markdown_files(directory_path):
    team_rules = ""
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            if filename.endswith(".ja_jp.md"):
                filepath = os.path.join(root, filename)
                with open(filepath, "r", encoding="utf-8") as file:
                    team_rules += file.read() + "\n\n"
    return team_rules


def read_markdown_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


model_type = os.environ.get("MODEL_TYPE", "gpt2")

if model_type == "Plamo":
    model: BaseModel = PlamoModel(model_name="pfnet/plamo-13b")
elif model_type == "gpt2":
    model: BaseModel = GptModel(model_name="gpt2")

# マークダウンファイルとプロンプトテンプレートの読み込み
search_directory = "./app/"
TEAM_RULES = read_all_markdown_files(search_directory)
prompt_template_path = "./prompt_template.txt"
PROMPT_FOR_GENERATION_FORMAT = read_markdown_file(prompt_template_path)


question_model = api.model(
    "Question",
    {"question": fields.String(required=True, description="The question you want to ask")},
)


@api.route("/api/question")
class QuestionResource(Resource):
    @api.expect(question_model, validate=True)
    @api.doc(
        params={"question": "The question you want to ask."},
    )
    def post(self):
        json_data = request.json
        if json_data is None:
            return jsonify({"error": "Invalid input, JSON expected"}), 400

        user_input = json_data.get("question")
        if not user_input:
            return jsonify({"error": "Missing 'question' field in input JSON"}), 400

        full_prompt = f"{PROMPT_FOR_GENERATION_FORMAT}\n{user_input}\n{TEAM_RULES}"
        response_text = model.generate_text(prompt=full_prompt, max_tokens=120, temperature=0.2)

        response_only = (
            response_text.split("Response:")[1].strip()
            if "Response:" in response_text
            else response_text
        )

        return jsonify({"response": response_only})


if __name__ == "__main__":
    app.run(port=5001, host="0.0.0.0")
