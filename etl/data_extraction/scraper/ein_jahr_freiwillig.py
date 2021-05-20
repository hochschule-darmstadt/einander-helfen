from data_extraction.Scraper import Scraper

import re
import math


class EinJahrFreiwillig(Scraper):
    """Scrapes the website ein-jahr-freiwillig.de."""

    base_url = 'https://ein-jahr-freiwillig.de'
    debug = True

    def parse(self, response, url):
        """Handles the soupified response of a detail page in the predefined way and returns it"""

        content = response.find('div', {'class': 'node__content'})

        location = content.find('p', {'class': 'address'})
        task = content.find('div', {
            'class': 'clearfix text-formatted field field--name-body '
                     'field--type-text-with-summary field--label-hidden field__item'})
        timing = content.find('div', {
            'class': 'field field--name-field-field-verfuegbar-ab field--type-string field--label-above'})
        effort = content.find('div', {
            'class': 'field field--name-field-laenge-dienstzeit field--type-string field--label-above'})
        organization = content.find('div', {
            'class': 'field field--name-field-traeger field--type-entity-reference field--label-above'})
        prerequisits = content.find('div', {
            'class': 'field field--name-field-voraussetzungen field--type-string-long field--label-above'})

        category_names = []
        categories = content.find('div', {
            'class': 'field field--name-field-einsatzfelder field--type-entity-reference '
                     'field--label-hidden field__items'})
        if categories is not None:
            categories = categories.find_all('a')
            for category in categories:
                category_names.append(category.decode_contents().strip())

        # Service types are added as an additional tag
        service_types = content.find('div', {
            'class': 'field field--name-field-dienstarten '
                     'field--type-entity-reference field--label-hidden field__items'})
        if service_types is not None:
            service_types = service_types.find_all('a')
            for service_type in service_types:
                category_names.append(service_type.decode_contents().strip())

        parsed_object = {
            'title': response.find('span', {
                'class': 'field field--name-title field--type-string field--label-hidden'}
                                   ).decode_contents().strip() or None,
            'categories': category_names,
            'location': location.decode_contents().strip() if location is not None else None,
            'task': task.decode_contents().strip() if task is not None else None,
            'target_group': None,
            'prerequisites': prerequisits.find('div', {
                'class': 'field__item'}).decode_contents().strip() if prerequisits is not None else None,
            'language_skills': None,
            'timing': timing.find('div',
                                  {'class': 'field__item'}).decode_contents().strip() if timing is not None else None,
            'effort': effort.find('div',
                                  {'class': 'field__item'}).decode_contents().strip() if effort is not None else None,
            'opportunities': None,
            'organization': organization.find("a").decode_contents().strip() if organization is not None else None,
            'contact': None,
            'link': url or None,
            'source': "www.ein-jahr-freiwillig.de",
            'geo_location': None,
        }

        contact_name = location.find('span', {'class': 'address-line1'})
        location_street = location.find('span', {'class': 'address-line2'})
        location_plz = location.find('span', {'class': 'postal-code'})
        location_ort = location.find('span', {'class': 'locality'})
        location_country = location.find('span', {'class': 'country'})

        phone = content.find('div', {
            'class': 'field field--name-field-einrichtung-telefon field--type-string field--label-above'})

        parsed_object['post_struct'] = {
            'title': self.clean_string(parsed_object['title']) or None,
            'categories': parsed_object['categories'] or None,
            'location': {
                'country': self.clean_string(
                    location_country.decode_contents()) if location_country is not None else None,
                'zipcode': self.clean_string(location_plz.decode_contents()) if location_plz is not None else None,
                'city': self.clean_string(location_ort.decode_contents()) if location_ort is not None else None,
                'street': self.clean_string(location_street.decode_contents()) if location_street is not None else None,
            },
            'task': self.clean_string(parsed_object['task']) or None,
            'target_group': None,
            'prerequisites': self.clean_string(parsed_object['prerequisites']),
            'language_skills': None,
            'timing': self.clean_string(parsed_object['timing']) or None,
            'effort': self.clean_string(parsed_object['effort']) or None,
            'opportunities': None,
            'organization': {
                'name': self.clean_string(parsed_object['organization']) or None,
                'zipcode': None,
                'city': None,
                'street': None,
                'phone': None,
                'email': None,
            },
            'contact': {
                'name': self.clean_string(contact_name.decode_contents()) if contact_name is not None else None,
                'zipcode': self.clean_string(location_plz.decode_contents()) if location_plz is not None else None,
                'city': self.clean_string(location_ort.decode_contents()) if location_ort is not None else None,
                'street': self.clean_string(location_street.decode_contents()) if location_street is not None else None,
                'phone': self.clean_string(
                    phone.find('div', {'class': 'field__item'}).decode_contents()) if phone is not None else None,
                'email': None,
            },
            'link': self.clean_string(parsed_object['link']) or None,
            'source': self.clean_string(parsed_object['source']) or None,
            'geo_location': None,
        }

        # Set category to international, if country is set to a value that is not 'Deutschland'
        if parsed_object['post_struct']['location']['country'] is not None \
                and parsed_object['post_struct']['location']['country'] != 'Deutschland':
            parsed_object['categories'].append('International')

        return parsed_object

    def add_urls(self):
        """Adds all URLs of detail pages, found on the search pages, for the crawl function to scrape"""
        self.logger.debug("add_urls()")
        import time

        search_page_url = f'{self.base_url}/de/suche/ort?geo%5Bvalue%5D=10&geo%5Bsource_configuration' \
                          f'%5D%5Borigin_address%5D=&last_minute=All&unterkunft=All&anbieter=&page=0'
        next_page_url = search_page_url

        index = 1
        while next_page_url:
            response = self.soupify(next_page_url)

            # Get tags of individual results
            detail_link_tags = [x.find('a') for x in response.find_all('div', {'class': 'field-link l-more'})]
            detail_link_tags = list(filter(lambda x: x['href'].startswith('/stellen/'), detail_link_tags))

            # Get maximum number of pages
            index_max = float(re.search('([0-9]+) Treffer', response.find('div', {
                'class': 'field-result-count'}).decode_contents().strip()).group(1))
            index_max = math.ceil(index_max / 20)

            self.logger.debug(f'Fetched {len(detail_link_tags)} URLs from {next_page_url} [{index}/{index_max}]')
            self.update_fetching_progress(index, index_max)

            # Iterate links and add, if not already found
            for link_tag in detail_link_tags:
                current_link = self.base_url + link_tag['href']
                if current_link in self.urls:
                    self.logger.debug(f"func: add_urls, 'body:'page_index: {index},"
                                      f" search_page: {search_page_url}, "
                                      f"duplicate_index: {current_link}, "
                                      f"duplicate_index: {self.urls.index(current_link)}")
                else:
                    self.urls.append(current_link)

            # Get next result page
            next_page_url = response.find('li', {'class': 'pager__item pager__item--next'})
            if next_page_url:
                next_page_url = self.base_url + '/de/suche/ort' + next_page_url.find('a')['href']

            index += 1

            time.sleep(self.delay)
