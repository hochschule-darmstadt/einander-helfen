import re
from bs4 import BeautifulSoup
from shared.LoggerFactory import LoggerFactory


class RequestStringCleaner:
    """Class that handles removing irrelevant address fields, leading to better api results"""

    logger = LoggerFactory.get_enhancement_logger()

    dividers = {
        'https://www.weltwaerts.de': ','
    }

    def clean_request_string(self, request_string, source=''):
        """Cleans the given request string"""
        result = BeautifulSoup(request_string, 'lxml').text

        divider = ','
        if source in self.dividers:
            divider = self.dividers[source]

        if divider and len(divider) > 0:
            address_fields = self._split_fields(result, divider)
            result_fields = []
            for field in address_fields:
                field = field.strip()
                if not self._remove_field(field):
                    result_fields.append(field)
                else:
                    self.logger.debug(f"Detected and removed irrelevant field: {field}")
            result = ', '.join(result_fields)

        return result.strip()

    def _split_fields(self, input_string, divider):
        """Splits an input string using the given divider"""
        return input_string.split(divider)

    def _remove_field(self, field):
        """Determines whether the given field should be removed"""
        is_po = self._is_post_office_substring(field)
        return is_po

    def _is_post_office_substring(self, input_string):
        """Determines whether the given input string matches the post office pattern (e.g. P.O. Box <number>)"""
        return len(re.findall(r'P\.? *O\.? *B[ox|OX][- 0-9]*[^,./]{0,4}', string=input_string)) > 0

