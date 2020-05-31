import json
import threading
import time

import requests
from bs4 import BeautifulSoup


class Scraper:
    base_url = 'http://example.com'
    debug = False

    def __init__(self):
        self.urls = []
        self.threads = []

        self.data = []
        self.error_urls = []

    def run(self):
        self.start = time.time()
        self.add_urls()

        for i, url in enumerate(self.urls):
            thread = threading.Thread(target=self.crawl, args=(url, i + 1))
            thread.start()
            self.threads.append(thread)

        for t in self.threads:
            t.join()

        if self.debug:
            # print(json.dumps(self.data, indent=4))
            # print(self.error_urls)
            print(
                f"Took {(time.time() - self.start):0.2f} seconds to crawl {len(self.urls)} pages from {self.base_url}")

    def crawl(self, url, index):

        print(f'Thread #{index} created')

        res = requests.get(url).text
        detail_page = BeautifulSoup(res, 'html.parser')
        self.data.append({'url': url, 'response': self.parse(detail_page, url)})

        print(f'Thread #{index} ended')

    @staticmethod
    def parse(response, url):
        print(url)
        return response.soup.get_text()

    def add_urls(self):
        pass

    def get_json_data(self):
        return json.dumps(self.data)

    def get_data(self):
        return self.data

    @staticmethod
    def soupify(url):
        search_result_page = requests.get(url).text
        search_result_page = BeautifulSoup(search_result_page, 'html.parser')
        return search_result_page
