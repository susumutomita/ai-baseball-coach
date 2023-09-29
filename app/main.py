import os

from llama_cpp import Llama


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

model_path = "../model/llama-2-7b-chat/ggml-model-f16_q4_0.bin"
model = Llama(
    model_path=model_path,
    n_ctx=2048,  # context window size
    n_gpu_layers=1,  # enable GPU
    use_mlock=True,
)  # enable memory lock so not swap

while True:
    user_input = input("質問を入力してください（終了するには'quit'と入力）: ")
    if user_input.lower() == "quit":
        break

    full_prompt = f"{PROMPT_FOR_GENERATION_FORMAT}\n{user_input}\n{TEAM_RULES}"
    output = model(prompt=full_prompt, max_tokens=120, temperature=0.2)
    response_text = output.get("choices", [{}])[0].get("text", "No response generated.")

    print("応答:", response_text)
