from alioth.providers.ollama_client import OllamaClient
from alioth.providers.openai_client import *

log = logging.getLogger(__name__)

@try_catch()
def run_application():
    """Main Alioth application logic."""
    log.info("Activating Alioth")

    oai = OpenAIClient()

    oll = OllamaClient()

    log.info("Deactivating Alioth")

