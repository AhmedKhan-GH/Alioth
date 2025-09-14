from ..core.modelclient import *
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

    def _generate_text(self, prompt: str = "", schema: Optional[Type[BaseModel]] = None):
        response = self._client.chat(
            model = self._model,
            messages =
                [{
                    'role': 'user',
                    'content': prompt
                }],
            format = schema.model_json_schema() if schema else None
            )
        content = response['message']['content']
        if schema:
            return schema.model_validate_json(content)
        return content