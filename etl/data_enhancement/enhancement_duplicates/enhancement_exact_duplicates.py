from data_enhancement.enhancement_duplicates.JsonPost import JsonPost


debug = False


def remove_duplicates(data):
    """Removes exact duplicates from the json list.
    The URL is ignored in the comparison."""

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
        __one_to_one_comparison(posts, duplicates)

    print(f'[INFO]\tFound {len(duplicates)} duplicates')

    for duplicate in duplicates:
        if debug:
            print(f'[DEBUG]\t\'{duplicate["title"]}\' is a duplicate')
        data.remove(duplicate)

    print(f'[INFO]\tRemoved {len(duplicates)} duplicates')


def __one_to_one_comparison(posts, duplicates):
    for i in range(0, len(posts)):
        for j in range(i + 1, len(posts)):
            if posts[i].is_duplicate or posts[j].is_duplicate:
                continue
            if posts[i].mod_json == posts[j].mod_json:
                duplicates.append(posts[j].json)
                posts[j].is_duplicate = True
