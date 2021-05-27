import re

from data_extraction.Scraper import Scraper


class BetterplaceScraper(Scraper):
    """Scrapes the website https://www.betterplace.org."""

    base_url = 'https://www.betterplace.org'
    debug = True

    def parse(self, response, url):
        """Handles the soupified response of a detail page in the predefined way and returns it"""
        self.logger.debug("parse()")

        title = response.find('div', {'class': 'job-description-content-header'}).h1.text.strip() \
            if response.find('div', {'class': 'job-description-content-header'}) is not None \
            else None

        content = response.find('div', {'class': 'job-descriptions-show'})
        description_div = content.find('div', {'class': 'description'})
        tag_box = content.find('ul', {'class': 'generic-tags'})
        tag_list = [x.text.strip() for x in tag_box.find_all('li')]
        contact_div = content.find('div', {'class': 'contact-person'}).find('div', {'class': 'copytext'}) \
            if content.find('div', {'class': 'contact-person'}) is not None \
            else None

        contact_text = None
        if contact_div:
            a_list = [x.text.strip() for x in contact_div.find_all('a')]
            if len(a_list) > 0:
                contact_text = '<br>'.join(a_list)

        location_spans = content.find("h4", string=re.compile(r'Wo du hilfst.*')).parent.find_all('span')

        lat = None
        lon = None
        if len(location_spans) > 0 and location_spans[-1].find('a'):
            href = location_spans[-1].find('a')['href']
            location_spans = location_spans[:-1]

            coords = re.search(r'(-?\d*\.\d{3,5}),(-?\d*\.\d{3,5})', href)
            if coords:
                lat = float(coords.group(1))
                lon = float(coords.group(2))

        location = ', '.join([x.text.strip() for x in location_spans])

        parsed_object = {
            'title': title,
            'categories': tag_list,
            'location': location,
            'task': description_div.decode_contents().strip() if description_div else None,
            'target_group': None,
            'prerequisites': None,
            'language_skills': None,
            'timing': None,
            'effort': None,
            'opportunities': None,
            'organization': None,
            'contact': contact_text,
            'link': url or None,
            'source': "betterplace.org",
            'geo_location':  {
                'lat': lat,
                'lon': lon,
            } if lat and lon else None,  # If longitude and latitude are None, geo_location is set to None
        }

        parsed_object['post_struct'] = {
            'title': parsed_object['title'],
            'categories': parsed_object['categories'],
            'location': {
                'country': location.split(', ')[-1] if location else None,
                'zipcode': None,
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
            'organization': {
                'name': parsed_object['organization'],
                'zipcode': None,
                'city': None,
                'street': None,
                'phone': None,
                'email': None,
            },
            'contact': parsed_object['contact'],
            'link': parsed_object['link'],
            'source': parsed_object['source'],
            'geo_location': parsed_object['geo_location'],
        }

        # Set category to international, if country is set to a value that is not 'Deutschland' or 'Germany'
        if parsed_object['post_struct']['location']['country'] is not None \
                and parsed_object['post_struct']['location']['country'] != 'Deutschland' \
                and parsed_object['post_struct']['location']['country'] != 'Germany':
            parsed_object['categories'].append('International')

        return parsed_object

    def add_urls(self):
        """Adds all URLs of detail pages, found on the search pages, for the crawl function to scrape"""
        self.logger.debug("add_urls()")

        import time

        search_page_url = f'{self.base_url}/de/discover-volunteering'
        next_page_url = search_page_url

        index = 1
        while next_page_url:

            response = self.soupify(next_page_url)

            # Get tags of individual results
            detail_a_tags = response.find_all('a', {'class': 'generic-searches-result'})

            self.logger.debug(f'Fetched {len(detail_a_tags)} URLs from {next_page_url} [{index}/unknown]')

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
            next_page_url = response.find('a', {'class': 'next_page'})
            if next_page_url:
                next_page_url = self.base_url + '/' + next_page_url['href']

            index += 1

            time.sleep(self.delay)

        self.set_progress_completed(index, 'FETCH')
