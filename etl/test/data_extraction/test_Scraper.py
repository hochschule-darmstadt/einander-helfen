import unittest

from Scraper import Scraper


class TestScraper(unittest.TestCase):

    def setUp(self):
        self.scraper = Scraper('test')

    def test_clean_string(self):
        output = self.scraper.clean_string('\t\n\r  test   \r\t\n1\n\r\t   ')
        self.assertEqual('test   1', output)

    def test_clean_string_none(self):
        output = self.scraper.clean_string(None)
        self.assertIsNone(output)


if __name__ == '__main__':
    unittest.main()
