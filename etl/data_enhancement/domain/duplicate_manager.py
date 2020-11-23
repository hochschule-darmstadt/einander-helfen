from enum import Enum
import os
from shared.utils import read_data_from_json, write_data_to_json


# Root Directory (/etl)
# ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# os.environ['ROOT_DIR'] = ROOT_DIR


def run():
    post_dict = find_duplicated_posts_by_title()
    for posts in post_dict:
        analyse_post_quality(post_dict[posts])
        # remove_duplicated_posts(posts)


def find_duplicated_posts_by_title():
    grouped_posts = {}
    for file in os.scandir(os.path.join('/home/janf/git/einander-helfen/etl/', 'data_enhancement/data')):
        # read scraped data for enhancement
        json = read_data_from_json(file.path)

        for post in json:
            title = post['title']
            title = title.rstrip()
            if title in grouped_posts:
                grouped_posts[title].append(post)
            else:
                grouped_posts[title] = [post]

    post_dict = {}
    for post_title in grouped_posts:
        if len(grouped_posts[post_title]) <= 1:
            continue

        for post_json in grouped_posts[post_title]:
            post = Post("todo", post_json)
            if post_title in post_dict:
                post_dict[post_title].append(post)
            else:
                post_dict[post_title] = [post]

    return post_dict


def analyse_post_quality(posts):
    best_post = None
    print('> ' + posts[0].attr_scores[0].content.rstrip(), end=':\t')
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


def remove_duplicated_posts(posts):
    # todo
    # in post.data_file remove post where all parameter are equal
    for post in posts:
        if post.post_type == PostType.DUPLICATE:
            pass

    # Write enhanced data to files
    # write_data_to_json(os.path.join(ROOT_DIR, 'data_enhancement/data'), f'{file_name}.json', enhanced_data)
    pass


class PostType(Enum):
    QUALIFIED = 1
    DUPLICATE = 2


class AttrScore:
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

        self.attr_scores = [
            AttrScore(post_json.get('title'), 1),
            AttrScore(post_json.get('categories'), 1),
            AttrScore(post_json.get('location'), 1),
            AttrScore(post_json.get('task'), 1),
            AttrScore(post_json.get('target_group'), 1),
            AttrScore(post_json.get('timing'), 1),
            AttrScore(post_json.get('effort'), 1),
            AttrScore(post_json.get('opportunities'), 1),
            AttrScore(post_json.get('organization'), 1),
            AttrScore(post_json.get('contact'), 1),
            AttrScore(post_json.get('link'), 1),
            AttrScore(post_json.get('image'), 1),
            AttrScore(post_json.get('map_address'), 1),
            AttrScore(post_json.get('lat'), 1),
            AttrScore(post_json.get('lon'), 1),
        ]

    def calculate_quality_score(self):
        for attr_score in self.attr_scores:
            self.quality_score += attr_score.score
            self.quality_precise_score += attr_score.precise_score
