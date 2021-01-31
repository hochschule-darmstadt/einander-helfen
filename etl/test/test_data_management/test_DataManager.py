import unittest
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ['ROOT_DIR'] = ROOT_DIR

from data_management.DataManager import DataManager


class TestDataManager(unittest.TestCase):

    def test_timestamp_to_datestring(self):
        timestamp = 1577833200.0
        datestring = "01.01.2020"
        self.assertEqual(datestring, DataManager.timestamp_to_datestring(timestamp))

    def test_datestring_to_timestamp(self):
        timestamp = 1577833200.0
        datestring = "01.01.2020"
        self.assertEqual(timestamp, DataManager.datestring_to_timestamp(datestring))


if __name__ == '__main__':
    unittest.main()
