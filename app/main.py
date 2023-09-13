import argparse

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# 引数処理
parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str)
optvar = parser.parse_args()

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf")

# ソース言語・ターゲット言語の指定
tokenizer.src_lang = "en_XX"
tokenizer.tgt_lang = "ja_XX"

# トークナイザに投入する文字列長の指定
tokenizer.model_maxlength = 2048

# Pipelineを使用して翻訳タスクを実行するオブジェクトを作成する
pipe = pipeline(
    "translation",
    model=model,
    tokenizer=tokenizer,
    src_lang="en_XX",
    tgt_lang="ja_XX",
    device="cpu",
    batch_size=16,
)

# 翻訳元ファイルを開いて、翻訳処理を開始する
with open(optvar.file) as f:
    for line in f:
        # 翻訳処理を実行する。最大長は1024とし、truncate処理は有効にする
        translations = pipe(line, max_length=1024, truncation=True)

        # 原文の表示
        print(line)

        # 翻訳結果の表示
        print(str(translations[0]["translation_text"]))

        # 空行を挿入
        print("\n")
