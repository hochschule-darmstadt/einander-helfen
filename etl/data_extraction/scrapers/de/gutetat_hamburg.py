from data_extraction.scraper import Scraper
from scrapers.de.gutetat_berlin import GuteTatBerlinScraper


class GuteTatHamburgScraper(GuteTatBerlinScraper, Scraper):
    """Scrapes the website gute-tat.de for the region hamburg."""

    def __init__(self, name, context):
        """Constructor of GuteTatHamburgScraper."""

        super().__init__(name, context)

        # user id 15 leads to hamburg
        self.user_id = 15
