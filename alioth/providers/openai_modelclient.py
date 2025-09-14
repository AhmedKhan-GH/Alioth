from openai import OpenAI

from ..core.modelclient import *
from ..core.connection import *
from ..core.environment import *

class OpenAIModelClient(ModelClient):
    """OpenAI client provider."""

    def _check_connection(self) -> bool:
        api_key = get_environment_variable('OPENAI_API_KEY', required = True)
        return check_url_connection('https://api.openai.com/v1/models', headers = {'Authorization': f"Bearer {api_key}"})

    def _create_client(self):
        return OpenAI(api_key = get_environment_variable('OPENAI_API_KEY', required = True))

    def _list_models(self) -> list:
        return [m.id for m in self._client.models.list().data]

    def _generate_text(self, prompt: str = "", system="", schema: Optional[Type[BaseModel]] = None):
        messages = [{"role": "developer", "content": system}] if system else []
        messages.append({"role": "user", "content": prompt})

        if schema:
            response = self._client.responses.parse(
                model=self._language_model,
                input=messages,
                text_format=schema
            )
            return response.output_parsed
        else:
            response = self._client.responses.create(
                model=self._language_model,
                input=messages,
            )
            return response.output_text
