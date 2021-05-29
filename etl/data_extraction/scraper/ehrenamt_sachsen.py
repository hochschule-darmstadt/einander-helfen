import re

from data_extraction.Scraper import Scraper


class EhrenamtSachsenScraper(Scraper):
    """Scrapes the website https://www.ehrenamt.sachsen.de."""

    base_url = 'https://www.ehrenamt.sachsen.de'
    debug = True

    def parse(self, response, url):
        """Handles the soupified response of a detail page in the predefined way and returns it"""
        self.logger.debug("parse()")

        content = response.find('div', {'id': 'main-content-wrapper'})
        title = content.find('h1', {'id': 'page-title'})

        contact_address = content.find('p', {'class': 'contact contact-visitor'})
        location = None
        if contact_address is not None:
            location = contact_address.find('span', {'class': 'contact-content'})
            location = re.sub(r'<br/?>', ', ', location.decode_contents().strip())

        task_box = content.find('div', {'class': 'row'}).find('div', {'class': 'block'})
        task = None
        if task_box is not None:
            task = task_box.p

        table = content.find('tbody')
        city = None
        if table.find('th', string='Ort'):
            city = table.find('th', string='Ort').parent.find('td')

        categories = []
        if table.find('th', string='Engagementbereich'):
            categories = table.find('th', string='Engagementbereich').parent.find('td')
            categories = categories.decode_contents().strip().split(', ')

        parsed_object = {
            'title': title.decode_contents().strip() or None,
            'categories': categories,
            'location': location if location is not None else None,
            'task': task.decode_contents().strip() if task is not None else None,
            'target_group': None,
            'prerequisites': None,
            'language_skills': None,
            'timing': None,
            'effort': None,
            'opportunities': None,
            'organization': None,
            'contact': None,
            'link': url,
            'source': "www.ehrenamt.sachsen.de",
            'geo_location': None,
        }

        contact_person = content.find('p', {'class': 'contact contact-title'})
        if contact_person is not None:
            contact_person = contact_person.find('span', {'class': 'contact-content'})

        contact_phone = content.find('p', {'class': 'contact contact-phone'})
        if contact_phone is not None:
            contact_phone = contact_phone.find('span', {'class': 'contact-content'})

        parsed_object['post_struct'] = {
            'title': parsed_object['title'],
            'categories': parsed_object['categories'],
            'location': {
                'country': 'Deutschland',
                'zipcode': None,
                'city': city.decode_contents().strip() if city is not None else None,
                'street': None,
            },
            'task': None,
            'target_group': None,
            'prerequisites': parsed_object['prerequisites'],
            'language_skills': parsed_object['language_skills'],
            'timing': parsed_object['timing'],
            'effort': None,
            'opportunities': None,
            'organization': {
                'name': parsed_object['organization'],
                'zipcode': None,
                'city': None,
                'street': None,
                'phone': None,
                'email': None,
            },
            'contact': {
                'name': contact_person.decode_contents().strip() if contact_person is not None else None,
                'zipcode': None,
                'city': None,
                'street': None,
                'phone': contact_phone.decode_contents().strip() if contact_phone is not None else None,
                'email': None,
            },
            'link': parsed_object['link'],
            'source': parsed_object['source'],
            'geo_location': parsed_object['geo_location'],
        }

        return parsed_object

    def add_urls(self):
        """Adds all URLs of detail pages, found on the search pages, for the crawl function to scrape"""
        self.logger.debug("add_urls()")

        import time

        index = 1
        index_max = None

        search_page_url = f'{self.base_url}/engagementboerse/suche?filter=projects&location=address&page={index}'
        next_page_url = search_page_url

        while next_page_url:

            response = self.soupify(next_page_url)

            # Get tags of individual results
            detail_a_tags = [x.a for x in response.find_all('h3', {'class': 'media-heading'})]

            # Get maximum number of pages
            if index_max is None:
                button_last = response.find('button', {'class': 'lnk-last'})
                if button_last is not None:
                    last_page_link = button_last.parent['href']
                    index_max = re.match(r'.*page=([0-9]*)', last_page_link).group(1)
                else:
                    index_max = index

            self.logger.debug(f'Fetched {len(detail_a_tags)} URLs from {next_page_url} [{index}/{index_max}]')
            self.update_fetching_progress(index, index_max)

            # Iterate links and add, if not already found
            for link_tag in detail_a_tags:
                current_link = self.base_url + link_tag['href']
                if current_link in self.urls:
                    self.logger.debug(f"func: add_urls, 'body:'page_index: {index},"
                                      f" search_page: {search_page_url}, "
                                      f"duplicate_index: {current_link}, "
                                      f"duplicate_index: {self.urls.index(current_link)}")

                else:
                    self.urls.append(current_link)

            # Get next result page
            if index < int(index_max):
                index += 1
                next_page_url = self.base_url + f'/engagementboerse/suche?filter=projects&location=address&page={index}'
            else:
                next_page_url = None

            time.sleep(self.delay)
