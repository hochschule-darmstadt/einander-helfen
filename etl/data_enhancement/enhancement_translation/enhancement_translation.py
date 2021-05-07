import pycountry
import gettext

from shared.LoggerFactory import LoggerFactory

logger = LoggerFactory.get_enhancement_logger()


def translate_english_countries(data):
    """Translates the country names from english to german."""
    logger.debug("translate_english_countries()")

    german = gettext.translation('iso3166', pycountry.LOCALES_DIR, languages=['de'])
    for post in data:
        if post['post_struct']['location']['country'] is not None:
            post['post_struct']['location']['country'] = german.gettext(post['post_struct']['location']['country'])
