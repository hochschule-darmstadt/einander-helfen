import csv
import requests

class PlaceNamePostcode:
	def __init__(self, osmid, placeName, postcode, state):
		self.osmid = osmid
		self.placeName = placeName
		self.postcode = postcode
		self.state = state

class PostcodeLocation:
	def __init__(self, postcode, lon, lat):
		self.postcode = postcode
		self.lon = lon
		self.lat = lat

class PostcodeArea:
	def __init__(self, postcode, area):
		self.postcode = postcode
		self.area = area

def searchPostcode(postcodeArray, postcode):
	for element in postcodeArray:
		if (element.postcode == postcode):
			return element

def searchAllPlacesForPlaceName(placeArray, placeName, state):
	allPlaces = []

	for place in placeArray:
		if (place.placeName == placeName and place.state == state):
			allPlaces.append(place)

	return allPlaces

# file name of final file
fileName = '../../../public/files/places_postcode_placename_state_lat_lon_rank.csv'

# saves all PlaceNamePostcode objects read from file postcode_placename_state.csv
placeNamePostcodeArray = []

# saves all PostcodeLocation objects read from file postcode_lat_lon.csv
postcodeLocationArray = []

# saves all PostcodeArea objects read from file postcode_area.csv
postcodeAreaArray = []

# read place names, postcodes and states from file postcode_placename_state.csv
with open('postcode_placename_state.csv', newline='') as csvfile:
	placeNamePostcodeState = csv.reader(csvfile, delimiter=',')
	for row in placeNamePostcodeState:
		# row[1]: place name, row[2]: postcode, row[3]: state
		place = PlaceNamePostcode(row[0], row[1], row[2], row[3])
		placeNamePostcodeArray.append(place)

# read postcodes, lat and lon from file postcode_lat_lon.csv
with open('postcode_lat_lon.csv', newline='') as csvfile:
	postcodeLocation = csv.reader(csvfile, delimiter='\t')
	for row in postcodeLocation:
		# row[1]: postcode, row[2]: lon, row[3]: lat
		location = PostcodeLocation(row[1], row[2], row[3])
		postcodeLocationArray.append(location)

# read postcode and area from file postcode_area.csv
with open('postcode_area.csv', newline='') as csvfile:
	postcodeArea = csv.reader(csvfile, delimiter=',')
	for row in postcodeArea:
		# row[0]: postcode, row[2]: area in square kilometers
		area = PostcodeArea(row[0], row[2])
		postcodeAreaArray.append(area)

# add lat, lon and area to the PlaceNamePostcode objects
for placeNamePostcode in placeNamePostcodeArray:
	location = searchPostcode(postcodeLocationArray, placeNamePostcode.postcode)

	if (location is None):
		print("Couldn't find location data for " + placeNamePostcode.placeName + ", trying to query OpenStreetMap..")
		resp = requests.get(('https://nominatim.openstreetmap.org/search/?city=%s&country=Germany&postcalcode=%s&state=%s&format=json') % (placeNamePostcode.placeName, placeNamePostcode.postcode, placeNamePostcode.state))

		respJson = resp.json()

		if (len(respJson) != 0):
			placeNamePostcode.lon = respJson[0]['lon']
			placeNamePostcode.lat = respJson[0]['lat']
			print("Found location data!")
		else:
			print("Couldn't find location for " + placeNamePostcode.placeName)
			placeNamePostcode.lon = 0
			placeNamePostcode.lat = 0
	else:
		placeNamePostcode.lon = location.lon
		placeNamePostcode.lat = location.lat

	area = searchPostcode(postcodeAreaArray, placeNamePostcode.postcode)

	if (area is None):
		print("Couldn't find area for " + placeNamePostcode.placeName)
	else:
		placeNamePostcode.area = area.area

# aggregate places
alreadySearchedPlaces = []

placeNameArray = placeNamePostcodeArray.copy()

print("adding aggregated places")

for place in placeNameArray:

	if ([place.placeName, place.state] in alreadySearchedPlaces):
		continue

	places = searchAllPlacesForPlaceName(placeNameArray, place.placeName, place.state)

	if (len(places) > 1):
		aggregatedPlace = PlaceNamePostcode(place.osmid, place.placeName + " (alle)", place.postcode, place.state)

		# calculate aggregated area
		area = 0
		for placeElement in places:
			area += float(placeElement.area)

		aggregatedPlace.area = area

		# get center location of place
		resp = requests.get(('https://nominatim.openstreetmap.org/details?osmtype=R&osmid=%s&format=json') % (place.osmid))

		respJson = resp.json()

		if 'centroid' in respJson:
			lon = respJson['centroid']['coordinates'][0]
			lat = respJson['centroid']['coordinates'][1]

			print(place.placeName + " (alle), area: " + str(area) + ", lat: " + str(lat) + ", lon: " + str(lon))
			aggregatedPlace.lon = lon
			aggregatedPlace.lat = lat
		else:
			print("No location for " + place.placeName)
			aggregatedPlace.lon = 0
			aggregatedPlace.lat = 0

		placeNamePostcodeArray.append(aggregatedPlace)

	alreadySearchedPlaces.append([place.placeName, place.state])

# save all places to csv
with open(fileName, mode='w') as csvfile:
		places_writer = csv.writer(csvfile, delimiter=',')
		for place in placeNamePostcodeArray:
			places_writer.writerow([place.placeName, place.postcode, place.state, place.lat, place.lon, place.area])

print("wrote all places to file " + fileName)