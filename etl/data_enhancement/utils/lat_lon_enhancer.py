from geopy.geocoders import Nominatim
import csv
import time

class LatLonEnhancer:
    dict_file = 'geocoder_lat_lon.csv'

    lat_lon_dict = {}

    def __init__(self):
        self.geolocator = Nominatim(user_agent="einander-helfen.org")
        self.__load_local_storage()

    def enhance(self, object):
        # If object has lat lon: return object
        if None is object['geo_location']:
            request_string = LatLonEnhancer.get_api_request_string(object)

            lat_lon = self.__check_local_storage(request_string)

            if not lat_lon:
                lat_lon = self.__handle_api_requests(request_string)
                if lat_lon:
                    self.__add_new_entry(request_string, lat_lon)

            print("Output:", request_string, lat_lon)
            return lat_lon
        else:
            print("object exists:", object['geo_location'])
            return object['geo_location']

    def __check_local_storage(self, request_string):
        """Already read local storage file?"""
        """return: None if object was not found in local storage, geo_location object otherwise"""

        if request_string in self.lat_lon_dict:
            return self.lat_lon_dict[request_string]
        return None

    def __load_local_storage(self):
        """Reads local storage file (.csv) into class attribute"""

        # Initialize the file, if it is not
        with open(self.dict_file, 'a', newline='') as csvfile:
            if not csvfile.tell():
                fieldnames = ['request', 'lat', 'lon']
                writer = csv.DictWriter(csvfile, fieldnames)
                writer.writeheader()

        # Read the file
        with open(self.dict_file, newline='') as csvfile:
            geocoder_lat_lon = csv.reader(csvfile, delimiter=',')
            for row in geocoder_lat_lon:
                if row and row[0] != 'request':
                    # row[0]: request string, row[1]: lat, row[2]: lon
                    self.lat_lon_dict[row[0]] = {'lat': float(row[1]), 'lon': float(row[2])}

    def __add_new_entry(self, request_string, geo_location):
        """Adds new entry to local storage"""

        self.lat_lon_dict[request_string] = geo_location
        with open(self.dict_file, 'a', newline='') as csvfile:
            fieldnames = ['request', 'lat', 'lon']
            writer = csv.writer(csvfile)

            writer.writerow([request_string, str(geo_location['lat']), str(geo_location['lon'])])

    def __handle_api_requests(self, request_string):
        """Executes the API request"""

        if request_string != "":
            location = self.geolocator.geocode(request_string)

            geo_location = {'lat': location.latitude, 'lon': location.longitude}
            time.sleep(1)

            return geo_location
        return None

    @staticmethod
    def get_api_request_string(post_object):
        """Build the API request string"""

        struct_data = post_object['post_struct']
        request_string = ""

        # Try to build request string from:
        # 1. structured location 2. structured address of contact 3. structured address of organisation
        for field in ['location', 'contact', 'organisation']:
            if len(request_string) < 1 and field in struct_data and struct_data[field] and len(struct_data[field]) > 0:
                request_string += struct_data[field]['street'] + ' ' if 'street' in struct_data[field] else ''
                request_string += struct_data[field]['zipcode'] + ' ' if 'zipcode' in struct_data[field] else ''
                request_string += struct_data[field]['city'] + ' ' if 'city' in struct_data[field] else ''
                request_string += struct_data[field]['country'] + ' ' if 'country' in struct_data[field] else ''

        # TODO: If string is empty at this point, maybe use formatted location

        return request_string.strip()


