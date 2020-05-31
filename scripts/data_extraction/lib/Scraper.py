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
        self.addUrls()

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
        detailPage = BeautifulSoup(res, 'html.parser')
        self.data.append({'url': url, 'response': self.parse(detailPage, url)})

        print(f'Thread #{index} ended')

    def parse(self, response, url):
        print(url)
        return response.soup.get_text()

    def addUrls(self):
        pass

    def getJSONData(self):
        return json.dumps(self.data)

    def getData(self):
        return self.data

    def soupify(self, url):
        searchResultPage = requests.get(url).text
        searchResultPage = BeautifulSoup(searchResultPage, 'html.parser')
        return searchResultPage
