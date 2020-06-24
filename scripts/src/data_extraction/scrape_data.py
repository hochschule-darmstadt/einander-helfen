import os
import threading
from importlib import import_module
from inspect import getmembers, isclass

from data_extraction.Scraper import Scraper

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

scraper_threads = []
scraper_results = {}


def execute_scraper(scraper_file_name: str):
    try:

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

    except Exception as err:
        print(err)
        return


def run():
    for file_entry in os.scandir(f'{ROOT_DIR}/data_extraction/scraper'):

        if file_entry.is_file():
            scraper_module_name = os.path.splitext(
                os.path.basename(file_entry))[0]

            thread = threading.Thread(target=execute_scraper, args=(scraper_module_name,))
            thread.start()
            scraper_threads.append(thread)

    for scraper_thread in scraper_threads:
        scraper_thread.join()

    return scraper_results
