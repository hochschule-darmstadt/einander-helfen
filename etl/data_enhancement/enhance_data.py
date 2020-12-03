import os
from shared.utils import write_data_to_json, read_data_from_json
from .enhancement_tags import enhancement_tags as e_tags
from .enhancement_links import enhancement_links as e_links
from .enhancement_location import enhancement_location as e_location


os.environ['ROOT_DIR'] = os.getcwd()


class Enhancer:

    def __init__(self, data, domain_name):
        self.__data = data
        self.__domain_name = domain_name

        # link function containing domain specific enhancement to said domain here
        # 'domain' : self.__enhance_domain_function_name
        # make sure to enter 'self.__enhance_domain_function_name' and not
        # 'self.__enhance_domain_function_name()' as brackets would make this
        # a function call instead of a reference to the function
        self.__function_map = {
            'ehrenamt_hessen': self.__enhance_ehrenamt_hessen,
        }

    def run(self):
        """ run general enhancements and load domainspecific enhancement. """
        print("run for", self.__domain_name)
        self.__run_for_domain(self.__domain_name)
        return self.__data

    def __run_for_domain(self, domain):
        """ run domainspecific enhancement. """
        if domain in self.__function_map:
            self.__function_map[domain]()
        else:
            print(f"Error [enhance_data.py]: No function set for '{domain}'")

    def __enhance_ehrenamt_hessen(self):
        print("ehrenamt_hessen func")
        e_tags.run(self.__data, self.__domain_name)
        self.__data = e_location.add_map_address(self.__data)
        return self.__data

    def enhance_gute_tat(self):
        # dummy call gute tat enhance
        return self.__data
