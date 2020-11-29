import unittest

from Scraper import Scraper


class TestScraper(unittest.TestCase):
    """Tests the Scraper class."""

    def setUp(self):
        self.scraper = Scraper('test')

    def test_clean_string(self):
        output = self.scraper.clean_string('\t\n\r  test   \r\t\n1\n\r\t   ')
        self.assertEqual('test   1', output)

    def test_clean_string_none(self):
        output = self.scraper.clean_string(None)
        self.assertIsNone(output)

    def test_clean_html_tags(self):
        html_string = '<p>brotZeit e.V.<br/></p>' \
                      '<p>' \
                      '<a class=\"\" href=\"/index.cfm?searchTab=organization_detail&amp;organizationId=69040&amp;\" target=\"_self\" title=\"zur Organisation\">' \
                      '<strong class=\"copy35 c7744 shameOnYouIfYouRemove\"> Ehrenamtssuche Hessen  - <br/><br/>' \
                      '</strong>Zur Detailansicht der Organisation' \
                      '</a>' \
                      '</p>'
        output = self.scraper.clean_html_tags(html_string)
        self.assertEqual('brotZeit e.V. Ehrenamtssuche Hessen  - Zur Detailansicht der Organisation', output)

    def test_clean_html_tags_nane(self):
        output = self.scraper.clean_html_tags(None)
        self.assertIsNone(output)


if __name__ == '__main__':
    unittest.main()
