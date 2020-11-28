import math
import time

from data_extraction.Scraper import Scraper


class EhrenamtHessenScraper(Scraper):
    base_url = 'https://www.ehrenamtssuche-hessen.de'
    debug = True

    def parse(self, response, url):
        """Handles the soupified response of a detail page in the predefined way and returns it."""

        parsed_object = {
            'title': response.find('h3', {'class': 'ItemTitle'}).text or None,
            'location': response.find('div', {'class': 'legendLeft'}, text='Ort Ihres Ehrenamts').parent.find('div', {
                'class': 'descriptionRight'}).next or None,
            'task': response.find('div', {'class': 'legendLeft'}, text='Ihr Aufgabenfeld').parent.find('div', {
                'class': 'descriptionRight'}).decode_contents().strip() or None,
            'target_group': None,
            'timing': None,
            'effort': None,
            'opportunities': None,
            'organization': response.find('div', {'class': 'legendLeft'}, text='Organisation/Anbieter').parent.find(
                'div', {'class': 'descriptionRight'}).decode_contents().strip() or None,
            'contact': response.find('div', {'class': 'legendLeft'}, text='Ihr Ansprechpartner').parent.find('div', {
                'class': 'descriptionRight'}).find('div').prettify() or None,
            'link': url or None,
            'source': 'www.ehrenamtssuche-hessen.de',
            'image': f'{self.base_url}/resources/img/hessenlogo_h180.png',
            'geo_location': {
                'lat': float(
                    response.find('div', {'class': 'legendLeft'}, text='Ort Ihres Ehrenamts').parent.find('div', {
                        'class': 'descriptionRight'}).find('li', {'class': 'geodata'}).get(
                        'data-pos-lat') or 0) or None,
                'lon': float(
                    response.find('div', {'class': 'legendLeft'}, text='Ort Ihres Ehrenamts').parent.find('div', {
                        'class': 'descriptionRight'}).find('li', {'class': 'geodata'}).get(
                        'data-pos-lon') or 0) or None,
            },
        }
        cat_object = []
        for cat in response.find('div', {'class': 'legendLeft'}, text='Kategorien').parent.find('div', {
            'class': 'descriptionRight'}).find('div', {'class': 'easCategories'}).find_all('div', {'class': 'catIcon'}):
            cat_object.append(cat.get('title'))

        parsed_object['categories'] = cat_object

        parsed_object['post_struct'] = {
            'title': self.clean_string(parsed_object['title']) or None,
            'categories': parsed_object['categories'] or None,
            'location': {
                'zipcode': None,
                'city': self.clean_string(parsed_object['location']) or None,
                'street': None,
            },
            'task': self.clean_string(parsed_object['task']) or None,
            'target_group': None,
            'timing': None,
            'effort': None,
            'opportunities': None,
            'organization': {
                'name': self.clean_string(parsed_object['todo']) or None,  # todo
                'zipcode': None,
                'city': None,
                'street': None,
                'phone': None,
                'email': None,
            },
            'contact': {
                'name': self.clean_string('todo') or None,  # todo
                'zipcode': None,
                'city': None,
                'street': None,
                'phone': self.clean_string('todo') or None,  # todo
                'email': self.clean_string('todo') or None,  # todo
            },
            'link': parsed_object['link'] or None,
            'source': parsed_object['source'] or None,
            'image': parsed_object['image'] or None,
            'geo_location': parsed_object['geo_location'],
            'map_address': None,
        }

        return parsed_object

    def add_urls(self):
        """Adds all URLs of detail pages, found on the search pages, for the crawl function to scrape."""

        end_page = self.fetch_end_page()

        for index in range(1, end_page + 1):

            time.sleep(self.delay)
            
            search_page_url = f'{self.base_url}/entry_search_result.cfm?locationId=0&entryTypeId=5&page={str(index)}'
            search_page = self.soupify(search_page_url)
            detail_links = [x.find('a') for x in search_page.find_all('div', {'class': 'easSearchResultTitle'})]

            if self.debug:
                print(f'Fetched {len(detail_links)} URLs from {search_page_url} [{index}/{end_page}]')

            for detail_link in detail_links:
                current_link = self.base_url + detail_link['href']
                if current_link in self.urls:
                    self.add_error({
                        'func': 'add_urls', 
                        'body': {
                            'page_index': index, 
                            'search_page': search_page_url,
                            'duplicate_link': current_link, 
                            'duplicate_index': self.urls.index(current_link)
                        }
                    })
                else:
                    self.urls.append(current_link)

    def fetch_end_page(self):
        """Domain-specific Function.
        Fetches the number of pages from the search result page for the add_urls function."""

        search_page_url = f'{self.base_url}/entry_search_result.cfm?locationId=0&entryTypeId=5'
        search_page = self.soupify(search_page_url)
        total_entries_as_string = search_page.find('h2', {'class': 'easSearchHeading'}).next.strip()
        formatted_entry_number = int(total_entries_as_string.replace('.', ''))
        end_page = math.ceil(formatted_entry_number / 15)

        if self.debug:
            print(f'Crawling {end_page} pages with 15 entries each.')

        return end_page
