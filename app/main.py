from transformers import pipeline

# モデルとトークナイザの設定
pipe = pipeline(task="text-generation")

# チームのルール（マークダウン形式）
with open("team_rules.md", "r", encoding="utf-8") as f:
    TEAM_RULES = f.read()

# プロンプト生成のためのテンプレート
INSTRUCTION_KEY = "### Instruction:"
RESPONSE_KEY = "### Response:"
INTRO_BLURB = "Below is an instruction that describes a task. "
"Write a response that appropriately completes the request."


# テキスト生成パラメータの設定
def gen_text(prompts, **kwargs):
    full_prompts = [
        f"{INTRO_BLURB}\n{INSTRUCTION_KEY}\n{prompt}\n{RESPONSE_KEY}\n{TEAM_RULES}"
        for prompt in prompts
    ]
    outputs = pipe(full_prompts, **kwargs)
    return [out[0]["generated_text"] for out in outputs]


results = gen_text(["ユニフォームのルールについて教えて"], max_length=100)
print(results[0])
