import json
import os

from elasticsearch import Elasticsearch


class ElasticClient:
    client = None

    def __init__(self):
        self.client = Elasticsearch([{'host': os.getenv('DB_HOST') or 'elastic', 'port': os.getenv('DB_PORT') or 9200}])

    def bulk_to_index(self, posts, index):

        if self.client.indices.exists(index=index):
            self.client.indices.delete(index=index, ignore=[400, 404])

        self.client.indices.create(index=index)

        for i in range(len(posts)):
            self.client.create(id=i + 1, index=index, doc_type='_doc', body=json.dumps(posts[i]))
