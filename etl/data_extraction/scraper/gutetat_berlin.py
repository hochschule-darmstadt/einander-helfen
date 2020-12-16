import math
import re
import time

from data_extraction.Scraper import Scraper


class GuteTatBerlinScraper(Scraper):
    """Scrapes the website gute-tat.de for the region berlin."""

    def __init__(self, name):
        """Constructor of GuteTatBerlinScraper."""

        super().__init__(name)
        self.base_url = 'https://ehrenamtsmanager.gute-tat.de/oberflaeche/'
        self.website_url = 'www.gute-tat.de'

        # user id 14 leads to berlin
        self.user_id = 14

    def parse(self, response, url):
        """Transforms the soupified response of a detail page in a predefined way and returns it."""

        self.logger.debug("parse()")

        main_table = response.find('table')
        project_address_attr = main_table.find_all('tr')[23:30]
        project_address_str = ''
        for tr in project_address_attr:
            project_address_str += str(tr)
        project_address_str = "<table>" + project_address_str + "</table>"

        contact_attr = main_table.find_all('tr')[34:47]
        contact_str = ''
        for tr in contact_attr:
            contact_str += str(tr)
        contact_str = "<table>" + contact_str + "</table>"

        parsed_object = {
            'title': response.find('strong', text='Name des Projekts:').parent.parent.find_all('td')[1].text or None,
            'categories': [],
            'location': project_address_str or None,
            'task': response.find('strong', text='Projektbeschreibung:').parent.parent.find_all('td')[1].text or None,
            'target_group': None,
            'prerequisites': response.find('strong', text='Voraussetzungen/Vorkenntnisse:').parent.parent.find_all('td')[1].text or None,
            'timing': response.find('strong', text='Zeitraum:').parent.parent.find_all('td')[1].text or None,
            'effort': response.find('strong', text='Zeitbedarf:').parent.parent.find_all('td')[1].text or None,
            'opportunities': None,
            'organization': None,
            'contact': contact_str or None,
            'link': url or None,
            'source': self.website_url,
            'geo_location': None,
        }

        location_street = response.find_all('strong', text='Straße:')[0].parent.parent.find_all('td')[1].text or None
        location_plzort = response.find_all('strong', text='PLZ, Ort:')[0].parent.parent.find_all('td')[1].text.split(', ') or None

        contact_name = response.find('strong', text='Ansprechperson:').parent.parent.find_all('td')[1].text or None
        contact_street = response.find_all('strong', text='Straße:')[1].parent.parent.find_all('td')[1].text or None
        contact_plzort = response.find_all('strong', text='PLZ, Ort:')[1].parent.parent.find_all('td')[1].text.split(', ') or None
        contact_phone = response.find('strong', text='Telefon:').parent.parent.find_all('td')[1].text or None
        contact_email = response.find('strong', text='E-Mail:').parent.parent.find_all('td')[1].text or None

        parsed_object['post_struct'] = {
            'title': self.clean_string(parsed_object['title']) or None,
            'categories': [],
            'location': {
                'country': "Deutschland",
                'zipcode': self.clean_string(location_plzort[0]) or None,
                'city': self.clean_string(location_plzort[1]) or None,
                'street': self.clean_string(location_street) or None,
            },
            'task': self.clean_string(parsed_object['task']) or None,
            'target_group': None,
            'prerequisites': self.remove_unnecessary_whitespaces(
                self.clean_string(parsed_object['prerequisites'], ' ')) or None,
            'timing': self.clean_string(parsed_object['timing']) or None,
            'effort': self.clean_string(parsed_object['effort']) or None,
            'opportunities': None,
            'organization': {
                'name': None,
                'zipcode': None,
                'city': None,
                'street': None,
                'phone': None,
                'email': None,
            },
            'contact': {
                'name': self.clean_string(contact_name) or None,
                'zipcode': self.clean_string(contact_plzort[0]) or None,
                'city': self.clean_string(contact_plzort[1]) or None,
                'street': self.clean_string(contact_street) or None,
                'phone': self.clean_string(contact_phone) or None,
                'email': self.clean_string(contact_email) or None,
            },
            'link': parsed_object['link'] or None,
            'source': parsed_object['source'] or None,
            'geo_location': parsed_object['geo_location'],
            'map_address': None,
        }

        return parsed_object

    def add_urls(self):
        """Adds URLs to an array which is later iterated over and scraped each."""

        self.logger.debug("add_urls()")

        end_page = self.__fetch_end_page()

        for index in range(1, end_page + 1):
            time.sleep(self.delay)

            search_page_url = f'{self.base_url}index.cfm?dateiname=ehrenamt_suche_ergebnis.cfm&anwender_id={self.user_id}&seite={str(index)}&ehrenamt_id=0&ea_projekt=0&stichwort=&kiez=&kiez_fk=0&bezirk=&bezirk_fk=0&ort=&ort_fk=0&zielgruppe=0&taetigkeit=0&merkmale=0&einsatzbereiche=0&plz=&organisation_fk=0&rl=0'
            search_page = self.soupify(search_page_url)
            # last link needs to be ignored
            detail_links = [x for x in search_page.find_all('a', {'class': 'links'})][:-1]

            self.logger.debug(f'Fetched {len(detail_links)} URLs from {search_page_url} [{index}/{end_page}]')

            for detail_link in detail_links:
                current_link = self.base_url + detail_link['href']
                if current_link in self.urls:
                    self.logger.warning(f"func: add_urls, 'body:'page_index: {index},"
                                        f" search_page: {search_page_url}, "
                                        f"duplicate_index: {current_link}, "
                                        f"duplicate_index: {self.urls.index(current_link)}")
                    #self.add_error({
                    #    'func': 'add_urls',
                    #    'body': {
                    #        'page_index': index,
                    #        'search_page': search_page_url,
                    #        'duplicate_link': current_link,
                    #        'duplicate_index': self.urls.index(current_link)
                    #    }
                    #})
                else:
                    self.urls.append(current_link)

        self.logger.debug(len(self.urls))

    def __fetch_end_page(self):
        """Fetches the number of pages from the search result page for the add_urls function."""

        self.logger.debug("__fetch_end_page()")

        entries_per_page = 30

        search_page_url = f'{self.base_url}index.cfm?dateiname=ehrenamt_suche_ergebnis.cfm&anwender_id={self.user_id}&seite=1&ehrenamt_id=0&ea_projekt=0&stichwort=&kiez=&kiez_fk=0&bezirk=&bezirk_fk=0&ort=&ort_fk=0&zielgruppe=0&taetigkeit=0&merkmale=0&einsatzbereiche=0&plz=&organisation_fk=0&rl=0'
        search_page = self.soupify(search_page_url)
        total_entries_as_string = search_page.find('td', {'class': 'ueberschrift'}).next.strip()
        formatted_entry_number = int(re.search(r'\d+', total_entries_as_string).group())
        end_page = math.ceil(formatted_entry_number / entries_per_page)

        self.logger.debug(f'Crawling {end_page} pages with {entries_per_page} entries each.')

        return end_page
