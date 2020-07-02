from data_extraction.Scraper import Scraper


class EhrenamtHessenScraper(Scraper):
    base_url = 'https://www.ehrenamtssuche-hessen.de'
    debug = True

    #   Handles the soupified response of a detail page in the predefined way and returns it
    def parse(self, response, url):

        parsed_object = {
            'title': response.find('h3', {'class': 'ItemTitle'}).text or None,
            'link': url or None,
            'organization': response.find('div', {'class': 'legendLeft'}, text='Organisation/Anbieter').parent.find(
                'div', {'class': 'descriptionRight'}).decode_contents().strip() or None,
            'task': response.find('div', {'class': 'legendLeft'}, text='Ihr Aufgabenfeld').parent.find('div', {
                'class': 'descriptionRight'}).text or None,
            'location': response.find('div', {'class': 'legendLeft'}, text='Ort Ihres Ehrenamts').parent.find('div', {
                'class': 'descriptionRight'}).next or None,
            'contact': response.find('div', {'class': 'legendLeft'}, text='Ihr Ansprechpartner').parent.find('div', {
                'class': 'descriptionRight'}).find('div').prettify() or None,
            'geo_location': {
                'lat': float(
                    response.find('div', {'class': 'legendLeft'}, text='Ort Ihres Ehrenamts').parent.find('div', {
                        'class': 'descriptionRight'}).find('li', {'class': 'geodata'}).get(
                        'data-pos-lat') or 0) or None,
                'lon': float(
                    response.find('div', {'class': 'legendLeft'}, text='Ort Ihres Ehrenamts').parent.find('div', {
                        'class': 'descriptionRight'}).find('li', {'class': 'geodata'}).get(
                        'data-pos-lon') or 0) or None,
            },
            'source': 'www.ehrenamtssuche-hessen.de',
            'image': f'{self.base_url}/resources/img/hessenlogo_h180.png',
        }
        cat_object = []
        for cat in response.find('div', {'class': 'legendLeft'}, text='Kategorien').parent.find('div', {
            'class': 'descriptionRight'}).find('div', {'class': 'easCategories'}).find_all('div', {'class': 'catIcon'}):
            cat_object.append(cat.get('title'))

        parsed_object['categories'] = cat_object

        return parsed_object

    #   Adds all URLs of detail pages, found on the search pages, for the crawl function to scrape
    def add_urls(self):

        import time

        end_page = self.fetch_end_page()

        for index in range(1, end_page + 1):

            time.sleep(self.delay)

            search_page_url = f'{self.base_url}/entry_search_result.cfm?locationId=0&entryTypeId=5&page={str(index)}'
            search_page = self.soupify(search_page_url)
            detail_links = [x.find('a') for x in search_page.find_all('div', {'class': 'easSearchResultTitle'})]

            for detailLink in detail_links:
                if self.base_url + detailLink['href'] in self.urls:
                    self.add_error({'func': 'add_urls', 'body': {'index': index, 'search_page': search_page_url, 'duplicate_link': self.base_url + detailLink['href']}})
                else:
                    self.urls.append(self.base_url + detailLink['href'])

    # Domain-specific Function
    # Fetches the number of pages from the search result page for the add_urls function
    def fetch_end_page(self):

        import math

        search_page_url = f'{self.base_url}/entry_search_result.cfm?locationId=0&entryTypeId=5'
        search_page = self.soupify(search_page_url)
        total_entries_as_string = search_page.find('h2', {'class': 'easSearchHeading'}).next.strip()
        formatted_entry_number = int(total_entries_as_string.replace('.', ''))
        end_page = math.ceil(formatted_entry_number / 15)

        if(self.debug):
            print(f'Crawling {end_page} pages with 15 entries each.')
        
        return end_page
