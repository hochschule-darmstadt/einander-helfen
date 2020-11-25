import os
from datetime import datetime

import jellyfish

from data_enhancement.domain.enhancement_duplicates.JsonPost import JsonPost
from data_enhancement.domain.enhancement_duplicates.PostType import PostType
from shared.utils import read_data_from_json, write_data_to_json

# Root Directory (/etl)
# ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# os.environ['ROOT_DIR'] = ROOT_DIR

debug = True
levenshtein_duplicate_rate = 0.01


def run():
    start_time = datetime.now()

    posts = get_posts_from_json()

    marked_identical_posts = find_identical_posts(posts)
    no_identical_posts = remove_duplicated_posts(marked_identical_posts)

    marked_fuzzy_duplicates = find_fuzzy_posts(no_identical_posts)
    remove_duplicated_posts(marked_fuzzy_duplicates)

    end_time = datetime.now()
    difference = (end_time - start_time).total_seconds()
    print(f'[INFO]\tFinding duplicates took {int((difference - (difference % 60)) / 60)}:{difference % 60} minutes')


def get_posts_from_json():
    json_posts = []
    for file in os.scandir(os.path.join('/home/janf/git/einander-helfen/etl/', 'data_enhancement/data')):
        # read scraped data for enhancement
        json_object = read_data_from_json(file.path)
        for json_post in json_object:
            json_posts.append(JsonPost(file, json_post))

    return json_posts


def find_identical_posts(posts):
    duplicate_counter = 0
    for i in range(0, len(posts)):
        if debug:
            print(f'[DEBUG]\t({i + 1}/{len(posts)}) Searching for identical posts for "{posts[i].json_post["title"].rstrip()}"')

        for j in range(i + 1, len(posts)):
            if posts[i].post_type == PostType.DUPLICATE or posts[j].post_type == PostType.DUPLICATE:
                continue
            if posts[i].json_post == posts[j].json_post:
                posts[j].post_type = PostType.DUPLICATE
                print(f'[INFO]\t{posts[j].json_post["title"].rstrip()} is identical to another post')
                duplicate_counter += 1

    print(f'[INFO]\tFound {str(duplicate_counter)} identical posts')

    return posts


def find_fuzzy_posts(posts):
    grouped_by_plz = {}
    duplicate_counter = 0
    for post in posts:
        if post.plz is None:
            continue

        if post.plz in grouped_by_plz:
            grouped_by_plz[post.plz].append(post)
        else:
            grouped_by_plz[post.plz] = [post]

    if debug:
        print(f'[DEBUG]\tFound {len(grouped_by_plz)} different PLZs')
    for plz in grouped_by_plz:
        posts = grouped_by_plz[plz]

        if debug:
            print(f'[DEBUG]\tSearch for fuzzy posts in {plz} ({len(posts)} posts)')

        for i in range(0, len(posts)):
            if debug:
                print(f'[DEBUG]\t({i + 1}/{len(posts)}) Searching for fuzzy posts for "{posts[i].json_post["title"].rstrip()}"')

            for j in range(i + 1, len(posts)):
                if posts[i].post_type == PostType.DUPLICATE or posts[j].post_type == PostType.DUPLICATE:
                    continue
                rate = jellyfish.levenshtein_distance(str(posts[i].fuzzy_json_post_str), str(posts[j].fuzzy_json_post_str)) / (len(posts[i].fuzzy_json_post_str) + len(posts[j].fuzzy_json_post_str))
                if rate < levenshtein_duplicate_rate:
                    posts[j].post_type = PostType.DUPLICATE
                    print(f'[INFO]\t{posts[j].json_post["title"]} is fuzzy to the post {posts[i].json_post["title"].rstrip()}: {rate}')
                    duplicate_counter += 1

    print(f'[INFO]\tFound {str(duplicate_counter)} fuzzy posts')

    return posts


def remove_duplicated_posts(posts):
    post_files = {}
    for post in posts:
        if post.post_type == PostType.QUALIFIED:
            if post.file.name in post_files:
                post_files[post.file.name].append(post.json_post)
            else:
                post_files[post.file.name] = [post.json_post]
        else:
            posts.remove(post)

    for file_name in post_files:
        # Write enhanced data to files
        write_data_to_json(os.path.join('/home/janf/git/einander-helfen/etl/', 'data_enhancement/data_eh'), f'{file_name}', post_files[file_name])

    return posts
