from data_extraction.scraper import Scraper
from scrapers.gutetat_berlin import GuteTatBerlinScraper


class GuteTatMunichScraper(GuteTatBerlinScraper, Scraper):
    """Scrapes the website gute-tat.de for the region munich."""

    def __init__(self, name):
        """Constructor of GuteTatMunichScraper."""

        super().__init__(name)

        # user id 16 leads to munich
        self.user_id = 16