enhancer = LatLonEnhancer()
enhancer.enhance({
        "title": "\"300 mit Gideon\" - Sozialprojekt und Kinderheim in Brasilien",
        "categories": [
            "International"
        ],
        "location": "Lajeado, Brasilien",
        "task": "<p>Das Projekt \"300 mit Gideon\" hat 2 Kinderheime, ein Durchgangskinderheim und Landwirtschaftsprojekte aufgebaut.  Es ist ein geschützter Lebensraum für zur Zeit 52 Kinder, die in 5 Familien integriert aufwachsen. Die verantwortlichen Ehepaare geben ihr Bestes, um den Mädchen und Jungen ein liebevolles Zuhause zu geben. Die heranwachsenden Kinder können in den missionseigenen Werkstätten und Betriebseinrichtungen Berufe erlernen, werden aber auch extern ausgebildet und während dieser Lehrzeit betreut.\nDarüber hinaus unterstützt das Projekt über 60 Kinder, die noch keinen Platz in den Familien haben und verteilt Nahrung, Kleider und Medikamente an Slumkinder. Daneben ist „Kinder mit Familien“ in der eigenen Schreinerei, in der Landwirtschaft, in der Suppenküche und in Kirchengemeinden aktiv.</p>\n<p>Freiwillige werden je nach Begabung eingesetzt. Möglichkeiten gibt es im handwerklichen Bereich, im gärtnerischen Bereich, in der Landwirtschaft und in einer Wohngruppe im Kinderheim. Bei Letztgenanntem unterstützt der  / die Freiwillige die Erzieher(innen) und Hauptamtlichen, also Betreuung, spielen, malen, Helfen bei der Versorgung usw.</p>",
        "timing": "ab August  | 12 Monate",
        "organization": "Centro Social Trezentos de Gidion",
        "contact": "<p>\nArbeitsgemeinschaft Freiwilligendienste im Bund Freikirchlicher Pfingstgemeinden - Worldwide Volunteers<br/>\nKlaus Poppenberg<br>\nHauptstraße 4<br>78333 Stockach                </br></br></p>\n<p>\n<a class=\"link-standard link-standard--red\" href=\"mailto:info@ww-volunteers.de\">Sende eine E-mail an diese Entsendeorganisation</a><br/>\n</p>",
        "link": "https://www.weltwaerts.de/de/ep-detail.html?id=206947",
        "source": "https://www.weltwaerts.de",
        "geo_location": {
            "lat": -29.4682891,
            "lon": -51.9643648
        },
        "languages": "Portugiesisch",
        "requirements": "Grundlegende Sprachkenntnisse der portugiesischen Sprache sollten vorhanden sein oder vor Antritt des Freiwilligenjahres durch einen Grundkurs erworben werden. Es sollte jemand sein, der ein offener Mensch ist und lernwillig ist. Jemand der sich gern mit Menschen aus anderen Kulturen auseinandersetzt und ihnen helfen will. Teamfähigkeit ist unbedingt notwendig; und natürlich der Wunsch, mit Kindern zu arbeiten.",
        "post_struct": {
            "title": "\"300 mit Gideon\" - Sozialprojekt und Kinderheim in Brasilien",
            "categories": [
                "International"
            ],
            "location": {
                "country": "Brasilien"
            },
            "task": "Das Projekt \"300 mit Gideon\" hat 2 Kinderheime, ein Durchgangskinderheim und Landwirtschaftsprojekte aufgebaut.  Es ist ein geschützter Lebensraum für zur Zeit 52 Kinder, die in 5 Familien integriert aufwachsen. Die verantwortlichen Ehepaare geben ihr Bestes, um den Mädchen und Jungen ein liebevolles Zuhause zu geben. Die heranwachsenden Kinder können in den missionseigenen Werkstätten und Betriebseinrichtungen Berufe erlernen, werden aber auch extern ausgebildet und während dieser Lehrzeit betreut.\nDarüber hinaus unterstützt das Projekt über 60 Kinder, die noch keinen Platz in den Familien haben und verteilt Nahrung, Kleider und Medikamente an Slumkinder. Daneben ist „Kinder mit Familien“ in der eigenen Schreinerei, in der Landwirtschaft, in der Suppenküche und in Kirchengemeinden aktiv.\nFreiwillige werden je nach Begabung eingesetzt. Möglichkeiten gibt es im handwerklichen Bereich, im gärtnerischen Bereich, in der Landwirtschaft und in einer Wohngruppe im Kinderheim. Bei Letztgenanntem unterstützt der  / die Freiwillige die Erzieher(innen) und Hauptamtlichen, also Betreuung, spielen, malen, Helfen bei der Versorgung usw.",
            "timing": "ab August  | 12 Monate",
            "organization": {
                "name": "Centro Social Trezentos de Gidion"
            },
            "contact": {
                "name": "Arbeitsgemeinschaft Freiwilligendienste im Bund Freikirchlicher Pfingstgemeinden - Worldwide Volunteers, Klaus Poppenberg",
                "zipcode": "78333",
                "city": "Stockach",
                "street": "Hauptstraße 4",
                "email": "info@ww-volunteers.de"
            },
            "link": "https://www.weltwaerts.de/de/ep-detail.html?id=206947",
            "source": "https://www.weltwaerts.de",
            "geo_location": {
                "lat": -29.4682891,
                "lon": -51.9643648
            },
            "languages": "Portugiesisch",
            "requirements": "Grundlegende Sprachkenntnisse der portugiesischen Sprache sollten vorhanden sein oder vor Antritt des Freiwilligenjahres durch einen Grundkurs erworben werden. Es sollte jemand sein, der ein offener Mensch ist und lernwillig ist. Jemand der sich gern mit Menschen aus anderen Kulturen auseinandersetzt und ihnen helfen will. Teamfähigkeit ist unbedingt notwendig; und natürlich der Wunsch, mit Kindern zu arbeiten."
        }
    })

