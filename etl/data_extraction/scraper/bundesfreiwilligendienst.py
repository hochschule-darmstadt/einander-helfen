from data_extraction.Scraper import Scraper


class BundesFreiwilligendienst(Scraper):

    base_url = "https://www.bundesfreiwilligendienst.de"
    debug = True

    def parse(self, response, url):
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
            'timing': None,
            'effort': None,
            'opportunities': None,
            'organization': None,
            'contact': contact.decode_contents().strip() if contact is not None else None,
            'link': url or None,
            'source': self.base_url,
            'geo_location':  {
                'lat': lat,
                'lon': lon,
            } if lat and lon else None, # If longitude and latitude are None, geo_location is set to None,
            'languages': None,
            'requirements': None,

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
            if 'Telefon' in object_name:
                contact_phone = contact_entry.find('span', {'class': 'span10'})
            if 'Mail' in object_name:
                contact_email = contact_entry.find('span', {'class': 'span10'}).find('a')

        parsed_object['post_struct'] = {
            'title': self.clean_string(parsed_object['title']) or None,
            'categories': parsed_object['categories'] or None,
            'location': {
                'country': None,
                'zipcode': self.clean_string(location_zipcode.decode_contents()) if location_zipcode is not None else None,
                'city': self.clean_string(location_city.decode_contents()) if location_city is not None else None,
                'street': self.clean_string(location_street.decode_contents()) if location_street is not None else None,
            },
            'task': self.clean_string(parsed_object['task']) or None,
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
                'name': self.clean_string(contact_name.decode_contents().strip()) if contact_name is not None else None,
                'zipcode': None,
                'city': None,
                'street': None,
                'phone': self.clean_string(contact_phone.decode_contents().strip()) if contact_phone is not None else None,
                'email': self.clean_string(contact_email.decode_contents().strip()) if contact_email is not None else None,
            },
            'link': self.clean_string(parsed_object['link']) or None,
            'source': self.clean_string(parsed_object['source']) or None,
            'geo_location': None,
        }

        return parsed_object

    def add_urls(self):

        import time

        search_page_url = f'{self.base_url}/bundesfreiwilligendienst/platz-einsatzstellensuche/einsatzstelle-suchen.html?tx_bfdeinsatzstellensuche_einsatzstellensuche%5Bseite%5D=1&tx_bfdeinsatzstellensuche_einsatzstellensuche%5Baction%5D=blaettern&tx_bfdeinsatzstellensuche_einsatzstellensuche%5Bcontroller%5D=Suchen%5CEinsatzstellensuche&cHash=094683ada8eb8c80aab0c200e3aa89f1'
        next_page_url = search_page_url

        index = 1
        index_max = -1

        while next_page_url:
            response = self.soupify(next_page_url)

            detail_link_tags = [x.find('a') for x in response.find_all('td', {'class': 'row5'})]

            pagination = response.find('ul', {'class': 'pagination'})
            next_page_tag = pagination.find('i', {'class': 'fa fa-chevron-right'})

            # Get maximum number of pages
            if index_max == -1 and next_page_tag is not None:
                index_max = next_page_tag.parent.parent.find_previous_sibling('li').a.decode_contents().strip()

            if self.debug:
                print(f'Fetched {len(detail_link_tags)} URLs from {self.base_url} [{index}/{index_max}]')

            # Iterate links and add, if not already found
            for link_tag in detail_link_tags:
                current_link = self.base_url + "/" + link_tag['href']
                if current_link in self.urls:
                    self.add_error({
                        'func': 'add_urls',
                        'body': {
                            'page_index': index,
                            'search_page': next_page_url,
                            'duplicate_link': current_link,
                            'duplicate_index': self.urls.index(current_link),
                        }
                    })
                else:
                    self.urls.append(current_link)

            # Get next result page
            next_page_url = next_page_tag

            if next_page_url:
                next_page_url = self.base_url + '/' + next_page_url.parent['href']

            index += 1

            time.sleep(self.delay)
