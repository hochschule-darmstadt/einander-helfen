import os
import sys
import time

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from shared.utils import append_data_to_json, write_data_to_json
from shared.LoggerFactory import LoggerFactory

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Scraper:
    """This class handles the scraping and crawling on a page."""

    # Domain to be scraped on
    base_url = 'http://example.com'

    # Delay between requests
    delay = 0.5

    def __init__(self, name, index):
        """Constructor of the scraper."""

        # Scraper name -> Overwritten by name of the scraper file
        self.name = name

        # The URLs which will be parsed and scraped  
        self.urls = []
        
        # An error object to keep track of error occurences (which is used for logging)
        self.errors = []

        # logger for Scraper
        self.logger = LoggerFactory.get_logger(name)

        # start time of logger
        self.start = None

        self.progress_bar = None

    def run(self):
        """Runs the Scraper.
        Step 1: Adding URLs
        Step 2: Clearing output data file
        Step 3: Crawl each URL in the urls-array"""
        self.logger.debug("run()")
        self.logger.info(f'Scraper {self.name} started')

        self.start = time.time()

        # Add URLs which should be crawled
        try:
            self.add_urls()

        except Exception as err:
            self.logger.exception(f"fn : add_urls, body {str(err)}")

        # Clean existing results
        write_data_to_json(os.path.join(ROOT_DIR, 'data_extraction/data', f'{self.name}.json'), [])

        # Iterate over URLs and crawl each page
        for i, url in enumerate(self.urls):
            time.sleep(self.delay)
            self.crawl(url, i + 1)

        crawling_time = "{:.2f}".format((time.time() - self.start))
        self.logger.debug(f"[{self.name}] took {crawling_time} seconds to crawl {len(self.urls)}"
                          f" pages from {self.base_url}")

    def crawl(self, url, index):
        """Crawls page, runs the parse function over the GET-result and appends it to the existing data output file."""
        self.logger.debug("crawl()")
        self.logger.debug(f'[{self.name}] Scraping page #{index} [{index}/{len(self.urls)}]')

        try:
            detail_page = self.soupify(url)
            parsed_data = self.parse(detail_page, url)
            if parsed_data is not None:
                append_data_to_json(os.path.join(ROOT_DIR, 'data_extraction/data', f'{self.name}.json'), parsed_data)

        except Exception as err:
            self.logger.exception(f'fn : parse, body {str(err)}, index: {index}, url:{url}')

        self.logger.debug(f'[{self.name}] Scraping page #{index} ended')
        self.get_progress_data_crawling(index, len(self.urls))

    def soupify(self, url):
        """Executes GET-request with the given url, transforms it to a BeautifulSoup object and returns it."""
        self.logger.debug("soupify()")

        res = requests.get(url)
        page = BeautifulSoup(res.text, 'html.parser')
        return page

    def soupify_post(self, url, form_data):
        """Executes POST-request with the given url and form data, transforms it to a BeautifulSoup object and returns
           it."""
        self.logger.debug("soupify_post()")

        res = requests.post(url, data=form_data)
        page = BeautifulSoup(res.text, 'html.parser')
        return page

    def soupify_post_session(self, url, form_data, session):
        """Executes POST-request with the given url, form data and session, transforms it to a BeautifulSoup object and
           returns it."""
        self.logger.debug("soupify_post_session()")

        if session is None:
            session = requests.Session()

        res = session.post(url, data=form_data)

        page = BeautifulSoup(res.text, 'html.parser')
        return page, session

    def parse(self, response, url):
        """Transforms the soupified response of a detail page in a predefined way and returns it."""
        self.logger.debug("parse()")

        return response.text

    def add_urls(self):
        """Adds URLs to an array which is later iterated over and scraped each."""
        self.logger.debug("add_urls()")

        self.urls.append(self.base_url)

    def remove_unnecessary_whitespaces(self, value):
        """Removes duplicate and leading or trailing whitespaces in a string"""
        self.logger.debug("remove_unnecessary_whitespaces()")

        if value is None:
            return None
        return ' '.join(value.split())

    def clean_string(self, value, *optional_replacement_argument):
        """Removes all line breaks, tabs and leading or trailing whitespaces from a string. The optional argument
        optional_replacement_argument lets you specify a string to substitute the replaced tags"""
        self.logger.debug("clean_string()")

        if value is None:
            return None
        if len(optional_replacement_argument) == 0:
            replace_with = ''
        else:
            if optional_replacement_argument[0] is not None:
                replace_with = optional_replacement_argument[0]
            else:
                replace_with = ''

        return value.replace('\n', replace_with).replace('\r', replace_with).replace('\t', replace_with).strip()

    def clean_html_tags(self, value):
        """Removes all html tags."""
        self.logger.debug("clean_html_tags()")

        if value is None:
            return None

        return BeautifulSoup(value, 'lxml').text

    def get_progress_data_fetching(self, current, total):
        """ Updates progress data of fetching process for crawler and triggers print of progeess bar"""
        self.logger.debug("get_progress_data_fetching()")

        self.get_progress_data(current, total, 'FETCH')

    def get_progress_data_crawling(self, current, total):
        """ Updates progress data of crawling for crawler and triggers print of progeess bar"""
        self.logger.debug("get_progress_data_crawling()")

        self.get_progress_data(current, total, 'CRAWL')

    def get_progress_data(self, current, total, phase):
        """ Updates progress for crawler and triggers print of progeess bar"""
        self.logger.debug("get_progress_data()")

        current = int(current)
        total = int(total)

        if self.progress_bar is None:
            self.progress_bar = tqdm(desc=f'[{phase}ING] {self.name}:',
                                     total=total,
                                     mininterval=5,
                                     position=0,
                                     file=sys.stdout,
                                     bar_format='{desc:45} {percentage:3.0f}%|{bar:50}| {n_fmt}/{total_fmt} [{elapsed}] ')

        self.progress_bar.update()

        if current == total:
            self.progress_bar.set_description(f'✓ [{phase}ED] {self.name}')
            self.progress_bar.close()
            self.progress_bar = None
