from data_extraction.Scraper import Scraper


class BundesFreiwilligendienst(Scraper):
    """Scrapes the website bundesfreiwilligendienst.de."""

    base_url = "https://www.bundesfreiwilligendienst.de"

    def parse(self, response, url):
        """Handles the soupified response of a detail page in the predefined way and returns it."""
        self.logger.debug("parse()")
        content = response.find('div', {'class': 'single_view_entry clearfix'})

        title = content.find('h1')
        categories_tag = content.find('section', {'class': 'einsatzbereich'})

        categories = []
        if categories_tag is not None:
            for cat_entry_lst in categories_tag.find('div', {'class': 'span9'}).find_all('li'):
                for cat_entry in cat_entry_lst.decode_contents().split(','):
                    categories.append(cat_entry.strip())

        location = content.find('div', {'class': 'span5'}).find_all('div', {'class': 'box white-bg'})[0]
        task = content.find('div', {'class': 'description'})
        contact = content.find('div', {'class': 'span5'}).find_all('div', {'class': 'box white-bg'})[1].find('div', {'class': 'box-content'})

        lat = None
        lon = None

        try:
            lat = float(response.find('span', {'class': 'coordLat'}).decode_contents().strip()) if response.find('span', {'class': 'coordLat'}) else None
            lon = float(response.find('span', {'class': 'coordLong'}).decode_contents().strip()) if response.find('span', {'class': 'coordLong'}) else None
        except (TypeError, ValueError):
            pass

        parsed_object = {
            'title': title.decode_contents().strip() if title is not None else None,
            'categories':  categories,
            'location': location.decode_contents().strip() if location is not None else None,
            'task': task.decode_contents().strip() if task is not None else None,
            'target_group': None,
            'prerequisites': None,
            'language_skills': None,
            'timing': None,
            'effort': None,
            'opportunities': None,
            'organization': None,
            'contact': contact.decode_contents().strip() if contact is not None else None,
            'link': url or None,
            'source': 'www.bundesfreiwilligendienst.de',
            'geo_location':  {
                'lat': lat,
                'lon': lon,
            } if lat and lon else None, # If longitude and latitude are None, geo_location is set to None,
        }

        location_street = None
        location_zipcode = None
        location_city = None

        for location_entry in location.find_all('div', {'class': 'span12'}):
            object_name = location_entry.find('strong').decode_contents().strip()
            if 'Straße' in object_name:
                location_street = location_entry.find('div', {'class': 'span10'})
            if 'PLZ' in object_name:
                location_zipcode = location_entry.find('span', {'class': 'span10'})
            if 'Ort' in object_name:
                location_city = location_entry.find('span', {'class': 'span10'})

        contact_name = None
        contact_phone = None
        contact_email = None

        for contact_entry in contact.find_all('div', {'class': 'span12'}):
            object_name = contact_entry.find('strong').decode_contents().strip()
            if 'Name' in object_name:
                contact_name = contact_entry.find('div', {'class': 'span10'})
                # Due to the contact name containing lots of spaces, they are being removed using split and join
                contact_name = ' '.join(contact_name.decode_contents().strip().split()) if contact_name is not None else None
            if 'Telefon' in object_name:
                contact_phone = contact_entry.find('span', {'class': 'span10'})
            if 'Mail' in object_name:
                contact_email = contact_entry.find('span', {'class': 'span10'}).find('a')

        parsed_object['post_struct'] = {
            'title': self.clean_string(parsed_object['title']) or None,
            'categories': parsed_object['categories'],
            'location': {
                'country': None,
                'zipcode': self.clean_string(location_zipcode.decode_contents()) if location_zipcode is not None else None,
                'city': self.clean_string(location_city.decode_contents()) if location_city is not None else None,
                'street': self.clean_string(location_street.decode_contents()) if location_street is not None else None,
            },
            'task': self.clean_string(self.clean_html_tags(parsed_object['task'])) or None,
            'target_group': None,
            'prerequisites': None,
            'language_skills': None,
            'timing': None,
            'effort': None,
            'opportunities': None,
            'organization': {
                'name':  None,
                'zipcode': None,
                'city': None,
                'street': None,
                'phone': None,
                'email': None,
            },
            'contact': {
                'name': self.clean_string(contact_name) if len(contact_name) > 0 else None,
                'zipcode': None,
                'city': None,
                'street': None,
                'phone': self.clean_string(contact_phone.decode_contents().strip()) if contact_phone is not None else None,
                'email': self.clean_string(contact_email.decode_contents().strip().replace('[at]', '@')) if contact_email is not None else None,
            },
            'link': self.clean_string(parsed_object['link']) or None,
            'source': self.clean_string(parsed_object['source']) or None,
            'geo_location': parsed_object['geo_location'],
            'map_address': None,
        }

        return parsed_object

    def add_urls(self):
        """Adds all URLs of detail pages, found on the search pages, for the crawl function to scrape."""
        self.logger.debug("add_urls()")

        import time

        search_page_url = f'{self.base_url}/bundesfreiwilligendienst/platz-einsatzstellensuche/einsatzstelle-suchen.html?tx_bfdeinsatzstellensuche_einsatzstellensuche%5Baction%5D=filter&tx_bfdeinsatzstellensuche_einsatzstellensuche%5Bcontroller%5D=Suchen%5CEinsatzstellensuche&cHash=e5b52d4a17e46f7278157d2c526cecc5'
        next_page_url = search_page_url

        index = 1
        index_max = -1
        session = None

        while next_page_url:
            response, session = self.soupify_post_session(next_page_url, {
                'tx_bfdeinsatzstellensuche_einsatzstellensuche[ergebnisseProSeite]': 100
            }, session)

            detail_link_tags = [x.find('a') for x in response.find_all('td', {'class': 'row5'})]

            pagination = response.find('ul', {'class': 'pagination'})
            next_page_tag = pagination.find('i', {'class': 'fa fa-chevron-right'})

            # Get maximum number of pages
            if index_max == -1 and next_page_tag is not None:
                index_max = next_page_tag.parent.parent.find_previous_sibling('li').a.decode_contents().strip()

            self.logger.debug(f'Fetched {len(detail_link_tags)} URLs from {self.base_url} [{index}/{index_max}]')

            # Iterate links and add, if not already found
            for link_tag in detail_link_tags:
                current_link = self.base_url + "/" + link_tag['href']
                if current_link in self.urls:
                    self.logger.debug(f"func: add_urls, 'body:'page_index: {index},"
                                      f" search_page: {search_page_url}, "
                                      f"duplicate_index: {current_link}, "
                                      f"duplicate_index: {self.urls.index(current_link)}")
                else:
                    self.urls.append(current_link)

            # Get next result page
            next_page_url = next_page_tag

            if next_page_url:
                next_page_url = self.base_url + '/' + next_page_url.parent['href']

            index += 1

            time.sleep(self.delay)
