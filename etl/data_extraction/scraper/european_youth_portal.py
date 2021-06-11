import re

from data_extraction.Scraper import Scraper


class EuropeanYouthPortalScraper(Scraper):
    """Scrapes the website https://europa.eu."""

    base_url = 'https://europa.eu'
    debug = True

    def parse(self, response, url):
        """Handles the soupified response of a detail page in the predefined way and returns it"""
        self.logger.debug("parse()")

        param_box = response.find('div', {'class': 'eyp-standard-block'})

        location_arrow = param_box.find('i', {'class': 'fa-location-arrow'})
        location = None
        country = None
        if location_arrow is not None:
            location = location_arrow.parent
            country = location.find('b').decode_contents().strip()
            location = location.text.strip()

        organization_link = param_box.find('a', {'class': 'link-default'})
        if organization_link is not None:
            organization_link = organization_link.decode_contents().strip()
            organization_link = re.sub(r'(https?://)?(www\.)?', '', organization_link)

        sidebar = response.find('div', {'class': 'region-sidebar-second'})
        categories_box = sidebar.find('div', {'class': 'box'})
        categories = []
        if categories_box is not None:
            categories = [x.text.strip() for x in categories_box.find_all('p')]

        description_box = param_box.parent.find('div', {'class': 'box'}).findNext('div', {'class': 'box'})

        parsed_object = {
            'title': param_box.find("h5").decode_contents().strip() or None,
            'categories': categories,
            'location': location or None,
            'task': description_box.p.decode_contents().strip() or None,
            'target_group': None,
            'prerequisites': None,
            'language_skills': None,
            'timing': None,
            'effort': None,
            'opportunities': None,
            'organization': organization_link or None,
            'contact': None,
            'link': url or None,
            'source': "europa.eu",
            'geo_location': None,
        }

        parsed_object['post_struct'] = {
            'title': parsed_object['title'],
            'categories': parsed_object['categories'],
            'location': {
                'country': country or None,
                'zipcode': None,
                'city': None,
                'street': None,
            },
            'task': parsed_object['task'],
            'target_group': parsed_object['target_group'],
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
            'contact': None,
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

        search_page_url = f'{self.base_url}/youth/volunteering/organisations_de?country=&topic=&scope%5Bql%5D=volunteering&town=&name=&combine=&inclusion_topic=&op=Apply+Filter'
        next_page_url = search_page_url

        index = 1
        while next_page_url:

            response = self.soupify(next_page_url)

            card_divs = response.find_all("div", {"class": "eyp-card block-is-flex box"})

            # Get <a> tags of individual results
            detail_page_a_tags = [x.find('a', href=re.compile('/youth/volunteering/organisation')) for x in card_divs]

            # Get maximum number of pages
            index_max = index
            last_page_link = response.find('li', {'class': 'pager-last'})
            if last_page_link is not None:
                last_page_link = last_page_link.a['href']
                index_max = re.match(r'.*page=([0-9]*)', last_page_link).group(1)
                index_max = int(index_max)+1

            self.logger.debug(f'Fetched {len(detail_page_a_tags)} URLs from {next_page_url} [{index}/{index_max}]')
            self.update_fetching_progress(index, index_max)

            # Iterate links and add, if not already found
            for link_tag in detail_page_a_tags:
                current_link = self.base_url + '/' + link_tag['href']
                if current_link in self.urls:
                    self.logger.debug(f"func: add_urls, 'body:'page_index: {index},"
                                      f" search_page: {search_page_url}, "
                                      f"duplicate_index: {current_link}, "
                                      f"duplicate_index: {self.urls.index(current_link)}")

                else:
                    self.urls.append(current_link)

            # Get next result page
            next_page_url = response.find('li', {'class': 'next'})
            if next_page_url:
                next_page_url = self.base_url + next_page_url.a['href']

            index += 1

            time.sleep(self.delay)
