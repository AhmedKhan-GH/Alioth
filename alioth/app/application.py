from alioth.providers.ollama_modelclient import *
from alioth.providers.openai_modelclient import *

log = logging.getLogger(__name__)

@try_catch()
def run_application():
    """Main Alioth application logic."""
    log.info("Activating Alioth")

    oll = OllamaModelClient('llama3.2:3b')
    oai = OpenAIModelClient('gpt-5-nano')

    for c in [oll, oai]:
        print(c.list_models())
        print(c.generate_text("hello? give a short response"))
        class Country(BaseModel):
            capitol: str
            population: int
        print(c.generate_text("Answer about the United States of America", Country))

    # next objective, create ResponseService

    log.info("Deactivating Alioth")

