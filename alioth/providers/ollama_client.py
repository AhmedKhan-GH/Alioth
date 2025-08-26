from ..core.base_client import *
from ..core.connection import *
from ..core.environment import *

class OllamaClient(BaseClient):
    """Ollama client provider."""
    def __init__(self):
        super().__init__()

    @try_catch(exit_on_error=False, default_return=False)
    def _check_connection(self) -> bool:
        return check_url_connection("http://localhost:11434/api/tags")
