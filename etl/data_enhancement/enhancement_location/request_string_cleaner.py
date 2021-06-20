import re
from bs4 import BeautifulSoup
from shared.logger_factory import LoggerFactory


class RequestStringCleaner:
    """Class that handles removing irrelevant address fields, leading to better api results"""

    @staticmethod
    def clean_request_string(request_string):
        """Cleans the given request string"""

        # Remove html tags
        result = BeautifulSoup(request_string, 'lxml').text

        # Remove newlines
        result = result.replace('\n', ' ')

        result = RequestStringCleaner._handle_single_field_rules(result)
        result = RequestStringCleaner._handle_multi_field_rules(result)

        return result.strip()

    @staticmethod
    def _handle_single_field_rules(input_string):
        """Execute rules that apply to single address fields"""
        result = input_string
        divider = ','

        address_fields = RequestStringCleaner._split_fields(result, divider)
        result_fields = []
        for field in address_fields:
            field = field.strip()
            if not RequestStringCleaner._remove_field(field):
                result_fields.append(field)
        result = ', '.join(result_fields)
        return result

    @staticmethod
    def _remove_field(field):
        """Determines whether the given field should be removed"""
        is_po = RequestStringCleaner._is_post_office_substring(field)
        is_district = RequestStringCleaner._is_district_substring(field)
        return is_po or is_district

    @staticmethod
    def _handle_multi_field_rules(input_string):
        """Execute rules that are applied across multiple address fields"""
        result = input_string
        result = re.sub(r'\(.*?\)', '', result)
        result = re.sub(r'[0-9]{1,2}\. ?(Stock|OG|Stockwerk) ', '', result)
        result = result.replace(' OT ', ' ')
        return result

    @staticmethod
    def _split_fields(input_string, divider):
        """Splits an input string using the given divider"""
        return input_string.split(divider)

    @staticmethod
    def _is_post_office_substring(input_string):
        """Determines whether the given input string matches the post office pattern (e.g. P.O. Box <number>)"""
        return len(re.findall(r'P\.? *O\.? *B[ox|OX][- 0-9]*[^,./]{0,4}', string=input_string)) > 0

    @staticmethod
    def _is_district_substring(input_string):
        """Determines whether the given input string is a district address field"""
        return len(re.findall(r'[Dd]istrict', string=input_string)) > 0

