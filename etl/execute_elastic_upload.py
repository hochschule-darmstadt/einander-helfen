import os
import argparse

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ['ROOT_DIR'] = ROOT_DIR

from upload_to_elasticsearch.elastic import run_elastic_upload
from shared.logger_factory import LoggerFactory
from data_management.data_manager import DataManager

parser = argparse.ArgumentParser(prog='main.py')
parser.add_argument('--context', '-c', nargs='?', help='Set the location context')
args = parser.parse_args()

context = 'de'
if args.context is not None:
    context = args.context.lower()

LoggerFactory.get_elastic_logger().info('running elastic upload')
# starts the process of selecting the files to upload to elastic search
DataManager.run_compose_upload_process(context)
# execute the upload to elastic search
run_elastic_upload(context)
