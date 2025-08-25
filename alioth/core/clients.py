from typing import Protocol
from dataclasses import dataclass
from typing import Any
import openai
import ollama

class ModelClient(Protocol):
    def generate(self, prompt: str): ...

def answer_prompt(adapter: ModelClient, prompt: str):
    return adapter.generate(prompt)

@dataclass
class OpenAIClient:
    model: str
    client: openai.OpenAI
    def generate(self, prompt: str):
        return f"user: {prompt}\n{self.model}: tested!"

@dataclass
class OllamaClientAdapter:
    model: str
    client: ollama.Client
    def generate(self, prompt: str):
        return f"user: {prompt}\n{self.model}: tested!"
