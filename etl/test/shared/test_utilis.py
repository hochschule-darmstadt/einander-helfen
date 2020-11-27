import unittest

from shared.utils import clean_string


class TestUtils(unittest.TestCase):
    def test_clean_string(self):
        output = clean_string('\t\n\r  test   \r\t\n1\n\r\t   ')
        self.assertEqual('test   1', output)

    def test_clean_string_none(self):
        output = clean_string(None)
        self.assertIsNone(output)


if __name__ == '__main__':
    unittest.main()
