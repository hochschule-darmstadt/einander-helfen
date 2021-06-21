import pycountry
import gettext


def translate_english_countries(data):
    """Translates the country names from english to german."""

    german = gettext.translation('iso3166', pycountry.LOCALES_DIR, languages=['de'])
    for post in data:
        if post['post_struct']['location']['country'] is not None:
            post['post_struct']['location']['country'] = german.gettext(post['post_struct']['location']['country'])
