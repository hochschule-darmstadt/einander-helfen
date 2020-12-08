from data_extraction.Scraper import Scraper


class Ein_Jahr_Freiwillig(Scraper):
    """Scrapes the website ein-jahr-freiwillig.de."""

    base_url = 'https://ein-jahr-freiwillig.de'
    debug = True

    def parse(self, response, url):
        """Handles the soupified response of a detail page in the predefined way and returns it"""

        parsed_object = {
            'title': response.find('span', {'class': 'field field--name-title field--type-string field--label-hidden'}).decode_contents().strip() or None,
            'location': response.find('p', {'class': 'address'}).decode_contents().strip() or None,
            'task': response.find('div', {'class' :'clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item'}).p[2].decode_contents().strip() or None,
            'target_group': None,
            'timing': response.find('div', {'class': 'field field--name-field-field-verfuegbar-ab field--type-string field--label-above'}).find('div', {'class': 'field__item'}).decode_contents().strip() or None,
            'effort': response.find('div', {'class': 'field field--name-field-laenge-dienstzeit field--type-string field--label-above'}).find('div', {'class': 'field__item'}).decode_contents().strip() or None,
            'opportunities': None,
            'organization': response.find('div', {'class': 'field field--name-field-traeger field--type-entity-reference field--label-above'}).find('div')[2].decode_contents().strip() or None,
            'contact': None,
            'link': url or None,
            'source': self.base_url,
            'geo_location':  None,
            'requirements': response.find('div', {'class': 'field field--name-field-voraussetzungen field--type-string-long field--label-above'}).find('div', {'class': 'field__item'}).decode_contents().strip() or None,
        }

        location_street = response.find('span', {'class': 'address-line2'}).decode_contents().strip() or None
        #contact_name = profil.find('span', {'class': 'address-line1'}).decode_contents().strip() or None
        location_plz = response.find('span', {'class': 'postal-code'}).decode_contents().strip() or None
        location_ort = response.find('span', {'class': 'locality'}).decode_contents().strip() or None
        location_country = response.find('span', {'class': 'country'}).decode_contents().strip() or None

        parsed_object['post_struct'] = {
            'title': self.clean_string(parsed_object['title']) or None,
            'categories': self.clean_string(parsed_object['categories']) or None,
            'location': {
                'country': self.clean_string(location_country) or None,
                'zipcode': self.clean_string(location_plz) or None,
                'city': self.clean_string(location_ort) or None,
                'street': self.clean_string(location_street) or None,
            },
            'task': self.clean_string(parsed_object['task']) or None,
            'target_group': None,
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
            'contact': None,
            'link': self.clean_string(parsed_object['link']) or None,
            'source': self.clean_string(parsed_object['source']) or None,
            'geo_location': None,
            'requirements': self.clean_string(parsed_object['requirements']) or None,
        }


        return parsed_object

    def add_urls(self):
        """Adds all URLs of detail pages, found on the search pages, for the crawl function to scrape"""

        import time

        search_page_url = f'{self.base_url}/de/suche/ort?geo%5Bvalue%5D=10&geo%5Bsource_configuration%5D%5Borigin_address%5D=&last_minute=All&unterkunft=All&anbieter=&page=0'
        next_page_url = search_page_url

        index = 1
        while next_page_url:

            response = self.soupify_post(next_page_url, {
                'ep-sortfilter': 1,
                'ep-numperpage': 50,
                'ep-sortorder': 'alpha'
            })

            # Get tags of individual results
            detail_link_tags = [x.find('a') for x in response.find_all('div', {'class': 'field field--name-title field--type-string field--label-hidden'})]

            # Get maximum number of pages
            index_max = 9 #response.find('div', {'class': 'pager__item'}).findNext('a').decode_contents().strip()

            if self.debug:
                print(f'Fetched {len(detail_link_tags)} URLs from {next_page_url} [{index}/{index_max}]')

            # Iterate links and add, if not already found
            for link_tag in detail_link_tags:
                current_link = self.base_url + link_tag['href']
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
            next_page_url = response.find('li', {'class': 'pager__item pager__item--next'}).find('a')
            if next_page_url:
                next_page_url = self.base_url + '/de/suche/ort' + next_page_url['href']

            index += 1

            if index > 2:
                break
            time.sleep(self.delay)
