from llama_cpp import Llama

from .base_model import BaseModel


class LlamaModel(BaseModel):
    def __init__(self, model_path: str, n_ctx=2048, n_gpu_layers=1, use_mlock=True):
        self.model = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_gpu_layers=n_gpu_layers,
            use_mlock=use_mlock,
        )

    def load_model(self, model_path: str):
        # Llama model のロード処理（必要であれば）
        pass

    def generate_text(self, prompt: str, max_tokens: int, temperature: float) -> str:
        output = self.model(prompt=prompt, max_tokens=max_tokens, temperature=temperature)
        response_text = output.get("choices", [{}])[0].get("text", "No response generated.")
        return response_text
