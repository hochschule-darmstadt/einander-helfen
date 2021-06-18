from data_enhancement.enhancement_duplicates.json_post import JsonPost
from shared.LoggerFactory import LoggerFactory

logger = LoggerFactory.get_enhancement_logger()


def remove_duplicates(data):
    """Removes exact duplicates from the json list.
    The URL is ignored in the comparison."""
    logger.debug('remove_duplicates()')

    posts_by_title = {}
    duplicates = []

    for date in data:
        if date['title'] in posts_by_title:
            posts_by_title[date['title']].append(JsonPost(date))
        else:
            posts_by_title[date['title']] = [JsonPost(date)]

    for title in posts_by_title:
        posts = posts_by_title[title]
        if len(posts) == 1:
            continue
        _one_to_one_comparison(posts, duplicates)

    logger.info(f'Found {len(duplicates)} duplicates')

    for duplicate in duplicates:
        logger.debug(f'\'{duplicate["title"]}\' is a duplicate')
        data.remove(duplicate)

    logger.info(f'Removed {len(duplicates)} duplicates')


def _one_to_one_comparison(posts, duplicates):
    """Makes a one to one comparison between all JsonPosts in a list."""
    logger.debug('_one_to_one_comparison()')

    for i in range(0, len(posts)):
        for j in range(i + 1, len(posts)):
            if posts[i].is_duplicate or posts[j].is_duplicate:
                continue
            if posts[i].mod_json == posts[j].mod_json:
                duplicates.append(posts[j].json)
                posts[j].is_duplicate = True
