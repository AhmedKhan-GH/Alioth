from alioth.providers.ollama_modelclient import *
from alioth.providers.openai_modelclient import *

log = logging.getLogger(__name__)

@try_catch()
def run_application():
    """Main Alioth application logic."""
    log.info("Activating Alioth")

    # we can create provider model clients
    # that can be used interchangeably
    oll = OllamaModelClient()
    oai = OpenAIModelClient()

    # we can observe the models available
    oll.list_models()
    oai.list_models()

    # we can specify the model it uses at runtime
    oll.set_model("llama3.2:3b")
    oai.set_model("gpt-5-nano")

    class Country(BaseModel):
        capitol: str
        population: int

    for c in [oll, oai]:
        # we can interchangeably operate on different model providers and query either
        # with string prompts or pydantic schema structured outputs?
        print(c.generate_text("Briefly answer what is the largest state in America?"))
        print(c.generate_text("Answer about the United States of America", Country))

    # next objective, create ResponseService, what does it need to achieve?

    log.info("Deactivating Alioth")

