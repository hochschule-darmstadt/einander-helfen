from data_extraction.Scraper import Scraper
import re
import math

class BundesFreiwilligendienst(Scraper):

    base_url = "https://www.bundesfreiwilligendienst.de"
    debug = True

    def parse(self, response, url):

        content = response.find('div', {'class': 'tx-bfd-einsatzstellensuche'})

        title = content.find('div', {'class': 'span12'})
        categories = content.find('table', {'class': 'platzangebote table table-striped'})
        location = content.find('div', {'class': 'span5'}).find_all('div', {'class': 'box white-bg'})[0]
        task = content.find('div', {'class': 'description'})
        contact = content.find('div', {'class': 'span5'}).find_all('div', {'class': 'box white-bg'})[1].find('div', {'class': 'box-content'})





        parsed_object = {
            'title': title.find('h1').decode_contents().strip() if title is not None else None,
            'categories': categories.find('tbody').find('tr').find_all('td')[1].find('li').decode_contents().strip() if categories is not None else None,
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
            'geo_location': None,
            'languages': None,
            'requirements': None,

        }

        location_street = location.find_all('div', {'class': 'span12'})[0].find('div', {'class': 'span10'})
        location_plz = location.find_all('div', {'class': 'span12'})[1].find('span', {'class': 'span10'})
        location_ort = location.find_all('div', {'class': 'span12'})[2].find('span', {'class': 'span10'})

        contact_name = contact.find_all('div', {'class': 'span12'})[0].find('div', {'class': 'span10'})
        contact_phone = contact.find_all('div', {'class': 'span12'})[1].find('span', {'class': 'span10'})
        contact_email = contact.find_all('div', {'class': 'span12'})[2].find('span', {'class': 'span10'}).find('a')

        parsed_object['post_struct'] = {
            'title': self.clean_string(parsed_object['title']) or None,
            'categories': parsed_object['categories'] or None,
            'location': {
                'country': None,
                'zipcode': self.clean_string(location_plz.decode_contents()) if location_plz is not None else None,
                'city': self.clean_string(location_ort.decode_contents()) if location_ort is not None else None,
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

        search_page_url = f'{self.base_url}/bundesfreiwilligendienst/platz-einsatzstellensuche/einsatzstelle-suchen.html?tx_bfdeinsatzstellensuche_einsatzstellensuche%5Baction%5D=liste&tx_bfdeinsatzstellensuche_einsatzstellensuche%5Bcontroller%5D=Suchen%5CEinsatzstellensuche&cHash=ff2107f5ca1fc1b5b392cc09ff84a3c3'
        next_page_url = search_page_url

        index = 1

        while next_page_url:

            response = self.soupify(next_page_url)

            detail_link_tags = [x.find('a') for x in response.find_all('td', {'class': 'row5'})]
            #detail_link_tags = list(filter(lambda x: x['href'].startswith('/was-du-tun-kannst/deine-moeglichkeiten/ehrenamt-finden/detail.html?'), detail_link_tags))
            print(detail_link_tags)

            # Get maximum number of pages
            index_max = response.find('ul', {'class': 'pagination'}).find_all('li')[8].find('a').decode_contents().strip()

            if self.debug:
                print(f'Fetched {len(detail_link_tags)} URLs from {next_page_url} [{index}/{index_max}]')

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
                next_page_url = index_max = response.find('ul', {'class': 'pagination'}).find_all('li')[9]
                if next_page_url:
                    next_page_url = self.base_url + '/' + next_page_url.find('a')['href']

                index += 1

                if index > 3:
                    break

                time.sleep(self.delay)