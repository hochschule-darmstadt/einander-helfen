import math
import re
import time

from data_extraction.Scraper import Scraper


class GuteTatBerlinScraper(Scraper):
    """Scrapes the website gute-tat.de for the region berlin."""

    base_url = 'https://ehrenamtsmanager.gute-tat.de/oberflaeche/'
    website_url = 'www.gute-tat.de'
    debug = True

    def parse(self, response, url):
        """Transforms the soupified response of a detail page in a predefined way and returns it."""

        parsed_object = {
            'title': response.find('strong', text='Name des Projekts:').parent.parent.find_all('td')[1].text or None,
            'categories': None,
            'location': response.find_all('strong', text='PLZ, Ort:')[0].parent.parent.find_all('td')[1].text + ', ' +
                        response.find('strong', text='Straße:').parent.parent.find_all('td')[1].text + ', ' +
                        response.find('strong', text='Bezirk:').parent.parent.find_all('td')[1].text + ', ' +
                        response.find('strong', text='Ortsteil:').parent.parent.find_all('td')[1].text or None,
            'task': response.find('strong', text='Projektbeschreibung:').parent.parent.find_all('td')[1].text or None,
            'timing': response.find('strong', text='Zeitraum:').parent.parent.find_all('td')[1].text or None,
            'effort': response.find('strong', text='Zeitbedarf:').parent.parent.find_all('td')[1].text or None,
            'organization': response.find('strong', text='Zentrale:').parent.parent.find_all('td')[1].text or None,
            'contact': response.find('strong', text='Ansprechperson:').parent.parent.find_all('td')[1].text + '<br>' +
                       response.find('strong', text='Straße:').parent.parent.find_all('td')[1].text + '<br>' +
                       response.find_all('strong', text='PLZ, Ort:')[1].parent.parent.find_all('td')[1].text + '<br>' +
                       response.find('strong', text='Telefon:').parent.parent.find_all('td')[1].text + '<br>' +
                       response.find('strong', text='Fax:').parent.parent.find_all('td')[1].text + '<br>' +
                       response.find('strong', text='E-Mail:').parent.parent.find_all('td')[1].text + '<br>' +
                       response.find('strong', text='Internet:').parent.parent.find_all('td')[1].text or None,
            'link': url or None,
            'image': f'{self.website_url}/wp-content/uploads/2014/10/logo_gute_tat.gif',
            'geo_location': {
                'lat': None,
                'lon': None,
            },
            'source': f'{self.website_url}/helfen/ehrenamtliches-engagement/projekte-berlin',
        }

        return parsed_object

    def add_urls(self):
        """Adds URLs to an array which is later iterated over and scraped each."""

        end_page = self.__fetch_end_page()

        for index in range(1, end_page + 1):
            time.sleep(self.delay)

            search_page_url = f'{self.base_url}index.cfm?dateiname=ehrenamt_suche_ergebnis.cfm&anwender_id=14&seite={str(index)}&ehrenamt_id=0&ea_projekt=0&stichwort=&kiez=&kiez_fk=0&bezirk=&bezirk_fk=0&ort=&ort_fk=0&zielgruppe=0&taetigkeit=0&merkmale=0&einsatzbereiche=0&plz=&organisation_fk=0&rl=0'
            search_page = self.soupify(search_page_url)
            # last link needs to be ignored
            detail_links = [x for x in search_page.find_all('a', {'class': 'links'})][:-1]

            if self.debug:
                print(f'Fetched {len(detail_links)} URLs from {search_page_url} [{index}/{end_page}]')

            for detail_link in detail_links:
                current_link = self.base_url + detail_link['href']
                if current_link in self.urls:
                    self.add_error({
                        'func': 'add_urls',
                        'body': {
                            'page_index': index,
                            'search_page': search_page_url,
                            'duplicate_link': current_link,
                            'duplicate_index': self.urls.index(current_link)
                        }
                    })
                else:
                    self.urls.append(current_link)

        print(len(self.urls))

    def __fetch_end_page(self):
        """Fetches the number of pages from the search result page for the add_urls function."""

        entries_per_page = 30

        search_page_url = f'{self.base_url}index.cfm?dateiname=ehrenamt_suche_ergebnis.cfm&anwender_id=14&seite=1&ehrenamt_id=0&ea_projekt=0&stichwort=&kiez=&kiez_fk=0&bezirk=&bezirk_fk=0&ort=&ort_fk=0&zielgruppe=0&taetigkeit=0&merkmale=0&einsatzbereiche=0&plz=&organisation_fk=0&rl=0'
        search_page = self.soupify(search_page_url)
        total_entries_as_string = search_page.find('td', {'class': 'ueberschrift'}).next.strip()
        formatted_entry_number = int(re.search(r'\d+', total_entries_as_string).group())
        end_page = math.ceil(formatted_entry_number / entries_per_page)

        if self.debug:
            print(f'Crawling {end_page} pages with {entries_per_page} entries each.')

        return end_page
