from scripts.data_extraction.lib import Scraper


class __Scraper__(Scraper):
  base_url = 'https://www.ehrenamtssuche-hessen.de'
  debug = True

  def parse(self, response, url):

    try:
      parsed_object = {
        'provider': response('div', {'class': 'legendLeft'}, text='Organisation/Anbieter')[0].parent.find('div', {
          'class': 'descriptionRight'}).get_text() or None,
        'description': response('div', {'class': 'legendLeft'}, text='Ihr Aufgabenfeld')[0].parent.find('div', {
          'class': 'descriptionRight'}).get_text() or None,
        'locations': response('div', {'class': 'legendLeft'}, text='Ort Ihres Ehrenamts')[0].parent.find('div', {
          'class': 'descriptionRight'}).get_text() or None,
        'contact': response('div', {'class': 'legendLeft'}, text='Ihr Ansprechpartner')[0].parent.find('div', {
          'class': 'descriptionRight'}).get_text() or None
      }
      return parsed_object
    except:
      self.error_urls.append(url)
      return None

  def addUrls(self):
    # Get the first page of entries
    for index in range(1, 2):
      searchPageUrl = f'{self.base_url}/entry_search_result.cfm?locationId=0&entryTypeId=5&page={str(index)}'
      searchResultPage = self.soupify(searchPageUrl)
      detailLinks = searchResultPage.findAll('a', href=True, text='Details')

      if len(detailLinks) == 0:
        break

      for detailLink in detailLinks:
        self.urls.append(self.base_url + detailLink['href'])
