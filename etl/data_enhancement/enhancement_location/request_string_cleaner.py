import re
from bs4 import BeautifulSoup
from shared.LoggerFactory import LoggerFactory


class RequestStringCleaner:
    """Class that handles removing irrelevant address fields, leading to better api results"""

    logger = LoggerFactory.get_enhancement_logger()

    def clean_request_string(self, request_string):
        """Cleans the given request string"""

        # Remove html tags
        result = BeautifulSoup(request_string, 'lxml').text

        # Remove newlines
        result = result.replace('\n', ' ')

        result = self._handle_single_field_rules(result)
        result = self._handle_multi_field_rules(result)

        return result.strip()

    def _handle_single_field_rules(self, input_string):
        """Execute rules that apply to single address fields"""
        result = input_string
        divider = ','

        address_fields = self._split_fields(result, divider)
        result_fields = []
        for field in address_fields:
            field = field.strip()
            if not self._remove_field(field):
                result_fields.append(field)
            else:
                self.logger.debug(f"Detected and removed irrelevant field: {field}")
        result = ', '.join(result_fields)
        return result

    def _handle_multi_field_rules(self, input_string):
        """Execute rules that are applied across multiple address fields"""
        result = input_string
        result = re.sub(r'\(.*?\)', '', result)
        result = re.sub(r'[0-9]{1,2}\. ?(Stock|OG|Stockwerk) ', '', result)
        result = result.replace(' OT ', ' ')
        return result

    def _split_fields(self, input_string, divider):
        """Splits an input string using the given divider"""
        return input_string.split(divider)

    def _remove_field(self, field):
        """Determines whether the given field should be removed"""
        is_po = self._is_post_office_substring(field)
        is_district = self._is_district_substring(field)
        return is_po or is_district

    def _is_post_office_substring(self, input_string):
        """Determines whether the given input string matches the post office pattern (e.g. P.O. Box <number>)"""
        return len(re.findall(r'P\.? *O\.? *B[ox|OX][- 0-9]*[^,./]{0,4}', string=input_string)) > 0

    def _is_district_substring(self, input_string):
        """Determines whether the given input string is a district address field"""
        return len(re.findall(r'[Dd]istrict', string=input_string)) > 0

