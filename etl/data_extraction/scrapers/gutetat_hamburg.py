from data_extraction.scraper import Scraper
from scrapers.gutetat_berlin import GuteTatBerlinScraper


class GuteTatHamburgScraper(GuteTatBerlinScraper, Scraper):
    """Scrapes the website gute-tat.de for the region hamburg."""

    def __init__(self, name):
        """Constructor of GuteTatHamburgScraper."""

        super().__init__(name)

        # user id 15 leads to hamburg
        self.user_id = 15
