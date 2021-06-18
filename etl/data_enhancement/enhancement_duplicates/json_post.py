from copy import deepcopy
from shared.logger_factory import LoggerFactory


class JsonPost:
    """Handles the data to find duplicates."""

    logger = LoggerFactory.get_enhancement_logger()

    def __init__(self, json):
        """Constructor of JsonPost."""

        self.json = json
        self.mod_json = self._remove_not_needed_data(deepcopy(json))
        self.is_duplicate = False

    @staticmethod
    def _remove_not_needed_data(json):
        """Removes data from json which should not be use in the comparison."""

        if 'link' in json:
            del json['link']
        if 'source' in json:
            del json['source']
        if 'id' in json:
            del json['id']
        if 'post_struct' in json:
            del json['post_struct']

        return json
