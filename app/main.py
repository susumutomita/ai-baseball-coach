import os

from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from transformers import pipeline


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


search_directory = "./app/"

TEAM_RULES = read_all_markdown_files(search_directory)
prompt_template_path = "./prompt_template.txt"
PROMPT_FOR_GENERATION_FORMAT = read_markdown_file(prompt_template_path)

pipe = pipeline(task="text-generation", model="EleutherAI/gpt-neo-2.7B")


def gen_text(prompts, **kwargs):
    full_prompts = [f"{PROMPT_FOR_GENERATION_FORMAT}\n{prompt}\n{TEAM_RULES}" for prompt in prompts]
    outputs = pipe(full_prompts, **kwargs)
    return [out[0]["generated_text"] for out in outputs]


results = gen_text(["What should a team member do if they are running late?"], max_length=100)
print(results[0])

app = Flask(__name__)

line_bot_api = LineBotApi("YOUR_CHANNEL_ACCESS_TOKEN")
handler = WebhookHandler("YOUR_CHANNEL_SECRET")


def gen_text(prompts, **kwargs):
    full_prompts = [f"{PROMPT_FOR_GENERATION_FORMAT}\n{prompt}\n{TEAM_RULES}" for prompt in prompts]
    outputs = pipe(full_prompts, **kwargs)
    return [out[0]["generated_text"] for out in outputs]


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]

    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_input = event.message.text  # ユーザーからの入力を取得
    prompts = [f"What should a team member do if {user_input}?"]
    # ユーザーからの質問に応じた回答を生成
    responses = gen_text(prompts, max_length=100)
    response = responses[0]  # 生成されたテキストを取得

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response))


if __name__ == "__main__":
    app.run()
