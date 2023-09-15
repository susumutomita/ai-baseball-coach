import torch
import transformers
from transformers import AutoTokenizer

# モデルとトークナイザの設定
model = "meta-llama/Llama-2-7b-chat-hf"
revision = "0ede8dd71e923db6258295621d817ca8714516d4"
tokenizer = AutoTokenizer.from_pretrained(model, padding_side="left")

# パイプラインの設定
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",
    revision=revision,
    return_full_text=False,
)

# トークナイザのパッド設定
pipeline.tokenizer.pad_token_id = tokenizer.eos_token_id

# チームのルール（マークダウン形式）
with open("team_rules.md", "r", encoding="utf-8") as f:
    TEAM_RULES = f.read()

# プロンプト生成のためのテンプレート
INSTRUCTION_KEY = "### Instruction:"
RESPONSE_KEY = "### Response:"
INTRO_BLURB = "Below is an instruction that describes a task."
"Write a response that appropriately completes the request."


# テキスト生成パラメータの設定
def gen_text(prompts, **kwargs):
    full_prompts = [
        f"{INTRO_BLURB}\n{INSTRUCTION_KEY}\n{prompt}\n{RESPONSE_KEY}\n{TEAM_RULES}"
        for prompt in prompts
    ]
    outputs = pipeline(full_prompts, **kwargs)
    return [out[0]["generated_text"] for out in outputs]


# テキスト生成のテスト
results = gen_text(["What should a team member do if they are running late?"])
print(results[0])
