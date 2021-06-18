import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ['ROOT_DIR'] = ROOT_DIR

from upload_to_elasticsearch.elastic import run_elastic_upload
from shared.LoggerFactory import LoggerFactory
from data_management.data_manager import DataManager

LoggerFactory.get_elastic_logger().info('running elastic upload')
# starts the process of selecting the files to upload to elastic search
DataManager.run_compose_upload_process()
# execute the upload to elastic search
run_elastic_upload()