enhancer.enhance({
        "title": "1 millión de niños lectores: Bau von innovativen Schulbibliotheken zur Förderung des  Lesens",
        "categories": [
            "International"
        ],
        "location": "Lima - Husares de Junín 650 B, Jesús Maria, Peru",
        "task": "<p>\"Un Millón de Niños Lectores\" (Eine Million lesende Kinder) baut öffentliche Bibliotheken in benachteiligten Schulen in Peru, um das Land vom letzten Platz der Bildungsrankings zu holen und das nationale öffentliche und Schul-Bibliothekensystem zu aktivieren, welches aktuell nicht existiert. Diese Bibliotheken werden aus recyceltem Material von den Familieneltern, externen Freiwilligen und der Privatwirtschaft gebaut, welche ein \"Tool\" der sozialen Transformation darstellen und so zu fähigen BürgerInnen werden, die ihre Rechte einfordern. Im Fokus steht hierbei die Stärkung der Frauen und somit der Familien sowie die Implementierung von Lese-Animationsmethoden und -strategien an den Schulen, mit denen  zusammen gearbeitet wird.</p>\n<p>Der Freiwillige hilft bei der Institutionalisierung der alliierten Bibliotheken im peruanischen Bildungssystem. Er kennt alle Bibliotheken sowie die involvierten Personen (Direktoren, Lehrer, Eltern) und unterstützt bei der Betreuung. Zudem motiviert er direkt die BibliotheksnutzerInnen, d.h. Kinder, Jugendliche und Mütter, die Lektüre zur Gewohnheit zu entwickeln und die Anzahl der monatlich gelesenen Bücher zu erhöhen.\nDer Freiwillige erhält einen Einblick in das Bildungssystem Perus mit all seinen Defiziten und dem Potential von sozial-unternehmerischen Initiativen.</p>",
        "timing": "ab August  | 12 Monate",
        "organization": "Un Millón de Niños Lectores",
        "contact": "<p>\nFachstelle Internationale Freiwilligendienste - Erzdiözese Freiburg<br/>\nClaudia Debes<br>\nOkenstraße 15<br><br/>79108 Freiburg                </br></br></p>\n<p>\n<a class=\"link-standard link-standard--red\" href=\"mailto:fif@kja-freiburg.de\">Sende eine E-mail an diese Entsendeorganisation</a><br/>\n</p>",
        "link": "https://www.weltwaerts.de/de/ep-detail.html?id=213193",
        "source": "https://www.weltwaerts.de",
        "image": "https://www.weltwaerts.de/files/framework/img/ww-logo-de.svg",
        "geo_location": None,
        "languages": "Spanisch",
        "requirements": "Spanischkenntnisse: je mehr, desto besser, mindestens Grundlagen.\nInteresse an Lesen",
        "post_struct": {
            "title": "1 millión de niños lectores: Bau von innovativen Schulbibliotheken zur Förderung des  Lesens",
            "categories": [
                "International"
            ],
            "location": {
                "country": "Peru"
            },
            "task": "\"Un Millón de Niños Lectores\" (Eine Million lesende Kinder) baut öffentliche Bibliotheken in benachteiligten Schulen in Peru, um das Land vom letzten Platz der Bildungsrankings zu holen und das nationale öffentliche und Schul-Bibliothekensystem zu aktivieren, welches aktuell nicht existiert. Diese Bibliotheken werden aus recyceltem Material von den Familieneltern, externen Freiwilligen und der Privatwirtschaft gebaut, welche ein \"Tool\" der sozialen Transformation darstellen und so zu fähigen BürgerInnen werden, die ihre Rechte einfordern. Im Fokus steht hierbei die Stärkung der Frauen und somit der Familien sowie die Implementierung von Lese-Animationsmethoden und -strategien an den Schulen, mit denen  zusammen gearbeitet wird.\nDer Freiwillige hilft bei der Institutionalisierung der alliierten Bibliotheken im peruanischen Bildungssystem. Er kennt alle Bibliotheken sowie die involvierten Personen (Direktoren, Lehrer, Eltern) und unterstützt bei der Betreuung. Zudem motiviert er direkt die BibliotheksnutzerInnen, d.h. Kinder, Jugendliche und Mütter, die Lektüre zur Gewohnheit zu entwickeln und die Anzahl der monatlich gelesenen Bücher zu erhöhen.\nDer Freiwillige erhält einen Einblick in das Bildungssystem Perus mit all seinen Defiziten und dem Potential von sozial-unternehmerischen Initiativen.",
            "timing": "ab August  | 12 Monate",
            "organization": {
                "name": "Un Millón de Niños Lectores"
            },
            "contact": {
                "name": "Fachstelle Internationale Freiwilligendienste - Erzdiözese Freiburg, Claudia Debes",
                "zipcode": "79108",
                "city": "Freiburg",
                "street": "Okenstraße 15",
                "email": "fif@kja-freiburg.de"
            },
            "link": "https://www.weltwaerts.de/de/ep-detail.html?id=213193",
            "source": "https://www.weltwaerts.de",
            "image": "https://www.weltwaerts.de/files/framework/img/ww-logo-de.svg",
            "geo_location": None,
            "languages": "Spanisch",
            "requirements": "Spanischkenntnisse: je mehr, desto besser, mindestens Grundlagen.\nInteresse an Lesen"
        }
    })
