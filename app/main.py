from transformers import pipeline


def read_markdown_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


team_rules_path = "/app/app/team_rules.md"
prompt_template_path = "/app/app/prompt_template.txt"

TEAM_RULES = read_markdown_file(team_rules_path)
PROMPT_FOR_GENERATION_FORMAT = read_markdown_file(prompt_template_path)

pipe = pipeline(task="text-generation")


# テキスト生成パラメータの設定
def gen_text(prompts, **kwargs):
    full_prompts = [f"{PROMPT_FOR_GENERATION_FORMAT}\n{prompt}\n{TEAM_RULES}" for prompt in prompts]
    outputs = pipe(full_prompts, **kwargs)
    return [out[0]["generated_text"] for out in outputs]


# テキスト生成のテスト
results = gen_text(["What should a team member do if they are running late?"], max_length=100)
print(results[0])
