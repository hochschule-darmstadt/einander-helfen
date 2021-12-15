import os
import sys
import time

import requests
from lxml.html.clean import Cleaner
from bs4 import BeautifulSoup
from tqdm import tqdm

from shared.utils import append_data_to_json, write_data_to_json
from shared.logger_factory import LoggerFactory
from shared.stats_collector import StatsCollector

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Scraper:
    """This class handles the scraping and crawling on a page."""

    # Domain to be scraped on
    base_url = 'http://example.com'

    # Delay between requests
    delay = 0.5

    def __init__(self, name, context):
        """Constructor of the scraper."""

        # Scraper name -> Overwritten by name of the scraper file
        self.name = name

        # Scraper location context
        self.context = context

        # The URLs which will be parsed and scraped  
        self.urls = []
        
        # An error object to keep track of error occurences (which is used for logging)
        self.errors = []

        # logger for Scraper
        self.logger = LoggerFactory.get_logger(name)

        # stats for Scraper
        self.stats = StatsCollector.get_stats_collector(name)

        # start time of logger
        self.start = None

        self.progress_bar = None

        self._init_cleaner()

    def run(self):
        """Runs the Scraper.
        Step 1: Adding URLs
        Step 2: Clearing output data file
        Step 3: Crawl each URL in the urls-array"""
        self.logger.info(f'Scraper {self.name} started')

        self.start = time.time()

        # Add URLs which should be crawled
        try:
            self.add_urls()

        except Exception as err:
            self.logger.exception(f'fn : add_urls, body {str(err)}')
            self.stats.add_error_message(StatsCollector.ERROR_TYPE_FETCHING, str(err))

        # Clean existing results
        write_data_to_json(os.path.join(ROOT_DIR, f'data_extraction/data/{self.context}', f'{self.name}.json'), [])

        # Iterate over URLs and crawl each page
        for i, url in enumerate(self.urls):
            time.sleep(self.delay)
            self.crawl(url, i + 1)

        crawling_time = '{:.2f}'.format((time.time() - self.start))
        self.stats.set_crawling_duration(crawling_time)
        self.logger.debug(f'[{self.name}] took {crawling_time} seconds to crawl {len(self.urls)}'
                          f' pages from {self.base_url}')

    def crawl(self, url, index):
        """Crawls page, runs the parse function over the GET-result and appends it to the existing data output file."""
        self.logger.debug('crawl()')
        self.logger.debug(f'[{self.name}] Scraping page #{index} [{index}/{len(self.urls)}]')

        try:
            detail_page = self.soupify(url)
            parsed_data = self.parse(detail_page, url)

            keys_to_skip = ['categories', 'link', 'source', 'geo_location', 'post_struct']

            if parsed_data is not None:
                for key in parsed_data.keys():
                    if key not in keys_to_skip and parsed_data[key] is not None and len(parsed_data[key]) > 2:
                        parsed_data[key] = self.sanitize_html(parsed_data[key])
                append_data_to_json(os.path.join(ROOT_DIR, f'data_extraction/data/{self.context}', f'{self.name}.json'), parsed_data)
                self.stats.inc_crawling_successful()
            else:
                self.stats.inc_crawling_empty_posts()

        except Exception as err:
            self.logger.exception(f'fn : parse, body {str(err)}, index: {index}, url:{url}')
            self.stats.add_error_message(StatsCollector.ERROR_TYPE_PARSING, str(err))

        self.logger.debug(f'[{self.name}] Scraping page #{index} ended')
        self.update_crawling_progress(index, len(self.urls))

    def soupify(self, url):
        """Executes GET-request with the given url, transforms it to a BeautifulSoup object and returns it."""
        self.logger.debug('soupify()')

        res = requests.get(url)
        page = BeautifulSoup(res.text, 'html.parser')
        return page

    def soupify_post(self, url, form_data):
        """Executes POST-request with the given url and form data, transforms it to a BeautifulSoup object and returns
           it."""
        self.logger.debug('soupify_post()')

        res = requests.post(url, data=form_data)
        page = BeautifulSoup(res.text, 'html.parser')
        return page

    def soupify_post_session(self, url, form_data, session):
        """Executes POST-request with the given url, form data and session, transforms it to a BeautifulSoup object and
           returns it."""
        self.logger.debug('soupify_post_session()')

        if session is None:
            session = requests.Session()

        res = session.post(url, data=form_data)

        page = BeautifulSoup(res.text, 'html.parser')
        return page, session

    def rest_post(self, url, json):
        """Executes POST-request with the given url and json data, returns the response."""
        self.logger.debug('rest_post()')

        res = requests.post(url, data=json, headers={'Content-Type': 'application/json'})
        return res
    
    def parse(self, response, url):
        """Transforms the soupified response of a detail page in a predefined way and returns it."""
        self.logger.debug('parse()')

        return response.text

    def add_urls(self):
        """Adds URLs to an array which is later iterated over and scraped each."""
        self.logger.debug('add_urls()')

        self.urls.append(self.base_url)

    def remove_unnecessary_whitespaces(self, value):
        """Removes duplicate and leading or trailing whitespaces in a string. """
        self.logger.debug('remove_unnecessary_whitespaces()')

        if value is None:
            return None
        return ' '.join(value.split())

    def clean_string(self, value, *optional_replacement_argument):
        """Removes all line breaks, tabs and leading or trailing whitespaces from a string. The optional argument
        optional_replacement_argument lets you specify a string to substitute the replaced tags"""
        self.logger.debug('clean_string()')

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
        self.logger.debug('clean_html_tags()')

        if value is None:
            return None

        return BeautifulSoup(value, 'lxml').text

    def sanitize_html(self, value):
        """Cleans html tags from css and javascript content"""
        self.logger.debug('sanitize_html()')

        cleaned_value = str(self.cleaner.clean_html(value))
        if cleaned_value.startswith('<p>') and cleaned_value.endswith('</p>'):
            cleaned_value = cleaned_value[3:-4]

        return cleaned_value

    def update_fetching_progress(self, current, total):
        """ Updates progress data of fetching process for crawler and triggers print of progress bar. """
        self.logger.debug('get_progress_data_fetching()')

        self.update_progress(current, total, 'FETCH')

    def update_crawling_progress(self, current, total):
        """ Updates progress data of crawling for crawler and triggers print of progress bar. """
        self.logger.debug('get_progress_data_crawling()')

        if current == 1 and self.progress_bar is not None:
            self.progress_bar.set_description(f'[FETCHED] {self.name}')
            self.progress_bar.close()
            self.progress_bar = None

        self.update_progress(current, total, 'CRAWL')

    def update_progress(self, current, total, phase):
        """ Updates progress for crawler and triggers print of progress bar. """
        self.logger.debug('get_progress_data()')

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
            self.progress_bar.set_description(f'[{phase}ED] {self.name}')
            self.progress_bar.close()
            self.progress_bar = None

    def set_progress_completed(self, total, phase):
        """ Set unfinished progress bar to completed. """
        total = int(total)

        self.progress_bar = tqdm(desc=f'[{phase}ING] {self.name}:',
                                 total=total,
                                 mininterval=5,
                                 position=0,
                                 file=sys.stdout,
                                 bar_format='{desc:45} {percentage:3.0f}%|{bar:50}| {n_fmt}/{total_fmt} [{elapsed}] ')

        self.progress_bar.update(total)

        self.progress_bar.set_description(f'[{phase}ED] {self.name}')
        self.progress_bar.close()
        self.progress_bar = None

    def _init_cleaner(self):
        """ Initializes the cleaner used to sanitize fields that may contain html tags. """
        self.cleaner = Cleaner()
        self.cleaner.scripts = True  # Removes any <script> tags.
        self.cleaner.javascript = True  # Removes any Javascript, like an onclick attribute. Also removes stylesheets as they could contain Javascript.
        self.cleaner.style = True  # Removes any style tags.
        self.cleaner.inline_style = True  # Removes any style attributes. Defaults to the value of the style option.
        self.cleaner.frames = True  # Removes any frame-related tags
        self.cleaner.forms = True  # Removes any form tags
        self.cleaner.annoying_tags = True  # Tags that aren't wrong, but are annoying.
        self.cleaner.remove_unknown_tags = True  # Remove any tags that aren't standard parts of HTML.
        self.cleaner.comments = True  # Removes any comments.
        self.cleaner.links = False  # Do not remove links.
