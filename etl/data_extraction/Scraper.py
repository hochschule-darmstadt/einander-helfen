import json
import os
import time

import requests
from bs4 import BeautifulSoup

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Scraper:
    # Domain to be scraped on
    base_url = 'http://example.com'

    # Show debug information
    debug = False

    # Delay between requests
    delay = 0.5

    def __init__(self, name):
        # Scraper name -> Overwritten by name of the scraper file
        self.name = name
        
        # The URLs which will be parsed and scraped  
        self.urls = []
        
        # And array of the data of the scraped pages (each entry holds the scraped and parsed information of a detail page)
        self.data = []
        
        # An error object to keep track of error occurences (which is used for logging)
        self.errors = []

    # Runs the Scraper 
    # Step 1: Adding URLs
    # Step 2: Crawl each URL in the urls-array
    def run(self):

        if self.debug:
            print(f'Scraper {self.name} started')

        self.start = time.time()

        # Add URLs which should be crawled
        try:
            self.add_urls()

        except Exception as err:
            self.add_error({'fn': 'add_urls', 'body': str(err)})

        # Iterate over URLs and crawl each page
        for i, url in enumerate(self.urls):
            time.sleep(self.delay)
            self.crawl(url, i + 1)

        if self.debug:
            print(
                f"[{self.name}] took {(time.time() - self.start):0.2f} seconds to crawl {len(self.urls)} pages from {self.base_url}")
            print(f'Scraper {self.name} ended')

    # Crawls page, runs the parse function over the GET-result and appends it to the data-array 
    def crawl(self, url, index):

        if self.debug:
            print(f'[{self.name}] Scraping page #{index} [{index}/{len(self.urls)}]')

        try:
            detail_page = self.soupify(url)
            parsed_data = self.parse(detail_page, url)
            self.data.append(parsed_data)

        except Exception as err:
            self.add_error({'fn': 'parse', 'body': str(err), 'index': index, 'url': url})

        if self.debug:
            print(f'[{self.name}] Scraping page #{index} ended')

    # Returns data of the Scraper
    def get_data(self):
        return self.data

    # Returns data of the Scraper in JSON-Format
    def get_json_data(self):
        return json.dumps(self.data)

    # Returns errors of scraping process
    def get_errors(self):
        return self.errors

    # Adds error to the error object (used for logging)
    def add_error(self, err: dict):
        if self.debug:
            print(f'Error [{self.name}]:', err)
        self.errors.append(err)

    # Executes GET-request with the given url, transforms it to a BeautifulSoup object and returns it
    @staticmethod
    def soupify(url):
        res = requests.get(url)
        page = BeautifulSoup(res.text, 'html.parser')
        return page

    #   Transforms the soupified response of a detail page in a predefined way and returns it
    @staticmethod
    def parse(response, url):
        return response.text

    #   Adds URLs to an array which is later iterated over and scraped each
    def add_urls(self):
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
