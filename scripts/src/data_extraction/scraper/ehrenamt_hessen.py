from lib.Scraper import Scraper


class __Scraper__(Scraper):
    base_url = 'https://www.ehrenamtssuche-hessen.de'
    debug = True

    def parse(self, response, url):

        try:
            parsed_object = {
                'title': response('h3', {'class': 'ItemTitle'})[0].get_text() or None,
                'link': url or None,
                'organization': response('div', {'class': 'legendLeft'}, text='Organisation/Anbieter')[0].parent.find(
                    'div', {'class': 'descriptionRight'}).get_text() or None,
                'task': response('div', {'class': 'legendLeft'}, text='Ihr Aufgabenfeld')[0].parent.find('div', {
                    'class': 'descriptionRight'}).get_text() or None,
                'location': response('div', {'class': 'legendLeft'}, text='Ort Ihres Ehrenamts')[0].parent.find('div', {
                    'class': 'descriptionRight'}).get_text() or None,
                'contact': response('div', {'class': 'legendLeft'}, text='Ihr Ansprechpartner')[0].parent.find('div', {
                    'class': 'descriptionRight'}).get_text() or None,
                'lat': response('div', {'class': 'legendLeft'}, text='Ort Ihres Ehrenamts')[0].parent.find('div', {
                    'class': 'descriptionRight'}).find('li', {'class': 'geodata'}).get('data-pos-lat') or None,
                'lon': response('div', {'class': 'legendLeft'}, text='Ort Ihres Ehrenamts')[0].parent.find('div', {
                    'class': 'descriptionRight'}).find('li', {'class': 'geodata'}).get('data-pos-lon') or None,
            }
            cat_object = []
            for cat in response('div', {'class': 'legendLeft'}, text='Kategorien')[0].parent.find('div', {
                'class': 'descriptionRight'}).find('div', {'class': 'easCategories'}).find_all('div',
                                                                                               {'class': 'catIcon'}):
                cat_object.append(cat.get('title'))

            parsed_object['categories'] = cat_object
            return parsed_object
        except:
            self.error_urls.append(url)
            return None

    def add_urls(self):
        # Get the first page of entries
        # TODO: make range dynamic
        for index in range(1, 125):
            search_page_url = f'{self.base_url}/entry_search_result.cfm?locationId=0&entryTypeId=5&page={str(index)}'
            search_result_page = self.soupify(search_page_url)
            detail_links = search_result_page.findAll('a', href=True, text='Details')

            if len(detail_links) == 0:
                print(f"nix mehr gefunden: {index}")
                break

            for detailLink in detail_links:
                self.urls.append(self.base_url + detailLink['href'])
