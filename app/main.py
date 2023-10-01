import os

from flask import Flask, jsonify, request
from llama_cpp import Llama

app = Flask(__name__)


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


# 以下の設定もそのまま
search_directory = "./app/"
TEAM_RULES = read_all_markdown_files(search_directory)
prompt_template_path = "./prompt_template.txt"
PROMPT_FOR_GENERATION_FORMAT = read_markdown_file(prompt_template_path)

# モデルのロード
model_path = "../model/llama-2-7b-chat/ggml-model-f16_q4_0.bin"
model = Llama(
    model_path=model_path,
    n_ctx=2048,
    n_gpu_layers=1,
    use_mlock=True,
)


@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("question", "")

    full_prompt = f"{PROMPT_FOR_GENERATION_FORMAT}\n{user_input}\n{TEAM_RULES}"
    output = model(prompt=full_prompt, max_tokens=120, temperature=0.2)
    response_text = output.get("choices", [{}])[0].get("text", "No response generated.")

    # 'Response:' 以降のテキストを取り出す
    response_only = (
        response_text.split("Response:")[1].strip()
        if "Response:" in response_text
        else response_text
    )

    return jsonify({"response": response_only})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
