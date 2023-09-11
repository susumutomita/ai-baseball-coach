import torch
from transformers import GPT2Tokenizer, pipeline


def main():
    # トークナイザとモデルの初期化
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    # model = GPT2LMHeadModel.from_pretrained("gpt2")
    # model = AutoModel.from_pretrained("TheBloke/Llama-2-7B-Chat-GGML")
    model = pipeline("text-generation", model="TheBloke/Llama-2-7B-Chat-GGML")

    # 入力テキスト
    input_text = "Hello, how are you?"

    # テキストをトークンに変換
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    # モデルで推論
    with torch.no_grad():
        output = model.generate(input_ids, max_length=50)

    # 生成されたテキストをデコード
    output_text = tokenizer.decode(output[0], skip_special_tokens=True)

    print(output_text)


if __name__ == "__main__":
    main()
