import hashlib
import json
import os

from elasticsearch import Elasticsearch

from shared.utils import read_data_from_json

ROOT_DIR = os.environ['ROOT_DIR']
client = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])


def run_elastic_upload():
    print('[INFO]\tStarting Index Process!')
    index = 'posts'
    if client.indices.exists(index=index):
        client.indices.delete(index=index, ignore=[400, 404])

    request_body = {
        'mappings': {
            'properties': {
                'geo_location': {'type': 'geo_point'},
            }}
    }

    client.indices.create(index=index, body=request_body)
    print('[INFO]\tFinished Indexing!')

    for file in os.scandir(os.path.join(ROOT_DIR, 'data_enhancement/data')):
        print(f'[INFO]\t{file.name}: Starting data upload')
        # read enhanced data for indexing
        data = read_data_from_json(file.path)

        # Write enhanced data to Elastic Search
        write_to_elastic(data, index)
        print(f'[INFO]\t{file.name}: Finished data upload')


def write_to_elastic(posts, index):
    ids = []
    for post in posts:
        if post is not None:
            hashed_id = hashlib.md5(post['link'].encode()).hexdigest()
            if hashed_id not in ids:
                client.create(id=hashed_id, index=index, doc_type='_doc', body=json.dumps(post))
                ids.append(hashed_id)
