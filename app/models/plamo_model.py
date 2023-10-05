from transformers import AutoModelForCausalLM, AutoTokenizer

from .base_model import BaseModel


class PlamoModel(BaseModel):
    def __init__(self, model_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)

    def load_model(self, model_path: str):
        # この場合、必要ないかもしれません
        pass

    def generate_text(self, prompt: str, max_tokens: int, temperature: float) -> str:
        inputs = self.tokenizer.encode(prompt, return_tensors="pt")
        outputs = self.model.generate(
            inputs, max_length=max_tokens, num_return_sequences=1, temperature=temperature
        )
        response_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response_text
