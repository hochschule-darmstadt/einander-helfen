import json
import os
import time

import requests
from bs4 import BeautifulSoup

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Scraper:
    # Scraper name -> Overwritten by name of the scraper file
    name = 'scraper'

    # Domain to be scraped on
    base_url = 'http://example.com'

    # Show debug information
    debug = False

    # Delay between requests
    delay = 0.5

    # Starting and Ending indices for adding urls via page crawling
    # i.e. example.com?page=5
    start_page = 1
    end_page = None

    urls = []
    data = []
    errors = []

    def __init__(self, name):
        self.name = name

    def run(self):

        if self.debug:
            print(f'Scraper {self.name} started')

        self.start = time.time()

        if not self.end_page:

            try:
                self.override_end_page()

            except Exception as err:
                self.add_error({'func': 'override_end_page', 'body': err})

        if self.start_page and self.end_page:
            self.add_urls_by_index()

        for i, url in enumerate(self.urls):
            time.sleep(self.delay)
            self.crawl(url, i + 1)

        if self.debug:
            print(
                f"[{self.name}] took {(time.time() - self.start):0.2f} seconds to crawl {len(self.urls)} pages from {self.base_url}")
            print(f'Scraper {self.name} ended')

    def crawl(self, url, index):

        if self.debug:
            print(f'[{self.name}] crawling page #{index}')

        try:
            detail_page = self.soupify(url)
            parsed_data = self.parse(detail_page, url)
            self.data.append(parsed_data)

        except Exception as err:
            self.add_error({'func': 'parse', 'body': err, 'index': index, 'url': url})

        if self.debug:
            print(f'[{self.name}] crawling page #{index} ended')

    def add_urls_by_index(self):
        for index in range(self.start_page, self.end_page + 1):

            time.sleep(self.delay)

            if self.debug:
                print(f'[{self.name}] URLs added for page {index} from {self.end_page}.')

            try:
                self.scrape_urls(index)

            except Exception as err:
                self.add_error({'func': 'scrape_urls', 'body': err, 'index': index})

    def get_json_data(self):
        return json.dumps(self.data)

    def get_data(self):
        return self.data

    def add_error(self, err: dict):
        self.errors.append(err)

    @staticmethod
    def soupify(url):
        session = requests.Session()
        res = session.get(url)
        page = BeautifulSoup(res.text, 'html.parser')
        return page

    #   Overwriteable functions for customized Scraping
    @staticmethod
    def parse(response, url):
        return response.text

    def scrape_urls(self, index):
        self.urls.append(self.base_url)

    def override_end_page(self):
        pass
