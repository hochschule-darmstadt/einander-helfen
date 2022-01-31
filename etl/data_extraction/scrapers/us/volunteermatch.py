import math
import re

from data_extraction.scraper import Scraper


class VolunteermatchScraper(Scraper):
    """Scrapes the website volunteermatch.org."""

    base_url = 'https://www.volunteermatch.org'
    debug = True

    def parse(self, response, url):
        """Handles the soupified response of a detail page in the predefined way and returns it"""
        self.logger.debug('parse()')

        # parse metadata
        metadata = response.find_all('meta')
        title = lat = lon = street = city = region = zipcode = country = None
        for meta in metadata:
            if 'property' in meta.attrs and meta.attrs['property'] == 'og:title':
                title = meta.attrs['content']
            elif 'property' in meta.attrs and meta.attrs['property'] == 'og:latitude':
                lat = meta.attrs['content']
            elif 'property' in meta.attrs and meta.attrs['property'] == 'og:longitude':
                lon = meta.attrs['content']
            elif 'property' in meta.attrs and meta.attrs['property'] == 'og:street-address':
                street = meta.attrs['content']
            elif 'property' in meta.attrs and meta.attrs['property'] == 'og:locality':
                city = meta.attrs['content']
            elif 'property' in meta.attrs and meta.attrs['property'] == 'og:region':
                region = meta.attrs['content']
            elif 'property' in meta.attrs and meta.attrs['property'] == 'og:postal-code':
                zipcode = meta.attrs['content']
            elif 'property' in meta.attrs and meta.attrs['property'] == 'og:country-name':
                country = meta.attrs['content']
        
        content = response.find('div', {'id': 'content_opp_details'})

        logistics = content.find('div', {'class': 'logistics'})

        # Get categories
        categories_box = logistics.find('div', {'class': 'logistics__causes'})
        categories_tag = categories_box.find_all('svg')
        categories = []
        if categories_tag is not None:
            for cat_entry in categories_tag:
                categories.append(cat_entry['title'].strip())

        # Get target groups
        target_group_box = content.find('section', {'class': 'logistics__section--friendlies'}).find('ul')
        target_groups_raw = target_groups = None
        if target_group_box is not None:
            target_groups_raw = target_group_box.prettify()
            target_groups = []
            for target_group in target_group_box.find_all('li'):
                target_groups.append(target_group.decode_contents().strip())
            target_groups = ', '.join(target_groups)

        # Get requirements
        requirements_box = content.find('section', {'class': 'logistics__section--requirements'}).find('ul')
        requirements_raw = None
        requirements = []
        if requirements_box is not None:
            requirements_raw = requirements_box.prettify()
            for requirement in requirements_box.find_all('li'):
                requirements.append(requirement.decode_contents().strip())
        
        # Get skills
        skills_box = content.find('section', {'class': 'logistics__section--skills'}).find('ul')
        if skills_box is not None:
            requirements_raw = (requirements_raw if requirements_raw else '')  + skills_box.prettify()
            for skill in skills_box.find_all('li'):
                requirements.append(skill.decode_contents().strip())

        requirements = ', '.join(requirements)

        # Get timing
        timing = content.find('section', {'class': 'logistics__section--when'}).find('div', {'class': 'para'}).decode_contents().strip()

        # Get organisation
        organisation_box = content.find('p', {'class': 'opp-dtl__org-name'})
        organisation = None
        if organisation_box is not None:
            organisation = organisation_box.a.decode_contents().strip()

        # Get contact
        contact_box = content.find('section', {'id': 'tertiary-content'})
        contact = None
        if contact_box is not None:
            contact_address = contact_box.find('h4', {'class': 'l-location'})
            contact = contact_address.findNext('p').decode_contents().strip()

        # Get description
        description_box = content.find('div', {'id': 'short_desc'})
        description = None
        if description_box is not None:
            description = []
            for desc in description_box.find_all('p'):
                description.append(desc.prettify())
            description = ''.join(description)

        parsed_object = {
            'title': title,
            'categories': categories,
            'location': ', '.join(filter(None, [street, city, region, zipcode, country])) or None,
            'task': description,
            'target_group': target_groups_raw,
            'prerequisites': requirements_raw,
            'language_skills': None,
            'timing': timing,
            'effort': None,
            'opportunities': None,
            'organization': organisation,
            'contact': contact,
            'link': url or None,
            'source': 'www.volunteermatch.org',
            'geo_location': {
                'lat': lat,
                'lon': lon,
            } if lat and lon else None,  # If longitude and latitude are None, geo_location is set to None,
        }

        parsed_object['post_struct'] = {
            'title': parsed_object['title'],
            'categories': parsed_object['categories'],
            'location': {
                'country': country,
                'region': region,
                'zipcode': zipcode,
                'city': city,
                'street': street,
                'continent': 'North America',
            },
            'task': self.clean_html_tags(description),
            'target_group': target_groups,
            'prerequisites': requirements,
            'language_skills': parsed_object['language_skills'],
            'timing': parsed_object['timing'],
            'effort': None,
            'opportunities': None,
            'organization': {
                'name': parsed_object['organization'],
                'region': None,
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

        return parsed_object

    def add_urls(self):
        """Adds all URLs of detail pages, found on the search pages, for the crawl function to scrape"""
        self.logger.debug('add_urls()')

        import time

        index = 1
        index_max = None
        pagesize = 25

        search_page_url = f'{self.base_url}/s/srp/search'

        next_page_url = search_page_url

        while next_page_url:

            body = '{"query":"query {\\nsearchSRP(input:{\\nreturnVirtualAndOnSiteOpps: true\\nlocation: \\"United States\\"\\nvirtual: false\\ncategories: []\\nskills: []\\nradius: \\"1\\"\\ngreatFor: []\\nspecialFlag: \\"\\"\\nkeywords: []\\npageNumber: '+f'{index}'+'\\nsortCriteria: null\\nnumberOfResults: '+f'{pagesize}'+'\\n}){\\nnumberOfResults\\nresultsSize\\noriginalResultSize\\ncurrentPage\\nsortCriteria\\nhasDistanceCriteria\\ntopCity\\ntotalVolunteersNeeded\\ncityLocation\\nsrpOpportunities{\\ndetail {\\ncategories\\nid\\nlocation {\\ncity\\ncountry\\npostalCode\\nregion\\nvirtual\\n}\\nparentOrg {\\nid\\nname\\n}\\nshifts {\\nid\\n}\\ntitle\\nurl\\n}\\ndateRange {\\nendDate\\nendTime\\nongoing\\nsingleDayOpps\\nstartDate\\nstartTime\\n}\\ndistance\\nparentOrgOppCount\\nplaintextDescription\\npostDate\\npremiumOrg\\n}}}","location":"United States","radius":"1"}'

            response = self.rest_post(next_page_url, body)

            response = response.json()['data']['searchSRP']

            # Get maximum number of pages
            index_max = math.ceil(response['resultsSize'] / pagesize)
            
            self.logger.debug(f'Fetched {len(response["srpOpportunities"])} URLs from {next_page_url} [{index}/{index_max}]')
            self.update_fetching_progress(index, index_max)

            # Iterate links and add, if not already found
            for post in response['srpOpportunities']:
                current_link = post['detail']['url']
                if current_link in self.urls:
                    self.logger.debug(f'func: add_urls, page_index: {index},'
                                      f' search_page: {search_page_url}, '
                                      f'duplicate_index: {current_link}, '
                                      f'duplicate_index: {self.urls.index(current_link)}')

                else:
                    self.urls.append(current_link)

            # Get next result page
            if index < index_max:
                index += 1
            else:
                next_page_url = None
            
            time.sleep(self.delay)
