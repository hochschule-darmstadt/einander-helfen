from enhancement_duplicates.JsonPost import JsonPost


def remove_duplicates(data):
    """Removes exact duplicates from the json list.
    The URL is ignored in the comparison."""

    posts = []
    duplicates = []

    for date in data:
        posts.append(JsonPost(date))

    for i in range(0, len(posts)):
        for j in range(i + 1, len(posts)):
            if posts[i].json not in duplicates and posts[j].json not in posts:
                if posts[i].mod_json == posts[j].mod_json:
                    duplicates.append(posts[j].json)

    print(f'[INFO]\tFound {len(duplicates)} duplicates')

    for duplicate in duplicates:
        data.remove(duplicate)

    print(f'[INFO]\tRemoved {len(duplicates)} duplicates')
