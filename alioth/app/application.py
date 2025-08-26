import openai

from alioth.core.connection import *
from alioth.core.environment import *
from alioth.core.base_client import *
from alioth.providers.ollama_client import OllamaClient
from alioth.providers.openai_client import *

log = logging.getLogger(__name__)

@try_catch()
def run_application():
    """Main Alioth application logic."""
    log.info("Activating Alioth")

    oai = OpenAIClient()
    oai.check_connection()

    oll = OllamaClient()
    oll.check_connection()
    # need to check ollama connection here before creating a client

    log.info("Deactivating Alioth")

