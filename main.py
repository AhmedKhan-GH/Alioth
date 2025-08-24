# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os

from dotenv import load_dotenv

from alioth.app.application import run_application
from alioth.core.environment import *
from alioth.core.bootstrap import *

log = logging.getLogger(__name__)

setup_logging(handlers=[logging.StreamHandler(sys.stdout),
                        logging.FileHandler('app.log', mode='w')])

@try_catch(exit_code = 1, verbose=True)
def main():

    load_dotenv()

    check_environment_vars(['OPENAI_API_KEY'])

    run_application()


if __name__ == '__main__':
    main()