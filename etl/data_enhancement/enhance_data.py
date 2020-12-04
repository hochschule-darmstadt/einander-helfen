import os
from shared.utils import write_data_to_json, read_data_from_json
from .enhancement_tags import enhancement_tags as e_tags
from .enhancement_location import enhancement_location as e_location
from .enhancement_location.lat_lon_enhancer import add_lat_lon


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
            'weltwaerts': self.__enhance_weltwaerts,
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
        """ domain specific enhancement for ehrenamtsuche hessen """
        e_tags.run(self.__data, self.__domain_name)
        e_location.add_map_address(self.__data)

    def __enhance_weltwaerts(self):
        """ domain specific enhancement for weltwaerst """
        e_location.add_map_address(self.__data)
        add_lat_lon(self.__data)

    def enhance_gute_tat(self):
        """ domain specific enhancement for gute-tat"""
        # dummy call gute tat enhance
        pass
