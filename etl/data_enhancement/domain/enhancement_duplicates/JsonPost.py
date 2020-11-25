import re
from copy import deepcopy

from bs4 import BeautifulSoup

from data_enhancement.domain.enhancement_duplicates.PostType import PostType


class JsonPost:
    def __init__(self, file, json_post):
        self.file = file
        self.json_post = json_post
        self.post_type = PostType.QUALIFIED
        self.fuzzy_json_post_str = self.__create_fuzzy_json_post(deepcopy(json_post))

        found_plz = re.search(r'(?<!\d)\d{5}(?!\d)', json_post['location'])
        self.plz = found_plz.group(0) if found_plz else None

    def __create_fuzzy_json_post(self, json_post):
        if 'link' in json_post:
            del json_post['link']
        if 'source' in json_post:
            del json_post['source']
        if 'image' in json_post:
            del json_post['image']
        if 'map_address' in json_post:
            del json_post['map_address']
#        if 'geo_location' in json_post:
#            del json_post['geo_location']

        json_value_arr = []
        self.__extract_json_value(json_value_arr, json_post)
        return BeautifulSoup(';'.join(json_value_arr), 'lxml').text.replace('\\n', '').replace('\\r', '').replace('\\t', '')

    def __extract_json_value(self, value_arr, json_post):
        if type(json_post) == type(dict()):
            for key, value in json_post.items():
                if type(value) == type(dict()) or type(value) == type(list()):
                    self.__extract_json_value(value_arr, value)
                else:
                    value_arr.append(str(value))
        elif type(json_post) == type(list()):
            for value in json_post:
                if type(value) == type(dict()) or type(value) == type(list()):
                    self.__extract_json_value(value_arr, value)
                else:
                    value_arr.append(str(value))
