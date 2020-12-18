import json
import unittest

from enhancement_duplicates.enhancement_exact_duplicates import remove_duplicates


class TestEnhancementExactDuplicates(unittest.TestCase):
    def test_remove_duplicates(self):
        data = '[' \
               '    {' \
               '        "title": "a1",' \
               '        "task": "a2",' \
               '        "link": "a3",' \
               '        "source": "a4",' \
               '        "id": "a5",' \
               '        "post_struct": "a6"' \
               '    },' \
               '    {' \
               '        "title": "a1",' \
               '        "task": "a2",' \
               '        "link": "a3",' \
               '        "source": "a4",' \
               '        "id": "a5",' \
               '        "post_struct": "a6"' \
               '    },' \
               '    {' \
               '        "title": "a1",' \
               '        "task": "a2",' \
               '        "link": "a7",' \
               '        "source": "a8",' \
               '        "id": "a9",' \
               '        "post_struct": "a10"' \
               '    },' \
               '    {' \
               '        "title": "a11",' \
               '        "task": "a12",' \
               '        "link": "a7",' \
               '        "source": "a8",' \
               '        "id": "a9",' \
               '        "post_struct": "a10"' \
               '    }' \
               ']'
        json_data = json.loads(data)

        remove_duplicates(json_data)

        self.assertEqual(2, len(json_data))


if __name__ == '__main__':
    unittest.main()
