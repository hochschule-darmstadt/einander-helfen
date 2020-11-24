from datetime import datetime
from enum import Enum
import os
from shared.utils import read_data_from_json, write_data_to_json


# Root Directory (/etl)
# ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# os.environ['ROOT_DIR'] = ROOT_DIR


def run():
    start_time = datetime.now()

    posts = get_posts_from_json()

    marked_identical_posts = find_identical_posts(posts)
    #no_identical_posts = remove_duplicated_posts(marked_identical_posts)

    #marked_subsumed_posts = find_subsumed_posts(no_identical_posts)
    marked_subsumed_posts = find_subsumed_posts(marked_identical_posts)
    no_subsumed_posts = remove_duplicated_posts(marked_subsumed_posts)

    marked_fuzzy_duplicates = find_fuzzy_posts(no_subsumed_posts)
    remove_duplicated_posts(marked_fuzzy_duplicates)

    end_time = datetime.now()
    difference = (end_time - start_time).total_seconds()
    print(f'Finding duplicates took {int((difference - (difference % 60)) / 60)}:{difference % 60} minutes')


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
        print(f'Searching for identical posts for "{posts[i].json_post["title"].rstrip()}" [{i + 1}/{len(posts)}]')
        for j in range(i + 1, len(posts)):
            if posts[i].post_type == PostType.DUPLICATE or posts[j].post_type == PostType.DUPLICATE:
                continue
            if posts[i].json_post == posts[j].json_post:
                posts[j].post_type = PostType.DUPLICATE
                print(f'{posts[j].json_post["title"]} is identical to another post')
                duplicate_counter += 1

    print(f'Found {str(duplicate_counter)} identical posts')

    return posts


def find_subsumed_posts(posts):
    duplicate_counter = 0
    for i in range(0, len(posts)):
        print(f'Searching for subsumed posts for "{posts[i].json_post["title"].rstrip()}" [{i + 1}/{len(posts)}]')

        i_str = str(posts[i].json_post).rstrip()
        i_ordered = list(dict.fromkeys(i_str.split()))  # only unique words in alphabetic order
        i_ordered.sort()

        for j in range(i + 1, len(posts)):
            if posts[i].post_type == PostType.DUPLICATE or posts[j].post_type == PostType.DUPLICATE:
                continue

            j_str = str(posts[j].json_post).rstrip()
            j_ordered = list(dict.fromkeys(j_str.split()))
            j_ordered.sort()

            if i_ordered == j_ordered:
                posts[j].post_type = PostType.DUPLICATE
                print(f'{posts[j].json_post["title"]} is identical to another post')
                duplicate_counter += 1

    print(f'Found {str(duplicate_counter)} subsumed posts')

    return posts


def find_fuzzy_posts(posts):
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
        write_data_to_json(os.path.join('/home/janf/git/einander-helfen/etl/', 'data_enhancement/data'), f'{file_name.split(".json")[0]}nd.json', post_files[file_name])  # todo fix path and remove 'nd' from name

    return posts


class PostType(Enum):
    QUALIFIED = 1
    DUPLICATE = 2


class JsonPost:
    def __init__(self, file, json_post):
        self.file = file
        self.json_post = json_post
        self.post_type = PostType.QUALIFIED


"""
def analyse_post_quality(posts):
    best_post = None
    print('> ' + posts[0].score_attrs[0].content.rstrip(), end=':\t')
    for post in posts:
        post.calculate_quality_score()
        print('[' + str(post.quality_score) + '/' + str(post.quality_precise_score) + ']', end='\t')  # todo go on
        if best_post is None:
            best_post = post
        elif post.quality_score > best_post.quality_score:
            best_post = post
        elif post.quality_score == best_post.quality_score and post.quality_precise_score > best_post.quality_precise_score:
            best_post = post

    best_post.post_type = PostType.QUALIFIED
    print('\nQualified: [' + str(best_post.quality_score) + '/' + str(best_post.quality_precise_score) + ']')


class ScoreAttr:
    def __init__(self, content, weighting):
        self.content = content
        self.weighting = weighting

        if content is not None and len(content) > 0:
            self.completeness = 1
            self.length = len(content)
            self.score = self.completeness * weighting
            self.precise_score = self.score * self.length
        else:
            self.completeness = 0
            self.length = 0
            self.score = 0
            self.precise_score = 0


class Post:
    def __init__(self, data_file, post_json):
        self.data_file = data_file
        self.quality_score = 0
        self.quality_precise_score = 0
        self.post_type = PostType.DUPLICATE

        self.score_attrs = [
            ScoreAttr(post_json.get('title').rstrip(), 1),
            ScoreAttr(post_json.get('categories').rstrip(), 1),
            ScoreAttr(post_json.get('location').rstrip(), 1),
            ScoreAttr(post_json.get('task').rstrip(), 1),
            ScoreAttr(post_json.get('target_group').rstrip(), 1),
            ScoreAttr(post_json.get('timing').rstrip(), 1),
            ScoreAttr(post_json.get('effort').rstrip(), 1),
            ScoreAttr(post_json.get('opportunities').rstrip(), 1),
            ScoreAttr(post_json.get('organization').rstrip(), 1),
            ScoreAttr(post_json.get('contact').rstrip(), 1),
            ScoreAttr(post_json.get('link').rstrip(), 1),
            ScoreAttr(post_json.get('image').rstrip(), 1),
            ScoreAttr(post_json.get('map_address').rstrip(), 1),
            ScoreAttr(post_json.get('lat').rstrip(), 1),
            ScoreAttr(post_json.get('lon').rstrip(), 1),
        ]

    def calculate_quality_score(self):
        for attr_score in self.score_attrs:
            self.quality_score += attr_score.score
            self.quality_precise_score += attr_score.precise_score
"""
