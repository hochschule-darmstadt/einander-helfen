import csv
import requests
import math


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


def calculate_area_form_osm_bounding_box(calculate_area_form_osm_boundingbox_array):
    """Calculate area with bounding box values.
        https://www.kompf.de/gps/distcalc.html
    """
    lat1=float(calculate_area_form_osm_boundingbox_array[0])
    lat2=float(calculate_area_form_osm_boundingbox_array[1])
    lon1=float(calculate_area_form_osm_boundingbox_array[2])
    lon2=float(calculate_area_form_osm_boundingbox_array[3])

    lat = (lat1 + lat2) / 2 * 0.0174
    dx = 111.3 * math.cos(lat) * (lon1 - lon2)
    dy = 111.3 * (lat1 - lat2)

    if lat1 < lat2:
        dy = 111.3 * (lat2 - lat1)
    else:
        dy = 111.3 * (lat1 - lat2)

    if lon1 < lon2:
        dx = 111.3 * math.cos(lat) * (lon2 - lon1)
    else:
        dx = 111.3 * math.cos(lat) * (lon1 - lon2)
    #print("BB = Height "+str(dx)+" * Width "+str(dy)+" = "+str(dx*dy))
    return dx*dy

def write_file(fileName,placeNamePostcodeArray, postcodeLocationArray, postcodeAreaArray):
    # add lat, lon and area to the PlaceNamePostcode objects
    for placeNamePostcode in placeNamePostcodeArray:
        location = search_postcode(postcodeLocationArray, placeNamePostcode.postcode)
        
        if location:
            print("Location found data for " + placeNamePostcode.place_name )
            placeNamePostcode.lon = location.lon
            placeNamePostcode.lat = location.lat
        else:
            print("Couldn't find location for " + placeNamePostcode.place_name)
            placeNamePostcode.lon = 0
            placeNamePostcode.lat = 0


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
            aggregatedPlace = PlaceNamePostcode(named_place.osmid, named_place.place_name + " (alle)", named_place.postcode, named_place.state)
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
                aggregatedPlace.lon = named_place.lon
                aggregatedPlace.lat = named_place.lat

            placeNamePostcodeArray.append(aggregatedPlace)

        alreadySearchedPlaces.append([named_place.place_name, named_place.state])
    with open(fileName, mode='a', newline='', encoding='utf-8') as csvfile:
        places_writer = csv.writer(csvfile, delimiter=',')
        for named_postcode_place in placeNamePostcodeArray:
            places_writer.writerow([named_postcode_place.place_name, named_postcode_place.postcode,
                                    named_postcode_place.state, named_postcode_place.lat, named_postcode_place.lon,
                                    named_postcode_place.area])

    print("wrote all places to file " + fileName)
    


# file name of final file
fileName = './en_plz_ort_state_lat_lon_rank2.csv'
postcode_placename_state ='./en_postcode_placename_state2.csv'
modulo_write_count=1500
# saves all PlaceNamePostcode objects read from file postcode_placename_state.csv
placeNamePostcodeArray = []

# saves all PostcodeLocation objects read from file postcode_lat_lon.csv
postcodeLocationArray = []

# saves all PostcodeArea objects read from file postcode_area.csv
postcodeAreaArray = []

# save all places to csv
with open(fileName, mode='w', newline='', encoding='utf-8') as csvfile:
    places_writer = csv.writer(csvfile, delimiter=',')
    places_writer.writerow(['name', 'plz', 'state', 'lat', 'lon', 'rank'])

with open(postcode_placename_state, mode='w', newline='', encoding='utf-8') as csvfilePPS:
    places_writer_pps = csv.writer(csvfilePPS, delimiter=',')

# read place names, postcodes and states from file postcode_placename_state.csv
with open("uszips.csv", newline='', encoding='utf-8') as csvfile:
    placeNamePostcodeState = csv.reader(csvfile, delimiter=',')
    counter=0
    new_place_temp=""
    modulo_write_count_temp=modulo_write_count
    for row in placeNamePostcodeState:
        if(counter%10==0):
            print(str(counter) +" of 33121")
        resp = requests.get(
            'https://nominatim.openstreetmap.org/search/?city=%s&country=USA&postcalcode=%s&state=%s&format=json'
            % (row[3], row[0], row[5]))
        respJson = resp.json()
        if len(respJson) == 0:
            resp = requests.get(
            'https://nominatim.openstreetmap.org/search/?city=%s&country=USA&postcalcode=%s&format=json'
            % (row[3], row[0]))
        respJson = resp.json()
        # row[3]: place name, row[0]: postcode, row[5]: state
        if len(respJson) != 0:
            new_place = PlaceNamePostcode(respJson[0]['osm_id'], row[3], row[0], row[5])
            new_place.lon = respJson[0]['lon']
            new_place.lat = respJson[0]['lat']
            # row[0]: postcode, row[1]: lon, row[2]: lat
            location = PostcodeLocation(row[0], respJson[0]['lon'], respJson[0]['lat'])
            # row[0]: postcode, row[2]: area in square kilometers
            new_postcode_area = PostcodeArea(row[0], calculate_area_form_osm_bounding_box(respJson[0]['boundingbox']))
        else:
            new_place = PlaceNamePostcode(0, row[3], row[0], row[5])
            # row[0]: postcode, row[1]: lon, row[2]: lat
            location = PostcodeLocation(row[0], row[1], row[2])
            # row[0]: postcode, row[2]: area in square kilometers
            new_postcode_area = PostcodeArea(row[0], 0)
        with open(postcode_placename_state, mode='a', newline='', encoding='utf-8') as csvfilePPS:
            places_writer_pps = csv.writer(csvfilePPS, delimiter=',')
            places_writer_pps.writerow([new_place.osmid,new_place.place_name, new_place.postcode,
                                                new_place.state])

        placeNamePostcodeArray.append(new_place)
        postcodeLocationArray.append(location)
        postcodeAreaArray.append(new_postcode_area)
        counter=counter+1

        if(counter%modulo_write_count_temp==0 and new_place.place_name!=new_place_temp):
            write_file(fileName,placeNamePostcodeArray, postcodeLocationArray, postcodeAreaArray)
            # saves all PlaceNamePostcode objects read from file postcode_placename_state.csv
            placeNamePostcodeArray = []
            # saves all PostcodeLocation objects read from file postcode_lat_lon.csv
            postcodeLocationArray = []
            # saves all PostcodeArea objects read from file postcode_area.csv
            postcodeAreaArray = []
            modulo_write_count_temp=modulo_write_count
        elif(counter%modulo_write_count_temp==0 and new_place.place_name==new_place_temp):
            modulo_write_count_temp=modulo_write_count_temp+100

        new_place_temp=new_place.place_name
    write_file(fileName,placeNamePostcodeArray, postcodeLocationArray, postcodeAreaArray)
