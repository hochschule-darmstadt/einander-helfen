import math
import re

from data_extraction.scraper import Scraper


class SozialeinsatzScraper(Scraper):
    """Scrapes the website www.sozialeinsatz.de."""

    base_url = 'https://www.sozialeinsatz.de'
    debug = True

    def parse(self, response, url):
        """Handles the soupified response of a detail page in the predefined way and returns it"""
        self.logger.debug('parse()')

        content = response.find('div', {'id': 'content'})

        title = content.find('h2')

        if title.text == 'Error 404':
            return None

        task = content.find('h2', string=re.compile(r'Stellenbeschreibung.*')).findNext('p')

        organization = title.findNext('div', {'class': 'row'}).find('p')

        contact = content.find('h2', string=re.compile(r'Ansprechpartner.*')).findNext('p')

        details = content.find('h2', string=re.compile(r'Details.*')).findNext('p')

        category_string = details.find('strong', string=re.compile(r'Aufgaben.*')).nextSibling
        categories = [x.strip() for x in category_string.split(',')]
        categories.append(title.find('acronym')['title'])

        timing = details.find('strong', string=re.compile(r'Zeitraum.*')).nextSibling

        location = None
        location_p = content.find('h2', string=re.compile(r'Einsatzort.*')).findNext('p')
        if location_p.a is not None and 'q=' in location_p.a['href']:
            location = location_p.a['href'].split('q=')[1]

        zipcode = None
        if location is not None:
            if len(re.findall(r'(\d{5})', location)) > 0:
                zipcode = re.findall(r'(\d{5})', location)[0]

        parsed_object = {
            'title': title.text.strip(),
            'categories': categories,
            'location': location,
            'task': task.decode_contents().strip(),
            'target_group': None,
            'prerequisites': None,
            'language_skills': None,
            'timing': timing.strip(),
            'effort': None,
            'opportunities': None,
            'organization': organization.decode_contents().strip() if organization is not None else None,
            'contact': contact.decode_contents().strip() if contact is not None else None,
            'link': url or None,
            'source': 'www.sozialeinsatz.de',
            'geo_location': None,
        }

        parsed_object['post_struct'] = {
            'title': parsed_object['title'],
            'categories': parsed_object['categories'],
            'location': {
                'country': 'Deutschland',
                'zipcode': zipcode,
                'city': None,
                'street': None,
            },
            'task': None,
            'target_group': None,
            'prerequisites': parsed_object['prerequisites'],
            'language_skills': parsed_object['language_skills'],
            'timing': parsed_object['timing'],
            'effort': None,
            'opportunities': None,
            'organization': None,
            'contact': None,
            'link': parsed_object['link'],
            'source': parsed_object['source'],
            'geo_location': parsed_object['geo_location'],
        }

        return parsed_object

    def add_urls(self):
        """Adds all URLs of detail pages, found on the search pages, for the crawl function to scrape"""
        self.logger.debug('add_urls()')

        import time

        index = 1
        index_max = None

        search_page_url = f'{self.base_url}/stellenangebote/finden?Stellenangebot_page={index}'
        next_page_url = search_page_url

        while next_page_url:

            response = self.soupify(next_page_url)

            # Get tags of individual results
            detail_a_tags = response.findAll('a', {'class': 'morelink'})

            # Get maximum number of pages
            if index_max is None:
                summary_text = response.find('div', {'class': 'summary'}).text
                entries = int(re.findall(r'(\d+).?$', summary_text)[0])
                index_max = math.ceil(entries / 25.0)

            self.logger.debug(f'Fetched {len(detail_a_tags)} URLs from {next_page_url} [{index}/{index_max}]')
            self.update_fetching_progress(index, index_max)

            # Iterate links and add, if not already found
            for link_tag in detail_a_tags:
                current_link = self.base_url + link_tag['href']
                if current_link in self.urls:
                    self.logger.debug(f'func: add_urls, page_index: {index},'
                                      f' search_page: {search_page_url}, '
                                      f'duplicate_index: {current_link}, '
                                      f'duplicate_index: {self.urls.index(current_link)}')

                else:
                    self.urls.append(current_link)

            # Get next result page
            if index < index_max:
                index += 1
                next_page_url = f'{self.base_url}/stellenangebote/finden?Stellenangebot_page={index}'
            else:
                next_page_url = None

            time.sleep(self.delay)
