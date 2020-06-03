import json
import uuid

from elasticsearch import Elasticsearch


class ElasticClient:
    client = None

    def __init__(self):
        # self.client = Elasticsearch([{'host': os.getenv('DB_HOST') or 'elastic', 'port': os.getenv('DB_PORT') or 9200 }])
        self.client = Elasticsearch([{'host': '141.100.60.78', 'port': 9200}])

    def bulk_to_index(self, posts, index):
        if self.client.indices.exists(index=index):
            self.client.indices.delete(index=index, ignore=[400, 404])

        self.client.indices.create(index=index)
        for post in posts:
            if post is not None:
                self.client.create(id=uuid.uuid4(), index=index, doc_type='_doc', body=json.dumps(post))
