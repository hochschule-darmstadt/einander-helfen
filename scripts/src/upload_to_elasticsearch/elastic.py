import hashlib
import json

from elasticsearch import Elasticsearch

client = Elasticsearch([{'host': '141.100.60.78', 'port': 9200}])


def write_to_elastic(posts, index):
    if client.indices.exists(index=index):
        client.indices.delete(index=index, ignore=[400, 404])

    request_body = {
        'mappings': {
            'properties': {
                'geo_location': {'type': 'geo_point'},
            }}
    }

    client.indices.create(index=index, body=request_body)
    ids = []
    for post in posts:
        if post is not None:
            hashed_id = hashlib.md5(post['link'].encode()).hexdigest()
            if hashed_id not in ids:
                client.create(id=hashed_id, index=index, doc_type='_doc', body=json.dumps(post))
                ids.append(hashed_id)
