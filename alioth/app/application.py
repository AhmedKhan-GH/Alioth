
from alioth.providers.ollama_modelclient import *
from alioth.providers.openai_modelclient import *
from alioth.providers.postgres_databaseclient import PostgresDatabaseClient
from alioth.services.fileservice import *
from alioth.providers.chromadb_vectorclient import *
import random

import matplotlib.pyplot as plt

log = logging.getLogger(__name__)

def ai_model_test():
    # we can create provider model clients
    # that can be used interchangeably
    oai = OpenAIModelClient()

    # we can observe the models available
    oai.list_models()

    # we can specify the model it uses at runtime
    oai.set_language_model("gpt-5-nano")

    oai.set_embedding_model("text-embedding-3-large")

    class Country(BaseModel):
        capitol: str
        population: int

    for c in [oai]:
        # we can interchangeably operate on different model providers and query either
        # with string prompts or pydantic schema structured outputs?
        print(c.generate_text(prompt = "what is the largest state in america?", system = "you are an elementary school teacher"))
            #prompt = "Briefly answer what is the largest state in America?",
            #system = "You are an astute scholar that provides research-level answers to questions."))
        print(c.generate_text(prompt = "Answer about the United States of America", schema=Country))

def chunking_test():

    file_path = '/Users/ahmed/Library/Mobile Documents/com~apple~CloudDocs/Eagle/Books.library/images/MELSY8Y3XB9HZ.info/Kimothi RetrievalAugmentedGeneration 1E.pdf'
    save_path = '/Users/ahmed/PycharmProjects/Alioth/alioth/markdowns/highlighted.pdf'

    new_file_path = '/Users/ahmed/Library/Mobile Documents/com~apple~CloudDocs/Eagle/Books.library/images/MFP10EXGITV2G.info/Alonso InformationRetrieval 1E.pdf'

    fs = FileService(new_file_path)
    block_list = fs.get_block_list()

    reverse_sort = block_list.sort(key=lambda x: len(x["text"]), reverse=True)
    for bnum, b in enumerate(block_list, start=1):
        print(bnum, ": ", b["pnum"], ": ", b["text"], "\n\n")

    fs.live_highlight_view(block_list[0])

    plot_text_lengths(block_list)

    #fs.get_embeddings() -> list[list[float]]
    #internally it will pass around various methods
    #that break the text, pass to api, etc

    #import fileservice as fs
    #fs.method()
    # for file in list
        #fs.chunk(file)
    # need one method given a filepath, will return
    #
    # {page, bbox (x0, y0, x1, y1), text}

    #fs = FileService(filepath)
    #


    #fs.save_chunks_to_markdown(save_path, chunks)
    #print("\n\n".join(fs.make_chunks_into_list(chunks)))

def plot_text_lengths(block_list):

    text_lengths = [len(block["text"]) for block in block_list]
    plt.figure(figsize=(10, 6))
    plt.hist(text_lengths, bins=50, edgecolor='black')
    plt.title('Distribution of Text Block Lengths')
    plt.xlabel('Text Length')
    plt.ylabel('Frequency')
    plt.show()


def chromadb_test():
    chr = ChromaDBVectorClient()

def postgres_test():
    post = PostgresDatabaseClient()
    print(post.check_connection())
    post.test_database()

#@try_catch(exit_on_error=True, default_return=None)
def run_application():
    """Main Alioth application logic."""
    log.info("Activating Alioth")

    #chunking_test()
    postgres_test()

    log.info("Deactivating Alioth")
    
 
