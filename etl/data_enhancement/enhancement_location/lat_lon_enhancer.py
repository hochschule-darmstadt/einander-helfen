from geopy.geocoders import Nominatim
import csv
import time
import os
from shared.LoggerFactory import LoggerFactory


class LatLonEnhancer:
    """Class handling the enhancement of posts by adding geo data."""

    logger = LoggerFactory.get_enhancement_logger()
    dict_file = os.path.join(os.getenv('ROOT_DIR'), 'data_enhancement',
                             'enhancement_location', 'geocoder_lat_lon.csv')
    lat_lon_dict = {}

    def __init__(self):
        """Initializes the enhancer."""
        self.__setup()
        self.geo_locator = Nominatim(user_agent="einander-helfen.org")
        self.__load_local_storage()

    def __setup(self):
        """Checks if the local storage file exists and creates it if it is missing"""
        LatLonEnhancer.logger.debug("__setup()")

        if not os.path.exists(self.dict_file):
            LatLonEnhancer.logger.warn(f"Create missing geocoder_lat_lon.csv as {self.dict_file}")
            open(self.dict_file, "x", encoding='utf-8')

    def enhance(self, post):
        """Adds latitude and longitude to a given post, if both are missing. Returns the enhanced post."""
        LatLonEnhancer.logger.debug("enhance()")

        # If object has lat lon: return object
        if None is post['geo_location']:

            request_string = LatLonEnhancer.get_api_request_string(post)

            lat_lon = self.__check_local_storage(request_string)

            if lat_lon is None:
                LatLonEnhancer.logger.info(f"enhancing lat lon for {post}")
                lat_lon = self.__handle_api_requests(request_string)
                if lat_lon:
                    self.__add_new_entry(request_string, lat_lon)

            post['geo_location'] = lat_lon
            post['post_struct']['geo_location'] = lat_lon

    def __check_local_storage(self, request_string):
        """Checks if local storage contains a result for the query. If it does, the geo_location object is returned.
           Returns None if local storage doesn't contain a result for the request"""
        LatLonEnhancer.logger.debug("__check_local_storage()")

        if request_string in self.lat_lon_dict:
            return self.lat_lon_dict[request_string]
        return None

    def __load_local_storage(self):
        """Reads local storage file (.csv) into class attribute"""
        LatLonEnhancer.logger.debug("__load_local_storage()")

        # Initialize the file, if it is not
        with open(self.dict_file, 'a', newline='', encoding='utf-8') as csvfile:
            if not csvfile.tell():
                fieldnames = ['request', 'lat', 'lon']
                writer = csv.DictWriter(csvfile, fieldnames)
                writer.writeheader()

        # Read the file
        with open(self.dict_file, newline='', encoding='utf-8') as csvfile:
            geocoder_lat_lon = csv.reader(csvfile, delimiter=',')
            for row in geocoder_lat_lon:
                if row and row[0] != 'request':
                    # row[0]: request string, row[1]: lat, row[2]: lon
                    self.lat_lon_dict[row[0]] = {'lat': float(row[1]), 'lon': float(row[2])}

    def __add_new_entry(self, request_string, geo_location):
        """Adds new entry to local storage"""
        LatLonEnhancer.logger.debug("__add_new_entry()")

        self.lat_lon_dict[request_string] = geo_location
        with open(self.dict_file, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([request_string, str(geo_location['lat']), str(geo_location['lon'])])

        LatLonEnhancer.logger.info(f'Added geo location of \'{request_string}\' to the dictionary')

    def __handle_api_requests(self, request_string):
        """Executes the API request"""
        LatLonEnhancer.logger.debug(f"__handle_api_requests({request_string})")

        if request_string != "":
            location = self.geo_locator.geocode(request_string)
            time.sleep(1)

            if location:
                geo_location = {'lat': location.latitude, 'lon': location.longitude}
                return geo_location
        return None

    @staticmethod
    def get_api_request_string(post):
        """Build the API request string"""
        LatLonEnhancer.logger.debug("get_api_request_string()")

        struct_data = post['post_struct']
        request_string = ""

        # Try to build request string from:
        # 1. structured location 2. structured address of contact 3. structured address of organisation
        for field in ['location', 'contact', 'organization']:
            if len(request_string) < 1 and field in struct_data and struct_data[field] and len(struct_data[field]) > 0:
                request_string += struct_data[field]['street'] + ' ' if 'street' in struct_data[field] and \
                                                                        struct_data[field]['street'] else ''
                request_string += struct_data[field]['zipcode'] + ' ' if 'zipcode' in struct_data[field] and \
                                                                         struct_data[field]['zipcode'] else ''
                request_string += struct_data[field]['city'] + ' ' if 'city' in struct_data[field] and \
                                                                      struct_data[field]['city'] else ''
                request_string += struct_data[field]['country'] + ' ' if 'country' in struct_data[field] and \
                                                                         struct_data[field]['country'] else ''
                request_string = request_string.strip()

        return request_string


def add_lat_lon(data):
    """ sets up LatLon Enhancer and runs it for data """
    LatLonEnhancer.logger.debug("add_lat_lon()")

    enhancer = LatLonEnhancer()
    for post in data:
        enhancer.enhance(post)
