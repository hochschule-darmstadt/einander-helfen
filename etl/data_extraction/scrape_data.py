import os
import threading

from importlib import import_module
from inspect import getmembers, isclass

from data_extraction.Scraper import Scraper
from shared.utils import write_data_to_json, get_current_timestamp

# Root Directory (/etl)
ROOT_DIR = os.environ['ROOT_DIR']

# Contains all running scraper threads
scraper_threads = []

# Looks for the given file_name in the /data_extraction/scraper directory
# Checks if the files contains a subclass of Scraper (/data_extraction/Scraper.py) and starts the run function
# Writes the scraped data and errors during the scraping process data_extraction/data and data_extraction/errors
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

        # Create instance of the Scraper sub-class and execute the run method 
        scraper_instance = scraper_class(scraper_file_name)
        scraper_instance.run()

        # Write the data of the scraper to the data_extraction/data directory
        scraper_data = scraper_instance.get_data()
        write_data_to_json(os.path.join(ROOT_DIR, 'data_extraction/data'), f'{scraper_file_name}.json', scraper_data)

        # Write the errors of the scraper to the data_extraction/errors directory
        scraper_errors = scraper_instance.get_errors()    
        if len(scraper_errors):
            time_stamp = get_current_timestamp()
            write_data_to_json(os.path.join(ROOT_DIR, 'data_extraction/errors'), f'{scraper_file_name}_{time_stamp}.log', scraper_errors)
    
    except Exception as err:
        print(err)


#  Starts a thread with the execute_scraper function for all overridden scraper subclasses in /data_extraction/scraper
def run():
    for file_entry in os.scandir(os.path.join(ROOT_DIR, 'data_extraction/scraper')):

        if file_entry.is_file():
            scraper_module_name = os.path.splitext(
                os.path.basename(file_entry))[0]

            # Create a thread with each file in the directory data_extraction/scraper and execute the execute_scraper function with it 
            thread = threading.Thread(target=execute_scraper, args=(scraper_module_name,))
            thread.start()
            scraper_threads.append(thread)

    # Waits for all scraper_threads to finish
    for scraper_thread in scraper_threads:
        scraper_thread.join()
