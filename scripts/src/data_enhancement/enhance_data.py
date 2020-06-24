import csv
import os

from lib.util import write_data_to_json

SRC_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run(data):
    print('Starting Enhancement!')
    enhanced_data = add_map_address(data)
    find_new_tags(data)
    rank_tags(data)
    print('Enhancement finished!')
    return enhanced_data


def load_tags_from_file():
    loaded_tags = {}
    with open(os.path.join(os.path.dirname(__file__), 'Tags-einander-helfen.csv'), newline='',
              encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            loaded_tags[row['label']] = row['synonyms'].split(',')
    return loaded_tags


def get_synonyms_as_list(values):
    synonyms = []
    for val in values:
        for syn in val:
            synonyms.append(syn.strip())
    return synonyms


def find_new_tags(file):
    loaded_tags = load_tags_from_file()
    synonyms = get_synonyms_as_list(loaded_tags.values())

    new_tags = []
    for post in file:
        for category in post['categories']:
            if category not in loaded_tags.keys() and category not in synonyms:
                new_tags.append(category)
    new_tags = list(set(new_tags))
    write_data_to_json(f'{SRC_PATH}/data_enhancement/data', 'new_tags.json', new_tags)


def rank_tags(file):
    loaded_tags = load_tags_from_file()
    labels = loaded_tags.keys()
    synonyms = get_synonyms_as_list(loaded_tags.values())
    # todo: find occurrences of synonyms and add to label count
    tag_ranking = {}
    for post in file:
        list_of_words = post['task'].split()
        for tag in labels:
            count = list_of_words.count(tag)
            if count > 0:
                if not tag_ranking.get(tag):
                    tag_ranking.update({tag: count})
                else:
                    new_value = int(tag_ranking.get(tag)) + count
                    tag_ranking.update({tag: new_value})
    sorted_tags = sorted(tag_ranking.items(), key=lambda x: x[1], reverse=True)
    tag_ranking = dict(sorted_tags)
    write_data_to_json(f'{SRC_PATH}/data_enhancement/data', 'ranked_tags.json', tag_ranking)


def add_map_address(file):
    for post in file:
        post['map_address'] = ''
    return file
