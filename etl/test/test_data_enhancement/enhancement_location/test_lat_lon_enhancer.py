import os
import unittest

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ['ROOT_DIR'] = ROOT_DIR

from data_enhancement.enhancement_location.lat_lon_enhancer import LatLonEnhancer


class TestLatLonEnhancer(unittest.TestCase):

    def test_get_api_request_string(self):
        result = LatLonEnhancer.get_api_request_string(self.test_data[0])
        self.assertEqual(self.expected_results[0], result)

        result = LatLonEnhancer.get_api_request_string(self.test_data[1])
        self.assertEqual(self.expected_results[1], result)

        result = LatLonEnhancer.get_api_request_string(self.test_data[2])
        self.assertEqual(self.expected_results[2], result)

        result = LatLonEnhancer.get_api_request_string(self.test_data[3])
        self.assertEqual(self.expected_results[3], result)

        result = LatLonEnhancer.get_api_request_string(self.test_data[4])
        self.assertEqual(self.expected_results[4], result)

        result = LatLonEnhancer.get_api_request_string(self.test_data[5])
        self.assertEqual(self.expected_results[5], result)

    expected_results = [
        "Peru",
        "Okenstraße 15 Freiburg",
        "Okenstraße 15 79108 Freiburg",
        "",
        "",
        "Freiburg"
    ]

    test_data = [
        {
            "post_struct": {
                "location": {
                    "country": "Peru"
                },
                "organization": {
                    "name": "Un Millón de Niños Lectores"
                },
                "contact": {
                    "zipcode": "79108",
                    "city": "Freiburg",
                    "street": "Okenstraße 15",
                }
            }
        },
        {
            "post_struct": {
                "location": {
                    "country": None
                },
                "organization": {
                    "name": "Un Millón de Niños Lectores",
                    "city": "Freiburg",
                    "street": "Okenstraße 15",
                },
                "contact": {
                    "zipcode": None,
                    "city": None,
                    "street": None,
                }
            }
        },
        {
            "post_struct": {
                "location": {
                    "country": None
                },
                "organization": {
                    "name": "Un Millón de Niños Lectores"
                },
                "contact": {
                    "zipcode": "79108",
                    "city": "Freiburg",
                    "street": "Okenstraße 15",
                }
            }
        },
        {
            "post_struct": {
                "location": {
                    "country": None,
                    "zipcode": None,
                    "city": None,
                    "street": None,
                },
                "organization": {
                    "name": "Un Millón de Niños Lectores"
                },
                "contact": {
                    "zipcode": None,
                    "city": None,
                    "street": None,
                }
            }
        },
        {
            "post_struct": {
                "location": None,
                "organization": None,
                "contact": None,
            }
        },
        {
            "post_struct": {
                "location": {
                    "country": None
                },
                "organization": {
                    "name": "Un Millón de Niños Lectores",
                    "city": "Freiburg",
                    "street": "",
                },
                "contact": {
                    "zipcode": None,
                    "city": None,
                    "street": None,
                }
            }
        },
    ]


if __name__ == '__main__':
    unittest.main()
