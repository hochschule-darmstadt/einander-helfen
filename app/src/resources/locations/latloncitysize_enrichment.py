import csv
import requests


class PlaceNamePostcode:
    """Container for a openstreetmap result."""

    def __init__(self, osmid, place_name, postcode, state):
        """Sets all parameter of PlaceNamePostcode."""

        self.osmid = osmid
        self.place_name = place_name
        self.postcode = postcode
        self.state = state
        self.lat = 0.0
        self.lon = 0.0
        self.area = 0.0


class PostcodeLocation:
    """Container for a postcode mapped to his lat and lon."""

    def __init__(self, postcode, lon, lat):
        """Sets all parameter of PostcodeLocation."""

        self.postcode = postcode
        self.lon = lon
        self.lat = lat


class PostcodeArea:
    """Container for a postcode mapped to his area size in square kilometers."""

    def __init__(self, postcode, area):
        """Sets all parameter of PostcodeArea."""

        self.postcode = postcode
        self.area = area


def search_postcode(postcode_array, postcode):
    """Searches an element with a specified postcode attribute in a given array."""

    for element in postcode_array:
        if element.postcode == postcode:
            return element


def search_all_places_for_place_name(place_array, place_name, state):
    """Searches a place with a specified name and state in a given array."""

    all_places = []

    for place in place_array:
        if place.place_name == place_name and place.state == state:
            all_places.append(place)

    return all_places


# file name of final file
fileName = './plz_ort_state_lat_lon_rank.csv'

# saves all PlaceNamePostcode objects read from file postcode_placename_state.csv
placeNamePostcodeArray = []

# saves all PostcodeLocation objects read from file postcode_lat_lon.csv
postcodeLocationArray = []

# saves all PostcodeArea objects read from file postcode_area.csv
postcodeAreaArray = []

# read place names, postcodes and states from file postcode_placename_state.csv
with open('postcode_placename_state.csv', newline='', encoding='utf-8') as csvfile:
    placeNamePostcodeState = csv.reader(csvfile, delimiter=',')
    for row in placeNamePostcodeState:
        # row[1]: place name, row[2]: postcode, row[3]: state
        new_place = PlaceNamePostcode(row[0], row[1], row[2], row[3])
        placeNamePostcodeArray.append(new_place)

# read postcodes, lat and lon from file postcode_lat_lon.csv
with open('postcode_lat_lon.csv', newline='', encoding='utf-8') as csvfile:
    postcodeLocation = csv.reader(csvfile, delimiter='\t')
    for row in postcodeLocation:
        # row[1]: postcode, row[2]: lon, row[3]: lat
        location = PostcodeLocation(row[1], row[2], row[3])
        postcodeLocationArray.append(location)

# read postcode and area from file postcode_area.csv
with open('postcode_area.csv', newline='', encoding='utf-8') as csvfile:
    postcodeArea = csv.reader(csvfile, delimiter=',')
    for row in postcodeArea:
        # row[0]: postcode, row[2]: area in square kilometers
        new_postcode_area = PostcodeArea(row[0], row[2])
        postcodeAreaArray.append(new_postcode_area)

# add lat, lon and area to the PlaceNamePostcode objects
for placeNamePostcode in placeNamePostcodeArray:
    location = search_postcode(postcodeLocationArray, placeNamePostcode.postcode)

    if location is None:
        print("Couldn't find location data for " + placeNamePostcode.place_name + ", trying to query OpenStreetMap..")
        resp = requests.get(
            'https://nominatim.openstreetmap.org/search/?city=%s&country=Germany&postcalcode=%s&state=%s&format=json'
            % (placeNamePostcode.place_name, placeNamePostcode.postcode, placeNamePostcode.state))

        respJson = resp.json()

        if len(respJson) != 0:
            placeNamePostcode.lon = respJson[0]['lon']
            placeNamePostcode.lat = respJson[0]['lat']
            print("Found location data!")
        else:
            print("Couldn't find location for " + placeNamePostcode.place_name)
            placeNamePostcode.lon = 0
            placeNamePostcode.lat = 0
    else:
        placeNamePostcode.lon = location.lon
        placeNamePostcode.lat = location.lat

    postcode_area = search_postcode(postcodeAreaArray, placeNamePostcode.postcode)

    if postcode_area is None:
        print("Couldn't find area for " + placeNamePostcode.place_name)
    else:
        placeNamePostcode.area = postcode_area.area

# aggregate places
alreadySearchedPlaces = []

placeNameArray = placeNamePostcodeArray.copy()

print("adding aggregated places")

for named_place in placeNameArray:

    if [named_place.place_name, named_place.state] in alreadySearchedPlaces:
        continue

    places = search_all_places_for_place_name(placeNameArray, named_place.place_name, named_place.state)

    if len(places) > 1:
        aggregatedPlace = PlaceNamePostcode(
            named_place.osmid, named_place.place_name + " (alle)", named_place.postcode, named_place.state)

        # calculate aggregated area
        calculated_area = 0
        for placeElement in places:
            calculated_area += float(placeElement.area)

        aggregatedPlace.area = calculated_area

        # get center location of place
        resp = requests.get(
            'https://nominatim.openstreetmap.org/details?osmtype=R&osmid=%s&format=json' % named_place.osmid)

        respJson = resp.json()

        if 'centroid' in respJson:
            centro_lon = respJson['centroid']['coordinates'][0]
            centro_lat = respJson['centroid']['coordinates'][1]

            print(named_place.place_name + " (alle), area: " + str(calculated_area) +
                  ", lat: " + str(centro_lat) + ", lon: " + str(centro_lon))
            aggregatedPlace.lon = centro_lon
            aggregatedPlace.lat = centro_lat
        else:
            print("No location for " + named_place.place_name)
            aggregatedPlace.lon = 0
            aggregatedPlace.lat = 0

        placeNamePostcodeArray.append(aggregatedPlace)

    alreadySearchedPlaces.append([named_place.place_name, named_place.state])

# save all places to csv
with open(fileName, mode='w', encoding='utf-8') as csvfile:
    places_writer = csv.writer(csvfile, delimiter=',')
    places_writer.writerow(['name', 'plz', 'state', 'lat', 'lon', 'rank'])
    for named_postcode_place in placeNamePostcodeArray:
        places_writer.writerow([named_postcode_place.place_name, named_postcode_place.postcode,
                                named_postcode_place.state, named_postcode_place.lat, named_postcode_place.lon,
                                named_postcode_place.area])

print("wrote all places to file " + fileName)
