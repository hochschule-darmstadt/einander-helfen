from data_extraction.Scraper import Scraper


class WeltwaertsScraper(Scraper):
    base_url = 'https://www.weltwaerts.de'
    debug = True

    #   Handles the soupified response of a detail page in the predefined way and returns it
    def parse(self, response, url):
        print(url)

        parsed_object = {
            'title': None,
            'link': None,
            'organization': None,
            'task': None,
            'location': None,
            'contact': None,
            'geo_location': {
                'lat': None,
                'lon': None,
            },
            'source': self.base_url,
            'image': None,
        }


        return parsed_object

    #   Adds all URLs of detail pages, found on the search pages, for the crawl function to scrape
    def add_urls(self):
        import time

        search_page_url = f'{self.base_url}/de/ep-ergebnis.html'
        next_page_url = search_page_url

        index = 1
        while next_page_url:

            response = self.soupify(next_page_url)

            detail_link_tags = [x.find('a') for x in response.find_all('h3', {'class': 'result__headline'})]

            if self.debug:
                print(f'Fetched {len(detail_link_tags)} URLs from {next_page_url} [{index}]')

            for link_tag in detail_link_tags:
                current_link = self.base_url + link_tag['href']
                if current_link in self.urls:
                    self.add_error({
                        'func': 'add_urls',
                        'body': {
                            'page_index': index,
                            'search_page': next_page_url,
                            'duplicate_link': current_link,
                            'duplicate_index': self.urls.index(current_link)
                        }
                    })
                else:
                    self.urls.append(current_link)

            next_page_url = response.find('li', {'class': 'next'}).find('a', {'class': 'next'})['href']
            if next_page_url:
                next_page_url = self.base_url + '/' + next_page_url

            index += 1
            if index > 2:
                break
            time.sleep(self.delay)
