import hashlib
import json
import os
import time

from elasticsearch import Elasticsearch

from shared.utils import read_data_from_json
from shared.logger_factory import LoggerFactory

ROOT_DIR = os.environ['ROOT_DIR']
client = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])
logger = LoggerFactory.get_elastic_logger()

index = 'posts'
tmp_index = f'{index}_tmp'

index_configuration = {
    'mappings': {
        'properties': {
           'geo_location': {'type': 'geo_point'},
        }}
}


def run_elastic_upload():
    logger.debug('run_elastic_upload()')
    _create_temp_index()
    _reset_old_index()
    time.sleep(5)  # Timeout is necessary to prevent document loss during reindex
    _reindex_elastic()
    _delete_tmp_index()


def _create_temp_index():
    logger.debug('_create_temp_index()')
    logger.info('Starting temporary Index Process!')

    if client.indices.exists(index=tmp_index):
        client.indices.delete(index=tmp_index, ignore=[400, 404])

    client.indices.create(index=tmp_index, body=index_configuration)
    logger.info('Finished temporary Indexing!')

    for file in os.scandir(os.path.join(ROOT_DIR, 'data_management/upload')):
        logger.info(f'{file.name}: Starting data upload')
        # read enhanced data for indexing
        data = read_data_from_json(file.path)

        # Write enhanced data to Elastic Search
        _write_to_elastic(data)
        logger.info(f'{file.name}: Finished data upload')


def _write_to_elastic(posts):
    logger.debug('_write_to_elastic()')

    ids = []
    for post in posts:
        if post is not None:
            hashed_id = hashlib.md5(post['link'].encode()).hexdigest()
            if hashed_id not in ids:
                client.create(id=hashed_id, index=tmp_index, doc_type='_doc', body=json.dumps(post))
                ids.append(hashed_id)


def _reset_old_index():
    logger.debug('_reset_old_index()')
    logger.info(f'Delete old {index} index')

    if client.indices.exists(index=index):
        client.indices.delete(index=index, ignore=[400, 404])

    client.indices.create(index=index, body=index_configuration)


def _reindex_elastic():
    logger.debug('_reindex_elastic()')
    logger.info('Starting Reindex Process!')

    request_body = {
        'source': {
            'index': tmp_index
        },
        'dest': {
            'index': index
        }
    }
    try:
        result = client.reindex(request_body, wait_for_completion=True, refresh=True, request_timeout=60)

        logger.info(f'Reindex info: {result["total"]} documents reindexed in {result["took"]} milliseconds')
        logger.info(f'Failures: {result["failures"]}')
    except Exception as err:
        logger.exception(str(err))

    logger.info('Finished Reindexing!')


def _delete_tmp_index():
    logger.debug('_delete_tmp_index()')
    logger.info(f'Delete {tmp_index} index')

    if client.indices.exists(index=tmp_index):
        client.indices.delete(index=tmp_index, ignore=[400, 404])
