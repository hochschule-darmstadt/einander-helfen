from geopy.geocoders import Nominatim
import csv


class LatLonEnhancer:

    def __init__(self):
        self.geolocator = Nominatim(user_agent="einander-helfen.org")

    def enhance(self, object):
        # If object has lat lon: return object

        print(object['post_struct']['title'])
        request_string = self.__get_api_request_string(object)

        pass

    def __check_local_storage(self, request_string):
        # Already read local storage file?

        # return: None if object was not found in local storage, geo_location object otherwise
        return None

    def __load_local_storage(self):
        # Reads local storage file (.csv) into class attribute
        pass

    def __add_new_entry(self, request_string, geo_location):
        # Adds new entry to local storage
        pass

    def __handle_api_requests(self, request_string):
        pass

    def __get_api_request_string(self, object):
        return ""


enhancer = LatLonEnhancer()
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
