import math
import time

from bs4 import BeautifulSoup
from data_extraction.scraper import Scraper


class EhrenamtHessenScraper(Scraper):
    base_url = 'https://www.ehrenamtssuche-hessen.de'

    def parse(self, response, url):
        """Handles the soupified response of a detail page in the predefined way and returns it."""
        self.logger.debug('parse()')

        tab = response.find('a', {'href': '?param&searchTab=jobentries&entryTypeId=5&showEntryTypeFilterSelect=false'})
        tab_parent_div = tab.parent
        tab_classes = tab_parent_div['class']
        if 'active' not in tab_classes:
            self.logger.debug(f'\'{url}\' is not volunteering work')
            return None

        location_of = response.find('div', {'class': 'legendLeft'}, text='Ort Ihres Ehrenamts')
        location = None
        lat = 0
        lon = 0
        if location_of is not None and location_of.parent is not None:
            desc_right = location_of.parent.find('div', {'class': 'descriptionRight'})
            if desc_right is not None:
                location = desc_right.next
                geo_data = desc_right.find('li', {'class': 'geodata'})
                lat = geo_data.get('data-pos-lat') or 0
                lon = geo_data.get('data-pos-lon') or 0

        task_field = response.find('div', {'class': 'legendLeft'}, text='Ihr Aufgabenfeld')
        task = None
        if task_field is not None and task_field.parent is not None:
            desc_right = task_field.parent.find('div', {'class': 'descriptionRight'})
            if desc_right is not None:
                task_string = desc_right.decode_contents()
                if task_string:
                    task = task_string.strip()

        organization_field = response.find('div', {'class': 'legendLeft'}, text='Organisation/Anbieter')
        organization = None
        if organization_field is not None and organization_field.parent is not None:
            desc_right = organization_field.parent.find('div', {'class': 'descriptionRight'})
            if desc_right is not None:
                organization_string = desc_right.decode_contents()
                if organization_string:
                    organization = organization_string.strip()

        contact_field = response.find('div', {'class': 'legendLeft'}, text='Ihr Ansprechpartner')
        contact = None
        if contact_field is not None and contact_field.parent is not None:
            desc_right = contact_field.parent.find('div', {'class': 'descriptionRight'})
            if desc_right is not None:
                contact = desc_right.find('div').prettify()

        parsed_object = {
            'title': response.find('h3', {'class': 'ItemTitle'}).text or None,
            'categories': self._extract_categories(response),
            'location': location or None,
            'task': task or None,
            'target_group': None,
            'timing': None,
            'effort': None,
            'opportunities': None,
            'organization': organization or None,
            'contact': contact or None,
            'link': url or None,
            'source': 'www.ehrenamtssuche-hessen.de',
            'geo_location': {
                'lat': float(lat),
                'lon': float(lon),
            } if lat and lon else None,
        }

        city_string = self.clean_string(parsed_object['location'])
        city = None
        if city_string:
            city = city_string.strip()
        task_string = self.clean_html_tags(self.clean_string(parsed_object['task']))
        task = None
        if task_string:
            task = task_string.strip()

        parsed_object['post_struct'] = {
            'title': self.clean_string(parsed_object['title']) or None,
            'categories': parsed_object['categories'] or None,
            'location': {
                'country': 'Deutschland',
                'zipcode': None,
                'city': city or None,
                'street': None,
                'continent': 'Europa',
            },
            'task': task or None,
            'target_group': None,
            'timing': None,
            'effort': None,
            'opportunities': None,
            'organization': self._extract_sub_data(parsed_object['organization']),
            'contact': self._extract_sub_data(parsed_object['contact']),
            'link': parsed_object['link'] or None,
            'source': parsed_object['source'] or None,
            'geo_location': parsed_object['geo_location'],
            'map_address': None,
        }

        if parsed_object['organization'] is not None:
            organization = parsed_object['organization']
            organization = organization.replace('_self', '_blank')
            organization = organization.replace('/index.cfm', 'https://www.ehrenamtssuche-hessen.de/index.cfm')
            organization = self._fix_mail_to_links(organization)
            parsed_object['organization'] = organization

        if parsed_object['contact'] is not None:
            contact = parsed_object['contact']
            contact = self._fix_target_blank(contact)
            parsed_object['contact'] = contact

        if parsed_object['task'] is not None:
            task = parsed_object['task']
            task = self._fix_target_blank(task)
            parsed_object['task'] = task

        return parsed_object

    def add_urls(self):
        """Adds all URLs of detail pages, found on the search pages, for the crawl function to scrape."""
        self.logger.debug('add_urls()')

        end_page = self.fetch_end_page()

        for index in range(1, end_page + 1):

            time.sleep(self.delay)

            search_page_url = f'{self.base_url}/entry_search_result.cfm?locationId=0&entryTypeId=5&page={str(index)}'
            search_page = self.soupify(search_page_url)
            detail_links = [x.find('a') for x in search_page.find_all('div', {'class': 'easSearchResultTitle'})]

            self.logger.debug(f'Fetched {len(detail_links)} URLs from {search_page_url} [{index}/{end_page}]')
            self.update_fetching_progress(index, end_page)

            for detail_link in detail_links:
                current_link = self.base_url + detail_link['href']
                if current_link in self.urls:
                    self.logger.debug(f'func: add_urls, page_index: {index},'
                                      f' search_page: {search_page_url}, '
                                      f'duplicate_index: {current_link}, '
                                      f'duplicate_index: {self.urls.index(current_link)}')
                else:
                    self.urls.append(current_link)

    def fetch_end_page(self):
        """Domain-specific Function.
        Fetches the number of pages from the search result page for the add_urls function."""
        self.logger.debug('fetch_end_page()')

        search_page_url = f'{self.base_url}/entry_search_result.cfm?locationId=0&entryTypeId=5'
        search_page = self.soupify(search_page_url)
        total_entries_as_string = search_page.find('h2', {'class': 'easSearchHeading'}).next.strip()
        formatted_entry_number = int(total_entries_as_string.replace('.', ''))
        end_page = math.ceil(formatted_entry_number / 15)

        self.logger.debug(f'Crawling {end_page} pages with 15 entries each.')

        return end_page

    def _extract_categories(self, response):
        """Extracts the categories from corresponding field."""
        self.logger.debug('_extract_categories()')

        cat_list = []
        categories_html = response.find('div', {'class': 'legendLeft'}, text='Kategorien')
        if categories_html is None or categories_html.parent is None:
            return []
        desc_right = categories_html.parent.find('div', {'class': 'descriptionRight'})
        if desc_right is None:
            return []
        eas = desc_right.find('div', {'class': 'easCategories'})
        if eas is None:
            return []
        for cat in eas.find_all('div', {'class': 'catIcon'}):
            cat_list.append(cat.get('title'))

        return cat_list

    def _extract_sub_data(self, value):
        """Extracts name, street, zipcode, city, phone and email from a given string."""
        self.logger.debug('_extract_sub_data()')

        if value is None:
            return {
                'name': None,
                'street': None,
                'zipcode': None,
                'city': None,
                'phone': None,
                'email': None,
            }

        clean = self.clean_string(value)
        html = BeautifulSoup(clean, 'html.parser')
        clean_list = clean.split('<br/>')
        name = None
        street = None
        zipcode = None
        city = None
        phone = None
        email = None

        # name
        if sum(i.isdigit() for i in clean_list[0]) == 0:
            name_string = self.clean_html_tags(clean_list[0])
            if name_string:
                name = name_string.strip()
        # street
        for item in clean_list:
            digits = sum(i.isdigit() for i in item)
            if digits > 0 and digits != 5:
                street_string = self.clean_html_tags(item)
                if street_string:
                    street = street_string.strip()
                    break
        # plz & city
        for item in clean_list:
            digits = sum(i.isdigit() for i in item)
            if digits == 5:
                zipcode_city_string = self.clean_html_tags(item)
                if zipcode_city_string:
                    zipcode_city = zipcode_city_string.strip().split(' ')
                    zipcode = zipcode_city[0]
                    city = zipcode_city[1]
                    break
        # phone
        phone_html = html.find('i', {'class': 'fa-phone'}) or None
        if phone_html is not None:
            phone_string = phone_html.next.next
            if phone_string:
                phone = phone_string.strip()
        # email
        emails = html.select('a[href^=mailto]')

        if emails is not None:
            if len(emails) > 0:
                email_string = emails[0].text
                if email_string:
                    email = email_string.strip()

        return {
            'name': name or None,
            'street': street or None,
            'zipcode': zipcode or None,
            'city': city or None,
            'phone': phone or None,
            'email': email or None,
        }

    def _fix_mail_to_links(self, data):
        """ implements ehrenamtsuche specific fixes for mailto links in organisation field """
        self.logger.debug('_fix_mail_to_links()')

        soup = BeautifulSoup(data, 'html.parser')
        links = soup.findAll('a')
        for link in links:
            if 'mailto' not in link.decode():
                link['rel'] = 'noopener'
        data = soup.decode()
        return data

    def _fix_target_blank(self, data):
        """ implements ehrenamtsuche specific fixes for mailto links in task and contact field """
        self.logger.debug('_fix_target_blank()')

        soup = BeautifulSoup(data, 'html.parser')
        links = soup.findAll('a')
        for link in links:
            if 'mailto' not in link.decode():
                link['target'] = '_blank'
                link['rel'] = 'noopener'
        data = soup.decode()
        return data
