from alioth.providers.ollama_modelclient import *
from alioth.providers.openai_modelclient import *

log = logging.getLogger(__name__)

@try_catch()
def run_application():
    """Main Alioth application logic."""
    log.info("Activating Alioth")

    oai = OpenAIModelClient('gpt-5-nano')

    oll = OllamaModelClient('llama3.2:3b')

    clients = [oai, oll]
    for c in clients:
        print(c.list_models())
        print(c.generate_text("hello? give a short response"))

    # next objective, create ResponseService

    log.info("Deactivating Alioth")

