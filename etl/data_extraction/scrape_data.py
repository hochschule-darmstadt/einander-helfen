import os
import threading
from importlib import import_module
from inspect import getmembers, isclass

from data_extraction.Scraper import Scraper
from shared.utils import write_data_to_json

# Root Directory (/etl)
ROOT_DIR = os.environ['ROOT_DIR']

# Contains all running scraper threads
scraper_threads = []

# Dictionary with file name of scraper as the key and the scraped data as an array 
scraper_results = {}


# Looks for the given file_name in the /data_extraction/scraper directory
# Checks if the files contains a subclass of Scraper (/data_extraction/Scraper.py) and starts the run function
def execute_scraper(scraper_file_name: str):
    scraper_module = import_module(f'data_extraction.scraper.{scraper_file_name}')
    scraper_class = None

    # Looks for a derived sub-class of class 'Scraper' in imported module
    for name, scraper_sub_class in getmembers(scraper_module):
        if name != 'Scraper' and isclass(scraper_sub_class) and issubclass(scraper_sub_class, Scraper):
            scraper_class = scraper_sub_class

    if not scraper_class:
        raise Exception(f'[{scraper_file_name}] Error: No sub-class of class Scraper found')

    scraper_instance = scraper_class(scraper_file_name)
    scraper_instance.run()

    scraper_results[scraper_file_name] = scraper_instance.get_data()
    scraper_errors = scraper_instance.get_errors()

    if len(scraper_errors):
        write_data_to_json(os.path.join(ROOT_PATH, 'data_extraction/errors'), f'{scraper_file_name}.log', scraper_errors)


#  Starts a thread with the execute_scraper function for all overridden scraper subclasses in /data_extraction/scraper
#  Returns the results of all scrapers as a dict-object with the file name of the scraper as key
#  and the scraped data (array) as value
def run():
    for file_entry in os.scandir(os.path.join(ROOT_DIR, 'data_extraction/scraper')):

        if file_entry.is_file():
            scraper_module_name = os.path.splitext(
                os.path.basename(file_entry))[0]

            thread = threading.Thread(target=execute_scraper, args=(scraper_module_name,))
            thread.start()
            scraper_threads.append(thread)

    for scraper_thread in scraper_threads:
        scraper_thread.join()

    return scraper_results
