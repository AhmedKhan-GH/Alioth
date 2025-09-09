from alioth.providers.ollama_client import OllamaClient
from alioth.providers.openai_client import *

log = logging.getLogger(__name__)

@try_catch()
def run_application():
    """Main Alioth application logic."""
    log.info("Activating Alioth")

    oai = OpenAIClient('gpt-5-nano')

    oll = OllamaClient('tinyllama:latest')

    clients = [oai, oll]
    for c in clients:
        print(c.list_models())

    print(oai.generate_text("hello? give a short response"))


    log.info("Deactivating Alioth")

