import os

import git
from transformers import pipeline


def read_all_markdown_files(directory_path):
    team_rules = ""
    for filename in os.listdir(directory_path):
        if filename.endswith(".ja_jp.md"):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                team_rules += file.read() + "\n\n"
    return team_rules


def read_markdown_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


repo_url = os.environ.get("REPO_URL", "https://github.com/xerosbaseball/terms")
local_directory = "/app/app/rules/"

# レポジトリをクローン（注：既にディレクトリが存在する場合はこの行をコメントアウト）
git.Repo.clone_from(repo_url, local_directory)

TEAM_RULES = read_all_markdown_files(local_directory)
prompt_template_path = "/app/app/prompt_template.txt"
PROMPT_FOR_GENERATION_FORMAT = read_markdown_file(prompt_template_path)

pipe = pipeline(task="text-generation")


def gen_text(prompts, **kwargs):
    full_prompts = [f"{PROMPT_FOR_GENERATION_FORMAT}\n{prompt}\n{TEAM_RULES}" for prompt in prompts]
    outputs = pipe(full_prompts, **kwargs)
    return [out[0]["generated_text"] for out in outputs]


results = gen_text(["What should a team member do if they are running late?"], max_length=100)
print(results[0])
