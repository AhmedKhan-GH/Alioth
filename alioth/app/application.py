import openai

from alioth.core.clients import OpenAIClient
from alioth.core.connection import *
from alioth.core.environment import *
from alioth.core.clients import *

log = logging.getLogger(__name__)

@try_catch()
def run_application():
    """Main Alioth application logic."""
    log.info("Activating Alioth")

    openai_connection_status = check_url_connection('https://api.openai.com/v1/models',
    {'Authorization': f'Bearer {get_environment_variable("OPENAI_API_KEY", required = True)}'})

    log.info(f"OpenAI API connection status: {'OK' if openai_connection_status else 'FAILED'}")

    oai_client = openai.OpenAI()
    oai_adapter = OpenAIClient(client = oai_client, model ='gpt-5')
    print(answer_prompt(adapter = oai_adapter, prompt = "testing?"))

    ollama_connection_status = check_port_connection('localhost', 11434)
    log.info(f"Ollama API connection status: {'OK' if ollama_connection_status else 'FAILED'}")

    oll_client = ollama.Client(host = "http://localhost:11434")
    oll_adapter = OllamaClientAdapter(client = oll_client, model = 'llama2')
    print(answer_prompt(adapter = oll_adapter, prompt = "testing?"))


    log.info("Deactivating Alioth")