from ..client.modelclient import *
from ..core.connection import *
from ..core.environment import *


from ollama import Client

class OllamaModelClient(ModelClient):
    """Ollama client provider."""

    def _check_connection(self) -> bool:
        return check_url_connection("http://localhost:11434/api/tags")

    def _create_client(self) -> Any:
        return Client(host = 'http://localhost:11434', headers = {'Content-Type': 'application/json'})

    def _list_models(self) -> list:
        return [m['model'] for m in self._client.list()['models']]

    def _generate_text(self, prompt: str = "", system="", schema: Optional[Type[BaseModel]] = None):
        messages = [{"role": "system", "content": system}] if system else []
        messages.append({"role": "user", "content": prompt})

        response = self._client.chat(
            model = self._language_model,
            messages = messages,
            format = schema.model_json_schema() if schema else None
            )
        content = response['message']['content']
        if schema:
            return schema.model_validate_json(content)
        return content

    def _embed_text(self, prompt: str) -> list[float]:
        response = self._client.embed(
            model = self._embedding_model,
            input = prompt)
        return response['embeddings'] if isinstance(prompt, list) else response['embeddings'][0]