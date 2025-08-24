# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os

from dotenv import load_dotenv
import logging
import sys

from alioth.app.application import run_application
from alioth.core.environment import check_environment_vars
from alioth.core.bootstrap import setup_logging
from alioth.core.decorators import try_catch

log = logging.getLogger(__name__)

setup_logging(level=logging.DEBUG,
              handlers=[logging.FileHandler('app.log', mode='w'),
                        logging.StreamHandler(sys.stdout)])

@try_catch()
def main():

    load_dotenv()

    check_environment_vars(['OPENAI_API_KEY'])

    run_application()


if __name__ == '__main__':
    main()