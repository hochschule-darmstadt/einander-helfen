from copy import deepcopy


class JsonPost:

    def __init__(self, json):
        self.json = json
        self.mod_json = self.__remove_not_needed_data(deepcopy(json))
        self.is_duplicate = False

    @staticmethod
    def __remove_not_needed_data(json):
        if 'link' in json:
            del json['link']
        if 'source' in json:
            del json['source']
        if 'id' in json:
            del json['id']
        if 'post_struct' in json:
            del json['post_struct']

        return json
