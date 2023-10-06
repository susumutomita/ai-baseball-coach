import transformers

from .base_model import BaseModel


class PlamoModel(BaseModel):
    def __init__(self, model_name: str):
        self.pipeline = transformers.pipeline(
            "text-generation", model=model_name, trust_remote_code=True
        )

    def load_model(self, model_path: str):
        pass

    def generate_text(self, prompt: str, max_tokens: int, temperature: float) -> str:
        response_text = self.pipeline(prompt, max_new_tokens=max_tokens)
        return response_text
