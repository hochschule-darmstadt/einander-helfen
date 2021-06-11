import re

from data_extraction.Scraper import Scraper


class DKSBScraper(Scraper):
    """Scrapes the website dksb.de."""

    base_url = 'https://www.dksb.de'
    debug = True

    def parse(self, response, url):
        """Handles the soupified response of a detail page in the predefined way and returns it"""
        self.logger.debug("parse()")

        content = response.find('div', {'class': 'remodal-content'})
        title_h2 = content.find('h2', {'class': 'subHeadline'})

        title = 'Deutscher Kinderschutzbund ' + title_h2.text

        next_elem = title_h2.next_sibling
        loc = []
        zipcode = None
        contact = ''
        is_loc_part = True
        while next_elem is not None:
            if is_loc_part and re.match(r'<b>', str(next_elem)):
                is_loc_part = False
            if is_loc_part and not re.match(r'<.*?>', str(next_elem)):
                elem = str(next_elem).strip()
                if len(elem) > 0:
                    loc.append(elem)
                    if re.match(r'\d{5} ', elem):
                        zipcode = elem.split(' ')[0]

            if not is_loc_part:
                contact += str(next_elem)
            next_elem = next_elem.next_sibling

        parsed_object = {
            'title': title,
            'categories': ['Kinder', 'Jugend'],
            'location': ', '.join(loc),
            'task': """Der Deutsche Kinderschutzbund (DKSB) bietet Ihnen in seinen Orts- und Landesverbänden eine Vielzahl von Möglichkeiten, sich freiwillig zu engagieren.<br>
Wenn Ihre Stärken in der Arbeit mit Kindern oder Familien liegen, können Sie z.B. in der Hausaufgabenhilfe oder in Hilfsangeboten für Familien mitarbeiten. Möchten Sie sich in der Büroorganisation oder im Finanzbereich engagieren, sind Sie in der Vorstandsarbeit herzlich willkommen. Auch bei der fachpolitischen Lobbyarbeit für Kinder und Familien ist Ihr Engagement wichtig. Setzen Sie sich in Ihrer Gemeinde für den Kinderschutz ein.<br>
Wenn Sie ehrenamtlich beim DKSB mitarbeiten, lernen Sie gleichgesinnte Menschen kennen und können sich in der Arbeit mit Kindern und Familien weiterqualifizieren. Zudem bestimmen Sie die Verbandsarbeit aktiv mit.""",
            'target_group': None,
            'prerequisites': None,
            'language_skills': None,
            'timing': None,
            'effort': None,
            'opportunities': None,
            'organization': None,
            'contact': contact,
            'link': url or None,
            'source': 'https://www.dksb.de',
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
            'prerequisites': None,
            'language_skills': None,
            'timing': None,
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

        search_page_url = f'{self.base_url}/de/dksb-vor-ort/'

        response = self.soupify(search_page_url)
        detail_list_entries = response.find_all('div', {'class': 'list-dksbvorort-item'})

        self.logger.debug(f'Fetched {len(detail_list_entries)} URLs from {search_page_url} [1/1]')
        self.update_fetching_progress(1, 1)

        # Iterate links and add, if not already found
        for list_entry in detail_list_entries:
            current_link = self.base_url + '/template/php/dksbvorort/details.php?key=' + list_entry['name']
            if current_link in self.urls:
                self.logger.debug(f"func: add_urls, 'body:'page_index: 1,"
                                  f' search_page: {search_page_url}, '
                                  f'duplicate_index: {current_link}, '
                                  f'duplicate_index: {self.urls.index(current_link)}')

            else:
                self.urls.append(current_link)
