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
    oll.set_language_model("llama3.2:3b")
    oai.set_language_model("gpt-5-nano")

    oll.set_embedding_model("mxbai-embed-large:latest")
    oai.set_embedding_model("text-embedding-3-large")

    class Country(BaseModel):
        capitol: str
        population: int

    for c in [oll, oai]:
        # we can interchangeably operate on different model providers and query either
        # with string prompts or pydantic schema structured outputs?
        #print(c.generate_text(prompt = "what is the largest state in america?", system = "you are an elementary school teacher"))
            #prompt = "Briefly answer what is the largest state in America?",
            #system = "You are an astute scholar that provides research-level answers to questions."))
        #print(c.generate_text(prompt = "Answer about the United States of America", schema=Country))

        print(c.embed_text("What is the capital of California?"))


    # next objective, create ResponseService, what does it need to achieve?

    log.info("Deactivating Alioth")

