import csv
import os

from shared.utils import write_data_to_json
from shared.logger_factory import LoggerFactory
from shared.stats_collector import StatsCollector

ROOT_DIR = os.environ['ROOT_DIR']
logger = LoggerFactory.get_enhancement_logger()


def run(data, domain, context):
    """ calls functions for extracting and ranking tags """
    logger.debug('run()')

    stats = StatsCollector.get_stats_collector(domain)

    new_tags = find_new_tags(data, domain, context)
    if new_tags is not None:
        stats.set_enhancement_new_tags(len(new_tags))

    rank_tags(data, domain, context)


def load_tags_from_file(context):
    """loads given tags from csv file and returns them in a dict"""
    logger.debug('load_tags_from_file()')

    tag_file = f'{context}-Tags-einander-helfen.csv'

    loaded_tags = {}
    logger.debug(f'load_tags_from_file - path: {os.path.join(ROOT_DIR,"data_enhancement", tag_file)}')
    if os.path.exists(os.path.join(ROOT_DIR,"data_enhancement", tag_file)):
        with open(os.path.join(ROOT_DIR, 'data_enhancement', tag_file), newline='',
                encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                if row['synonyms'] is not None:
                    loaded_tags[row['label']] = row['synonyms'].split(',')
                else:
                    loaded_tags[row['label']] = []
    return loaded_tags


def get_synonyms_as_list(values):
    """converts the synonyms to a list"""
    logger.debug('get_synonyms_as_list()')

    synonyms = []
    for val in values:
        for syn in val:
            synonyms.append(syn.strip())
    return synonyms


def find_new_tags(file, domain, context):
    """scans categories of crawled data to find tags not existing in the given csv
    writes new found tags to output directory as new_tags.json"""
    logger.debug('find_new_tags()')

    loaded_tags = load_tags_from_file(context)
    synonyms = get_synonyms_as_list(loaded_tags.values())

    new_tags = []
    for post in file:
        for category in post['categories']:
            if category not in loaded_tags.keys() and category not in synonyms:
                new_tags.append(category)
    new_tags = list(set(new_tags))
    output_path = os.path.join(ROOT_DIR, f'data_enhancement/output/{context}', f'new_tags_{domain}{".json"}')
    write_data_to_json(output_path, new_tags)
    logger.info('Wrote new tags to \'' + output_path + '\'')

    return new_tags


def rank_tags(file, domain, context):
    """ranks the tags on count of occurrences in the task field and outputs it to the output file as ranked_tags.json"""
    # todo: find occurrences of synonyms and add to label count,
    #       print to json file in the same format like the tag ontology csv file,
    #       make a new index for the ranked tag ontology for frontend access
    logger.debug('rank_tags()')

    loaded_tags = load_tags_from_file(context)
    labels = loaded_tags.keys()
    tag_ranking = {}
    for post in file:
        if post['task'] is not None:
            list_of_words = post['task'].split()
            for tag in labels:
                count = list_of_words.count(tag)

                synonyms = loaded_tags[tag]
                for synonym in synonyms:
                    count += list_of_words.count(synonym)

                if count > 0:
                    if not tag_ranking.get(tag):
                        tag_ranking.update({tag: count})
                    else:
                        new_value = int(tag_ranking.get(tag)) + count
                        tag_ranking.update({tag: new_value})
    sorted_tags = sorted(tag_ranking.items(), key=lambda x: x[1], reverse=True)
    tag_ranking = dict(sorted_tags)
    output_path = os.path.join(ROOT_DIR, f'data_enhancement/output/{context}', f'ranked_tags_{domain}{".json"}')
    write_data_to_json(output_path, tag_ranking)
    logger.info('Wrote ranked tags to \'' + output_path + '\'')
