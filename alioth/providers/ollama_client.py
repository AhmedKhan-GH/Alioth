from ..core.base_client import *
from ..core.connection import *
from ..core.environment import *

import ollama

class OllamaClient(BaseClient):
    """Ollama client provider."""

    def _check_connection(self) -> bool:
        return check_url_connection("http://localhost:11434/api/tags")

    def _create_client(self) -> Any:
        return ollama.Client()