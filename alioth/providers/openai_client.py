from openai import OpenAI

from ..core.base_client import *
from ..core.connection import *
from ..core.environment import *

class OpenAIClient(BaseClient):
    """OpenAI client provider."""

    def _check_connection(self) -> bool:
        api_key = get_environment_variable('OPENAI_API_KEY', required = True)
        return check_url_connection('https://api.openai.com/v1/models', headers = {'Authorization': f"Bearer {api_key}"})

    def _create_client(self):
        return OpenAI(api_key = get_environment_variable('OPENAI_API_KEY', required = True))

    def _list_models(self) -> list:
        return [m.id for m in self._client.models.list().data]