import math
import re
import time

from data_extraction.Scraper import Scraper
from shared.utils import clean_string


class GuteTatBerlinScraper(Scraper):
    """Scrapes the website gute-tat.de for the region berlin."""

    base_url = 'https://ehrenamtsmanager.gute-tat.de/oberflaeche/'
    website_url = 'www.gute-tat.de'
    debug = True

    def parse(self, response, url):
        """Transforms the soupified response of a detail page in a predefined way and returns it."""

        location_street = response.find_all('strong', text='Straße:')[0].parent.parent.find_all('td')[1].text or None
        location_plzort = response.find_all('strong', text='PLZ, Ort:')[0].parent.parent.find_all('td')[1].text.split(', ') or None
        location_berzirk = response.find('strong', text='Bezirk:').parent.parent.find_all('td')[1].text or None
        location_ortsteil = response.find('strong', text='Ortsteil:').parent.parent.find_all('td')[1].text or None
        location_list = []
        if location_street is not None and len(clean_string(location_street)) > 0:
            location_list.append(location_street)
        if location_plzort is not None and len(location_plzort) > 0:
            location_list.append(', '.join(location_plzort))
        if location_berzirk is not None and len(clean_string(location_berzirk)) > 0:
            location_list.append(location_berzirk)
        if location_ortsteil is not None and len(clean_string(location_ortsteil)) > 0:
            location_list.append(location_ortsteil)

        contact_name = response.find('strong', text='Ansprechperson:').parent.parent.find_all('td')[1].text or None
        contact_street = response.find_all('strong', text='Straße:')[1].parent.parent.find_all('td')[1].text or None
        contact_plzort = response.find_all('strong', text='PLZ, Ort:')[1].parent.parent.find_all('td')[1].text.split(', ') or None
        contact_phone = response.find('strong', text='Telefon:').parent.parent.find_all('td')[1].text or None
        contact_email = response.find('strong', text='E-Mail:').parent.parent.find_all('td')[1].text or None
        contact_fax = response.find('strong', text='Fax:').parent.parent.find_all('td')[1].text or None
        contact_internet = response.find('strong', text='Internet:').parent.parent.find_all('td')[1].text or None
        contact_list = []
        if contact_name is not None and len(clean_string(contact_name)) > 0:
            contact_list.append(clean_string(contact_name))
        if contact_street is not None and len(clean_string(contact_street)) > 0:
            contact_list.append(contact_street)
        if contact_plzort is not None and len(contact_plzort) > 0:
            contact_list.append(', '.join(contact_plzort))
        if contact_phone is not None and len(clean_string(contact_phone)) > 0:
            contact_list.append(f'Tel: {contact_phone}')
        if contact_fax is not None and len(clean_string(contact_fax)) > 0:
            contact_list.append(f'Fax: {contact_fax}')
        if contact_email is not None and len(clean_string(contact_email)) > 0:
            contact_list.append(contact_email)
        if contact_internet is not None and len(clean_string(contact_internet)) > 0:
            contact_list.append(contact_internet)

        parsed_object = {
            'title': response.find('strong', text='Name des Projekts:').parent.parent.find_all('td')[1].text or None,
            'categories': [],
            'location': ' - '.join(location_list) or None,
            'task': response.find('strong', text='Projektbeschreibung:').parent.parent.find_all('td')[1].text or None,
            'target_group': None,
            'timing': response.find('strong', text='Zeitraum:').parent.parent.find_all('td')[1].text or None,
            'effort': response.find('strong', text='Zeitbedarf:').parent.parent.find_all('td')[1].text or None,
            'opportunities': None,
            'organization': response.find('strong', text='Zentrale:').parent.parent.find_all('td')[1].text or None,
            'contact': '<br>'.join(contact_list) or None,
            'link': url or None,
            'source': f'{self.website_url}/helfen/ehrenamtliches-engagement/projekte-berlin',
            'image': f'{self.website_url}/wp-content/uploads/2014/10/logo_gute_tat.gif',
            'geo_location': {
                'lat': 52.520008,
                'lon': 13.404954,
            },
        }

        parsed_object['post_struct'] = {
            'title': clean_string(parsed_object['title']) or None,
            'categories': [],
            'location': {
                'zipcode': clean_string(location_plzort[0]) or None,
                'city': clean_string(location_plzort[1]) or None,
                'street': clean_string(location_street) or None,
            },
            'task': clean_string(parsed_object['task']) or None,
            'target_group': clean_string(parsed_object['target_group']) or None,
            'timing': clean_string(parsed_object['timing']) or None,
            'effort': clean_string(parsed_object['effort']) or None,
            'opportunities': clean_string(parsed_object['opportunities']) or None,
            'organization': {
                'name': clean_string(parsed_object['organization']) or None,
                'zipcode': None,
                'city': None,
                'street': None,
                'phone': None,
                'email': None,
            },
            'contact': {
                'name': clean_string(contact_name) or None,
                'zipcode': clean_string(contact_plzort[0]) or None,
                'city': clean_string(contact_plzort[1]) or None,
                'street': clean_string(contact_street) or None,
                'phone': clean_string(contact_phone) or None,
                'email': clean_string(contact_email) or None,
            },
            'link': parsed_object['link'] or None,
            'source': parsed_object['source'] or None,
            'image': parsed_object['image'] or None,
            'geo_location': parsed_object['geo_location'],
            'map_address': None,
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
