import os
import threading

from importlib import import_module
from inspect import getmembers, isclass

from data_extraction.scraper import Scraper
from shared.LoggerFactory import LoggerFactory

# Root Directory (/etl)
ROOT_DIR = os.environ['ROOT_DIR']
logger = LoggerFactory.get_general_logger()

# Contains all running scraper threads
scraper_threads = []


def execute_scraper(scraper_file_name: str):
    """Looks for the given file_name in the /data_extraction/scraper directory.
    Checks if the files contains a subclass of Scraper (/data_extraction/Scraper.py) and starts the run function.
    Writes the scraped data and errors during the scraping process data_extraction/data and data_extraction/errors."""
    logger.debug('execute_scraper()')
    logger.info(f'execute_scraper for {scraper_file_name}')
    try:
        scraper_module = import_module(f'data_extraction.scrapers.{scraper_file_name}')
        scraper_class = None

        # Looks for a derived sub-class of class 'Scraper' in imported module
        for name, scraper_sub_class in getmembers(scraper_module):
            if name != 'Scraper' and isclass(scraper_sub_class) and issubclass(scraper_sub_class, Scraper):
                scraper_class = scraper_sub_class

        if not scraper_class:
            raise Exception(f'[{scraper_file_name}] Error: No sub-class of class Scraper found')

        # Create instance of the Scraper sub-class and execute the run method 
        scraper_instance = scraper_class(scraper_file_name)
        scraper_instance.run()

    except Exception as err:
        logger.exception(err)


def run():
    """Starts a thread with the execute_scraper function for all overridden scraper subclasses in
    /data_extraction/scraper."""
    logger.debug('run()')
    for i, file_entry in enumerate(os.scandir(os.path.join(ROOT_DIR, 'data_extraction/scrapers'))):

        if file_entry.is_file():
            scraper_module_name = os.path.splitext(
                os.path.basename(file_entry))[0]

            # Create a thread with each file in the directory data_extraction/scraper
            # and execute the execute_scraper function with it
            thread = threading.Thread(target=execute_scraper, args=(scraper_module_name,))
            thread.start()
            scraper_threads.append(thread)

    # Waits for all scraper_threads to finish
    for scraper_thread in scraper_threads:
        scraper_thread.join()

    # Prevents double output of the last progress bar
    print(' '*200)
    logger.info('All crawlers were successfully executed')
