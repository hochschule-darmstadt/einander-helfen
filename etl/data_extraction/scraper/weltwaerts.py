from data_extraction.Scraper import Scraper


class WeltwaertsScraper(Scraper):
    base_url = 'https://www.weltwaerts.de'
    debug = True

    #   Handles the soupified response of a detail page in the predefined way and returns it
    def parse(self, response, url):
        import re

        param_box = response.find('div', {'class': 'parameter__box'})

        content = response.find('div', {'class': 'mod_epdetail__content-container'})
        contact = content.find('h2', text='Ansprechpartner*in und Entsendeorganisation').findNext('div')

        google_map = response.find('a', {'class': 'mod_epdetail__link-map'})
        lat = None
        lon = None

        if google_map:
            try:
                result = re.findall(r'q=(-?\d+\.\d+),(-?\d+\.\d+)', google_map['href'])
                lat = float(result[0][0])
                lon = float(result[0][1])
            except (IndexError, TypeError, ValueError):
                pass

        parsed_object = {
            'title': param_box.find("h1").decode_contents().strip() or None,
            'categories': ['International'],
            'location': param_box.find('li').find('span', {'class': 'parameter__value'}).decode_contents().strip() or None,
            'task': content.find('h2', text='Deine Aufgabe').findNext('div').decode_contents().strip() or None,
            'timing': param_box.find('li').findNext('li').findNext('li').find('span', {'class': 'parameter__value'}).decode_contents().strip() or None,
            'organization': content.find('h2', text='Die Aufnahmeorganisation vor Ort').findNext('div').p.decode_contents().strip() or None,
            'contact': contact.decode_contents().strip() or None,
            'link': url or None,
            'source': self.base_url,
            'image': 'https://www.weltwaerts.de/files/framework/img/ww-logo-de.svg',
            'geo_location': {
                'lat': lat,
                'lon': lon,
            } if lat and lon else None,
            'languages': param_box.find('li').findNext('li').find('span', {'class': 'parameter__value'}).decode_contents().strip() or None,
            'requirements': content.find('h2', text='Anforderungen an dich').findNext('div').p.decode_contents().strip() or None,
        }

        contact_raw = re.sub(r'</?p>', '', parsed_object['contact'])
        contact_raw = re.sub(r'<br/?>', '\n', contact_raw)
        contact_raw = re.sub(r'<a.*</a>', '', contact_raw)
        contact_raw = contact_raw.replace('</br>', '')
        contact_raw = contact_raw.replace('\n\n', '\n').strip()
        contact_split = list(filter(None, contact_raw.split('\n')))

        if len(contact_split) > 3:
            names_split = contact_split[:(len(contact_split)-2)]
            names_raw = ', '.join(names_split)
            contact_split = [names_raw, contact_split[-2], contact_split[-1]]

        parsed_object['post_struct'] = {
            'title': parsed_object['title'],
            'categories': parsed_object['categories'],
            'location': {
                'country': parsed_object['location'].split(', ')[-1] or None,
            },
            'task': re.sub(r'</?p>', '', parsed_object['task']).strip(),
            'timing': parsed_object['timing'],
            'organization': {
                'name': parsed_object['organization'],
            },
            'contact': {
                'name':  contact_split[0].strip() or None,
                'zipcode': contact_split[2][:5].strip() or None,
                'city': contact_split[2][5:].strip() or None,
                'street':  contact_split[1].strip() or None,
                'email': contact.find('a', href=re.compile("mailto:.*"))['href'].replace('mailto:', '').strip() or None,
            },
            'link': parsed_object['link'],
            'source': parsed_object['link'],
            'image': parsed_object['link'],
            'geo_location': parsed_object['geo_location'],
            'languages': parsed_object['languages'],
            'requirements': parsed_object['requirements'],
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
                current_link = self.base_url + '/' + link_tag['href']
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

            time.sleep(self.delay)