enhancer.enhance({
        "title": "1 millión de niños lectores: Bau von innovativen Schulbibliotheken zur Förderung des  Lesens",
        "categories": [
            "International"
        ],
        "location": "Lima - Husares de Junín 650 B, Jesús Maria, Peru",
        "task": "<p>\"Un Millón de Niños Lectores\" (Eine Million lesende Kinder) baut öffentliche Bibliotheken in benachteiligten Schulen in Peru, um das Land vom letzten Platz der Bildungsrankings zu holen und das nationale öffentliche und Schul-Bibliothekensystem zu aktivieren, welches aktuell nicht existiert. Diese Bibliotheken werden aus recyceltem Material von den Familieneltern, externen Freiwilligen und der Privatwirtschaft gebaut, welche ein \"Tool\" der sozialen Transformation darstellen und so zu fähigen BürgerInnen werden, die ihre Rechte einfordern. Im Fokus steht hierbei die Stärkung der Frauen und somit der Familien sowie die Implementierung von Lese-Animationsmethoden und -strategien an den Schulen, mit denen  zusammen gearbeitet wird.</p>\n<p>Der Freiwillige hilft bei der Institutionalisierung der alliierten Bibliotheken im peruanischen Bildungssystem. Er kennt alle Bibliotheken sowie die involvierten Personen (Direktoren, Lehrer, Eltern) und unterstützt bei der Betreuung. Zudem motiviert er direkt die BibliotheksnutzerInnen, d.h. Kinder, Jugendliche und Mütter, die Lektüre zur Gewohnheit zu entwickeln und die Anzahl der monatlich gelesenen Bücher zu erhöhen.\nDer Freiwillige erhält einen Einblick in das Bildungssystem Perus mit all seinen Defiziten und dem Potential von sozial-unternehmerischen Initiativen.</p>",
        "timing": "ab August  | 12 Monate",
        "organization": "Un Millón de Niños Lectores",
        "contact": "<p>\nFachstelle Internationale Freiwilligendienste - Erzdiözese Freiburg<br/>\nClaudia Debes<br>\nOkenstraße 15<br><br/>79108 Freiburg                </br></br></p>\n<p>\n<a class=\"link-standard link-standard--red\" href=\"mailto:fif@kja-freiburg.de\">Sende eine E-mail an diese Entsendeorganisation</a><br/>\n</p>",
        "link": "https://www.weltwaerts.de/de/ep-detail.html?id=213193",
        "source": "https://www.weltwaerts.de",
        "image": "https://www.weltwaerts.de/files/framework/img/ww-logo-de.svg",
        "geo_location": None,
        "languages": "Spanisch",
        "requirements": "Spanischkenntnisse: je mehr, desto besser, mindestens Grundlagen.\nInteresse an Lesen",
        "post_struct": {
            "title": "1 millión de niños lectores: Bau von innovativen Schulbibliotheken zur Förderung des  Lesens",
            "categories": [
                "International"
            ],
            "task": "\"Un Millón de Niños Lectores\" (Eine Million lesende Kinder) baut öffentliche Bibliotheken in benachteiligten Schulen in Peru, um das Land vom letzten Platz der Bildungsrankings zu holen und das nationale öffentliche und Schul-Bibliothekensystem zu aktivieren, welches aktuell nicht existiert. Diese Bibliotheken werden aus recyceltem Material von den Familieneltern, externen Freiwilligen und der Privatwirtschaft gebaut, welche ein \"Tool\" der sozialen Transformation darstellen und so zu fähigen BürgerInnen werden, die ihre Rechte einfordern. Im Fokus steht hierbei die Stärkung der Frauen und somit der Familien sowie die Implementierung von Lese-Animationsmethoden und -strategien an den Schulen, mit denen  zusammen gearbeitet wird.\nDer Freiwillige hilft bei der Institutionalisierung der alliierten Bibliotheken im peruanischen Bildungssystem. Er kennt alle Bibliotheken sowie die involvierten Personen (Direktoren, Lehrer, Eltern) und unterstützt bei der Betreuung. Zudem motiviert er direkt die BibliotheksnutzerInnen, d.h. Kinder, Jugendliche und Mütter, die Lektüre zur Gewohnheit zu entwickeln und die Anzahl der monatlich gelesenen Bücher zu erhöhen.\nDer Freiwillige erhält einen Einblick in das Bildungssystem Perus mit all seinen Defiziten und dem Potential von sozial-unternehmerischen Initiativen.",
            "timing": "ab August  | 12 Monate",
            "organization": {
                "name": "Un Millón de Niños Lectores"
            },
            "contact": {
                "name": "Fachstelle Internationale Freiwilligendienste - Erzdiözese Freiburg, Claudia Debes",
                "zipcode": "79108",
                "city": "Freiburg",
                "street": "Okenstraße 15",
                "email": "fif@kja-freiburg.de"
            },
            "link": "https://www.weltwaerts.de/de/ep-detail.html?id=213193",
            "source": "https://www.weltwaerts.de",
            "image": "https://www.weltwaerts.de/files/framework/img/ww-logo-de.svg",
            "geo_location": None,
            "languages": "Spanisch",
            "requirements": "Spanischkenntnisse: je mehr, desto besser, mindestens Grundlagen.\nInteresse an Lesen"
        }
    })
