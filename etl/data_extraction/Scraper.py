import os
import time

import requests
from bs4 import BeautifulSoup

from shared.utils import append_data_to_json, write_data_to_json

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Scraper:
    """This class handles the scraping and crawling on a page."""

    # Domain to be scraped on
    base_url = 'http://example.com'

    # Show debug information
    debug = False

    # Delay between requests
    delay = 0.5

    def __init__(self, name):
        """Constructor of the scraper."""

        # Scraper name -> Overwritten by name of the scraper file
        self.name = name
        
        # The URLs which will be parsed and scraped  
        self.urls = []
        
        # An error object to keep track of error occurences (which is used for logging)
        self.errors = []

    def run(self):
        """Runs the Scraper.
        Step 1: Adding URLs
        Step 2: Clearing output data file
        Step 3: Crawl each URL in the urls-array"""

        if self.debug:
            print(f'Scraper {self.name} started')

        self.start = time.time()

        # Add URLs which should be crawled
        try:
            self.add_urls()

        except Exception as err:
            self.add_error({'fn': 'add_urls', 'body': str(err)})

        # Clean existing results
        write_data_to_json(os.path.join(ROOT_DIR, 'data_extraction/data', f'{self.name}.json'), [])

        # Iterate over URLs and crawl each page
        for i, url in enumerate(self.urls):
            time.sleep(self.delay)
            self.crawl(url, i + 1)

        if self.debug:
            print(
                f"[{self.name}] took {(time.time() - self.start):0.2f} seconds to crawl {len(self.urls)} pages from {self.base_url}")
            print(f'Scraper {self.name} ended')

    def crawl(self, url, index):
        """Crawls page, runs the parse function over the GET-result and appends it to the existing data output file."""

        if self.debug:
            print(f'[{self.name}] Scraping page #{index} [{index}/{len(self.urls)}]')

        try:
            detail_page = self.soupify(url)
            parsed_data = self.parse(detail_page, url)
            append_data_to_json(os.path.join(ROOT_DIR, 'data_extraction/data', f'{self.name}.json'), parsed_data)

        except Exception as err:
            self.add_error({'fn': 'parse', 'body': str(err), 'index': index, 'url': url})

        if self.debug:
            print(f'[{self.name}] Scraping page #{index} ended')

    def get_errors(self):
        """Returns errors of scraping process."""
        return self.errors

    def add_error(self, err: dict):
        """Adds error to the error object (used for logging)."""

        if self.debug:
            print(f'Error [{self.name}]:', err)
        self.errors.append(err)

    @staticmethod
    def soupify(url):
        """Executes GET-request with the given url, transforms it to a BeautifulSoup object and returns it."""

        res = requests.get(url)
        page = BeautifulSoup(res.text, 'html.parser')
        return page

    @staticmethod
    def soupify_post(url, form_data):
        """Executes POST-request with the given url and form data, transforms it to a BeautifulSoup object and returns it."""

        res = requests.post(url, data=form_data)
        page = BeautifulSoup(res.text, 'html.parser')
        return page

    @staticmethod
    def parse(response, url):
        """Transforms the soupified response of a detail page in a predefined way and returns it."""

        return response.text

    def add_urls(self):
        """Adds URLs to an array which is later iterated over and scraped each."""

        self.urls.append(self.base_url)

    @staticmethod
    def clean_string(value):
        """Removes all line breaks, tabs and leading or trailing whitespaces from a string."""

        if value is None:
            return None

        return value.replace('\n', '').replace('\r', '').replace('\t', '').strip()

    @staticmethod
    def clean_html_tags(value):
        """Removes all html tags."""

        if value is None:
            return None

        return BeautifulSoup(value, 'lxml').text
