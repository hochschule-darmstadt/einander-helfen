import csv
import os

from shared.utils import write_data_to_json

ROOT_DIR = os.environ['ROOT_DIR']


def run(data, domain):
    """ calls functions for extracting and ranking tags """
    find_new_tags(data, domain)
    rank_tags(data, domain)


def load_tags_from_file():
    """loads given tags from csv file and returns them in a dict"""
    loaded_tags = {}
    print("load_tags_from_file - path: ",os.path.join(ROOT_DIR,'data_enhancement', 'Tags-einander-helfen.csv'))
    with open(os.path.join(ROOT_DIR, 'data_enhancement','Tags-einander-helfen.csv'), newline='',
              encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            loaded_tags[row['label']] = row['synonyms'].split(',')
    return loaded_tags


def get_synonyms_as_list(values):
    """converts the synonyms to a list"""
    synonyms = []
    for val in values:
        for syn in val:
            synonyms.append(syn.strip())
    return synonyms


def find_new_tags(file,domain):
    """scans categories of crawled data to find tags not existing in the given csv
    writes new found tags to output directory as new_tags.json"""
    loaded_tags = load_tags_from_file()
    synonyms = get_synonyms_as_list(loaded_tags.values())

    new_tags = []
    for post in file:
        for category in post['categories']:
            if category not in loaded_tags.keys() and category not in synonyms:
                new_tags.append(category)
    new_tags = list(set(new_tags))
    write_data_to_json(os.path.join(ROOT_DIR, 'data_enhancement/output'), f"new_tags_{domain}{'.json'}", new_tags)


def rank_tags(file, domain):
    """ranks the tags on count of occurrences in the task field and outputs it to the output file as ranked_tags.json"""
    # todo: find occurrences of synonyms and add to label count,
    #       print to json file in the same format like the tag ontology csv file,
    #       make a new index for the ranked tag ontology for frontend access
    loaded_tags = load_tags_from_file()
    labels = loaded_tags.keys()
    synonyms = get_synonyms_as_list(loaded_tags.values())
    tag_ranking = {}
    for post in file:
        if post['task'] is not None:
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
    write_data_to_json(os.path.join(ROOT_DIR, 'data_enhancement', 'output'),
                       f"ranked_tags_{domain}{'.json'}", tag_ranking)
