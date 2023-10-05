from abc import ABC, abstractmethod


class BaseModel(ABC):
    @abstractmethod
    def load_model(self, model_path: str):
        pass

    @abstractmethod
    def generate_text(self, prompt: str, max_tokens: int, temperature: float) -> str:
        pass
