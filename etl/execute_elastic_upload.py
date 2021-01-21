import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ['ROOT_DIR'] = ROOT_DIR

from upload_to_elasticsearch.elastic import run_elastic_upload
from shared.LoggerFactory import LoggerFactory
from data_management.DataManager import DataManager

LoggerFactory.get_elastic_logger().info("running elastic upload")
DataManager.run_compose_upload_process()
run_elastic_upload()
