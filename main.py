# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os

from dotenv import load_dotenv
import logging
import sys

from alioth.app.application import run_application
from alioth.core.bootstrap import setup_logging
from alioth.core.decorators import try_catch
import alioth.core.environment as env

log = logging.getLogger(__name__)

setup_logging(level=logging.DEBUG,
              handlers=[logging.FileHandler('app.log', mode='w'),
                        logging.StreamHandler(sys.stdout)])

@try_catch()
def main():

    #verifies we can read environment vars and write logs
    env.check_filesystem_access()

    #loads environment vars from the.env file after verification
    load_dotenv()

    #we can ignore this as we will instead be checking lazily
    #verifies we have all the required environment vars
    #env.check_required_environment_vars(['OPENAI_API_KEY'])

    run_application()


if __name__ == '__main__':
    main()