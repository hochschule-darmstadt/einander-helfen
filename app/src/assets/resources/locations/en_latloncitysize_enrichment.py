import csv
import requests
import math
import copy


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

    lat = (lat1 + lat2) / 2 * 0.01745
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
    return dx*dy

def write_file(fileName,placeNamePostcodeArray):
    # aggregate places
    alreadySearchedPlaces = []
    placeNamePostcodeArrayForEachCity = []
    placeNamePostcodeArrayForAll = []
    placeNameArray = placeNamePostcodeArray.copy()

    print("adding aggregated places")

    for named_place in placeNameArray:

        #if [named_place.place_name, named_place.state] in alreadySearchedPlaces:
        #    continue

        places = search_all_places_for_place_name(placeNameArray, named_place.place_name, named_place.state)

        aggregatedPlace = PlaceNamePostcode(named_place.osmid,named_place.place_name, named_place.postcode, named_place.state)
        aggregatedPlace.lon = named_place.lon
        aggregatedPlace.lat = named_place.lat
        aggregatedPlace.area = named_place.area

        if len(places) > 1:
            aggregatedPlace.area = float(places[0].area) / len(places)


        placeNamePostcodeArrayForEachCity.append(aggregatedPlace)

        if len(places) > 1 and [named_place.place_name, named_place.state] not in alreadySearchedPlaces:
            aggregatedPlaceAll = copy.deepcopy(aggregatedPlace)
            alreadySearchedPlaces.append([named_place.place_name, named_place.state])
            aggregatedPlaceAll.place_name = named_place.place_name +" (all) "
            aggregatedPlaceAll.area = named_place.area
            # get center location of place
            resp = requests.get(
                'https://nominatim.openstreetmap.org/details?osmtype=R&osmid=%s&format=json' % named_place.osmid)

            respJson = resp.json()

            if 'centroid' in respJson:
                centro_lon = respJson['centroid']['coordinates'][0]
                centro_lat = respJson['centroid']['coordinates'][1]

                print(named_place.place_name + " (all), area: " + str(named_place.area) +
                    ", lat: " + str(centro_lat) + ", lon: " + str(centro_lon))
                aggregatedPlaceAll.lon = centro_lon
                aggregatedPlaceAll.lat = centro_lat

            placeNamePostcodeArrayForAll.append(aggregatedPlaceAll)

    with open(fileName, mode='a', newline='', encoding='utf-8') as csvfile:
        places_writer = csv.writer(csvfile, delimiter=',')
        for named_postcode_place in placeNamePostcodeArrayForEachCity:
            places_writer.writerow([named_postcode_place.place_name, named_postcode_place.postcode,
                                    named_postcode_place.state, named_postcode_place.lat, named_postcode_place.lon,
                                    named_postcode_place.area])

    with open(fileName, mode='a', newline='', encoding='utf-8') as csvfile:
        places_writer = csv.writer(csvfile, delimiter=',')
        for named_postcode_place in placeNamePostcodeArrayForAll:
            places_writer.writerow([named_postcode_place.place_name, named_postcode_place.postcode,
                                    named_postcode_place.state, named_postcode_place.lat, named_postcode_place.lon,
                                    named_postcode_place.area])

    print("wrote all places to file " + fileName)
    
# run for each postcodes in the uszips.csv a requests to osm
# long duration and is only needed if en_plz_ort_state_lat_lon_rank_osm.csv not exist
def write_osm_file():
    # file name of final file
    fileName = './en_plz_ort_state_lat_lon_rank_osm.csv'
    counter =0
    # save all places to csv
    with open(fileName, mode='w', newline='', encoding='utf-8') as csvfile:
        places_writer = csv.writer(csvfile, delimiter=',')
        places_writer.writerow(['osm_id','name', 'plz', 'state', 'lat', 'lon', 'rank'])

    # read place names, postcodes and states from file postcode_placename_state.csv
    with open("uszips.csv", newline='', encoding='utf-8') as csvfile:
        placeNamePostcodeState = csv.reader(csvfile, delimiter=',')
        for row in placeNamePostcodeState:
            if(counter%10==0):
                print(str(counter) +" Entries")
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
                new_place.area = calculate_area_form_osm_bounding_box(respJson[0]['boundingbox'])
            else:
                new_place = PlaceNamePostcode(0, row[3], row[0], row[5])
                # row[1]: lon, row[2]: lat
                new_place.lon = row[1]
                new_place.lat = row[2]
            
            with open(fileName, mode='a', newline='', encoding='utf-8') as csvfilePPS:
                places_writer_pps = csv.writer(csvfilePPS, delimiter=',')
                places_writer_pps.writerow([new_place.osmid,new_place.place_name, new_place.postcode,
                                        new_place.state, new_place.lat, new_place.lon,
                                        new_place.area])
            counter = counter +1
        print("Finished with " +str(counter) +" Entries")


runOSMRequestsearch = False
# run for each postcodes in the uszips.csv a requests to osm
# long duration and is only needed if en_plz_ort_state_lat_lon_rank_osm.csv not exist
if(runOSMRequestsearch):
    write_osm_file()

# file name of final file
fileName = './en_plz_ort_state_lat_lon_rank.csv'
# saves all PlaceNamePostcode objects read from file postcode_placename_state.csv
placeNamePostcodeArray = []

# save all places to csv
with open(fileName, mode='w', newline='', encoding='utf-8') as csvfile:
    places_writer = csv.writer(csvfile, delimiter=',')
    places_writer.writerow(['name', 'plz', 'state', 'lat', 'lon', 'rank'])

# read all entries in csv file
with open("en_plz_ort_state_lat_lon_rank_osm.csv", newline='', encoding='utf-8') as csvfile:
    placeNamePostcodeState = csv.reader(csvfile, delimiter=',')
    skipFirstRow = True
    for row in placeNamePostcodeState:
        
        if skipFirstRow:
            skipFirstRow= False
            continue
        # row[0]: osm ID, row[1]:place_name, row[2]: postcode, row[3]: state, row[4]:lon, row[5]: lat, row[7]: area
        # def __init__(self, osmid, place_name, postcode, state):
        location = PlaceNamePostcode(row[0],row[1], row[2], row[3])
        location.lon = row[4]
        location.lat = row[5]
        location.area = row[6] 
        placeNamePostcodeArray.append(location)

write_file(fileName,placeNamePostcodeArray)
