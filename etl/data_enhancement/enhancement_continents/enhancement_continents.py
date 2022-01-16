from shared.logger_factory import LoggerFactory
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


logger = LoggerFactory.get_enhancement_logger()

"""Latitude and longitude regions of the continents."""
north_america1 = Polygon([(90, -168.75), (90, -10), (78.13, -10), (57.5, -37.5), (15, -30), (15, -75), (1.25, -82.5), (1.25, -105), (51, -180), (60, -180), (60, -168.75)])
north_america2 = Polygon([(51, 166.6), (51, 180), (60, 180)])
south_america = Polygon([(1.25, -105), (1.25, -82.5), (15, -75), (15, -30), (-60, -30), (-60, -105)])
europe = Polygon([(90, -10), (90, 77.5), (42.5, 48.8), (42.5, 30), (40.79, 28.81), (41, 29), (40.55, 27.31), (40.40, 26.75), (40.05, 26.36), (39.17, 25.19), (35.46, 27.91), (33, 27.5), (38, 10), (35.42, -10), (28.25, -13), (15, -30), (57.5, -37.5), (78.13, -10)])
africa = Polygon([(15, -30), (28.25, -13), (35.42, -10), (38, 10), (33, 27.5), (31.74, 34.58), (29.540, 34.92), (27.78, 34.46), (11.3, 44.3), (12.5, 52), (-60, 75), (-60, -30)])
australia = Polygon([(-11.88, 110), (-10.27, 140), (-10, 145), (-30, 161.25), (-52.5, 142.5), (-31.88, 110)])
asia1 = Polygon([(90, 77.5), (42.5, 48.8), (42.5, 30), (40.79, 28.81), (41, 29), (40.55, 27.31), (40.4, 26.75), (40.05, 26.36), (39.17, 25.19), (35.46, 27.91), (33, 27.5), (31.74, 34.58), (29.54, 34.92), (27.78, 34.46), (11.3, 44.3), (12.5, 52), (-60, 75), (-60, 110), (-31.88, 110), (-11.88, 110), (-10.27, 140), (33.13, 140), (51, 166.6), (60, 180), (90, 180)])
asia2 = Polygon([(90, -180), (90, -168.75), (60, -168.75), (60, -180)])
antarctica = Polygon([(-60, -180), (-60, 180), (-90, 180), (-90, -180)])

"""Continent names."""
continents = {
    'de': ['Pazifik','Afrika','Australien','Asien','Europa','Nordamerika','Südamerika','Antarktis'],
    'us': ['Pacific','Africa','Australia','Asia','Europe','North America','South America','Antarctica']
}

def geo_location_to_continent(geo_location, context):
    """Return the continent of the country."""
    logger.debug('geo_location_to_continent()')

    point = Point(float(geo_location['lat']), float(geo_location['lon']))

    continent_index = 0
    if africa.contains(point):
        continent_index = 1
    elif australia.contains(point):
        continent_index = 2
    elif asia1.contains(point) or asia2.contains(point):
        continent_index = 3
    elif europe.contains(point):
        continent_index = 4
    elif north_america1.contains(point) or north_america2.contains(point):
        continent_index = 5
    elif south_america.contains(point):
        continent_index = 6
    elif antarctica.contains(point):
        continent_index = 7 

    return continents[context][continent_index]

def add_continent(data, context):
    """Add the continent of the country to the data."""
    logger.debug('add_continent()')

    cnt = 0
    for post in data:
        if post['geo_location'] is not None and ('continent' not in post['post_struct']['location'].keys() or post['post_struct']['location']['continent'] is None):
            post['post_struct']['location']['continent'] = geo_location_to_continent(post['geo_location'], context)
            cnt += 1

    logger.info(f'Added {cnt} continents')