enhancer.enhance({
        "title": "1 millión de niños lectores: Bau von innovativen Schulbibliotheken zur Förderung des  Lesens",
        "categories": [
            "International"
        ],
        "location": "Lima - Husares de Junín 650 B, Jesús Maria, Peru",
        "task": "<p>\"Un Millón de Niños Lectores\" (Eine Million lesende Kinder) baut öffentliche Bibliotheken in benachteiligten Schulen in Peru, um das Land vom letzten Platz der Bildungsrankings zu holen und das nationale öffentliche und Schul-Bibliothekensystem zu aktivieren, welches aktuell nicht existiert. Diese Bibliotheken werden aus recyceltem Material von den Familieneltern, externen Freiwilligen und der Privatwirtschaft gebaut, welche ein \"Tool\" der sozialen Transformation darstellen und so zu fähigen BürgerInnen werden, die ihre Rechte einfordern. Im Fokus steht hierbei die Stärkung der Frauen und somit der Familien sowie die Implementierung von Lese-Animationsmethoden und -strategien an den Schulen, mit denen  zusammen gearbeitet wird.</p>\n<p>Der Freiwillige hilft bei der Institutionalisierung der alliierten Bibliotheken im peruanischen Bildungssystem. Er kennt alle Bibliotheken sowie die involvierten Personen (Direktoren, Lehrer, Eltern) und unterstützt bei der Betreuung. Zudem motiviert er direkt die BibliotheksnutzerInnen, d.h. Kinder, Jugendliche und Mütter, die Lektüre zur Gewohnheit zu entwickeln und die Anzahl der monatlich gelesenen Bücher zu erhöhen.\nDer Freiwillige erhält einen Einblick in das Bildungssystem Perus mit all seinen Defiziten und dem Potential von sozial-unternehmerischen Initiativen.</p>",
        "timing": "ab August  | 12 Monate",
        "organization": "Un Millón de Niños Lectores",
        "contact": "<p>\nFachstelle Internationale Freiwilligendienste - Erzdiözese Freiburg<br/>\nClaudia Debes<br>\nOkenstraße 15<br><br/>79108 Freiburg                </br></br></p>\n<p>\n<a class=\"link-standard link-standard--red\" href=\"mailto:fif@kja-freiburg.de\">Sende eine E-mail an diese Entsendeorganisation</a><br/>\n</p>",
        "link": "https://www.weltwaerts.de/de/ep-detail.html?id=213193",
        "source": "https://www.weltwaerts.de",
        "image": "https://www.weltwaerts.de/files/framework/img/ww-logo-de.svg",
        "geo_location": None,
        "languages": "Spanisch",
        "requirements": "Spanischkenntnisse: je mehr, desto besser, mindestens Grundlagen.\nInteresse an Lesen",
        "post_struct": {
            "title": "1 millión de niños lectores: Bau von innovativen Schulbibliotheken zur Förderung des  Lesens",
            "categories": [
                "International"
            ],
            "task": "\"Un Millón de Niños Lectores\" (Eine Million lesende Kinder) baut öffentliche Bibliotheken in benachteiligten Schulen in Peru, um das Land vom letzten Platz der Bildungsrankings zu holen und das nationale öffentliche und Schul-Bibliothekensystem zu aktivieren, welches aktuell nicht existiert. Diese Bibliotheken werden aus recyceltem Material von den Familieneltern, externen Freiwilligen und der Privatwirtschaft gebaut, welche ein \"Tool\" der sozialen Transformation darstellen und so zu fähigen BürgerInnen werden, die ihre Rechte einfordern. Im Fokus steht hierbei die Stärkung der Frauen und somit der Familien sowie die Implementierung von Lese-Animationsmethoden und -strategien an den Schulen, mit denen  zusammen gearbeitet wird.\nDer Freiwillige hilft bei der Institutionalisierung der alliierten Bibliotheken im peruanischen Bildungssystem. Er kennt alle Bibliotheken sowie die involvierten Personen (Direktoren, Lehrer, Eltern) und unterstützt bei der Betreuung. Zudem motiviert er direkt die BibliotheksnutzerInnen, d.h. Kinder, Jugendliche und Mütter, die Lektüre zur Gewohnheit zu entwickeln und die Anzahl der monatlich gelesenen Bücher zu erhöhen.\nDer Freiwillige erhält einen Einblick in das Bildungssystem Perus mit all seinen Defiziten und dem Potential von sozial-unternehmerischen Initiativen.",
            "timing": "ab August  | 12 Monate",
            "organization": {
                "name": "Un Millón de Niños Lectores"
            },
            "contact": {

            },
            "link": "https://www.weltwaerts.de/de/ep-detail.html?id=213193",
            "source": "https://www.weltwaerts.de",
            "image": "https://www.weltwaerts.de/files/framework/img/ww-logo-de.svg",
            "geo_location": None,
            "languages": "Spanisch",
            "requirements": "Spanischkenntnisse: je mehr, desto besser, mindestens Grundlagen.\nInteresse an Lesen"
        }
    })