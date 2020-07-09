import os

from data_enhancement.enhance_data import run as run_enhancement
from data_extraction.scrape_data import run as run_extraction
from lib.util import write_data_to_json, read_data_from_json
from upload_to_elasticsearch.elastic import write_to_elastic

SRC_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/src'

scraped_data = run_extraction()

for file_name, data in scraped_data.items():
    # Write scraped data to files
    write_data_to_json(f'{SRC_PATH}/data_extraction/data', f'{file_name}.json', data)

for file in os.scandir(f'{SRC_PATH}/data_extraction/data'):
    # read scraped data for enhancement
    data = read_data_from_json(file.path)

    # Enhance data
    enhanced_data = run_enhancement(data, os.path.splitext(file.name)[0])

    # Write enhanced data to files
    write_data_to_json(f'{SRC_PATH}/data_enhancement/data', file.name, enhanced_data)

for file in os.scandir(f'{SRC_PATH}/data_enhancement/data'):
    # read enhanced data for indexing
    data = read_data_from_json(file.path)

    # Write enhanced data to Elastic Search
    print('Starting Index Process!')
    write_to_elastic(data, 'posts')
    print('Finished Indexing!')
