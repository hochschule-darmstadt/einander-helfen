from data_extraction.Scraper import Scraper
from scraper.gutetat_berlin import GuteTatBerlinScraper


class GuteTatHamburgScraper(GuteTatBerlinScraper, Scraper):
    """Scrapes the website gute-tat.de for the region hamburg."""

    def __init__(self, name):
        """Constructor of GuteTatHamburgScraper."""

        super().__init__(name)

        # user id 15 leads to hamburg
        self.user_id = 15
        self.source = f'{self.website_url}/helfen/ehrenamtliches-engagement/projekte-hamburg'
