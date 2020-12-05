import json
import unittest

from enhancement_duplicates.enhancement_exact_duplicates import remove_duplicates


class TestEnhancementExactDuplicates(unittest.TestCase):
    def test_remove_duplicates(self):
        data = '[' \
               '    {' \
               '        "a": "a1",' \
               '        "link": "a2",' \
               '        "source": "a3",' \
               '        "id": "a4",' \
               '        "post_struct": "a5"' \
               '    },' \
               '    {' \
               '        "a": "a1",' \
               '        "link": "a6",' \
               '        "source": "a7",' \
               '        "id": "a8",' \
               '        "post_struct": "a9"' \
               '    },' \
               '    {' \
               '        "a": "a10",' \
               '        "link": "a6",' \
               '        "source": "a7",' \
               '        "id": "a8",' \
               '        "post_struct": "a9"' \
               '    }' \
               ']'
        json_data = json.loads(data)

        remove_duplicates(json_data)

        self.assertEqual(2, len(json_data))


if __name__ == '__main__':
    unittest.main()
