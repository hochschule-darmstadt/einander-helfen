import os
import sys
import time
import argparse
from datetime import datetime

# Root Directory (/etl)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ['ROOT_DIR'] = ROOT_DIR

# Adds path of the data extraction modules
sys.path.extend([f'{ROOT_DIR}/data_extraction', f'{ROOT_DIR}/shared'])

from data_enhancement import enhance_data as enhance_data
from data_extraction.scrape_data import run as run_extraction
from shared.utils import write_data_to_json, read_data_from_json
from shared.logger_factory import LoggerFactory
from shared.stats_collector import StatsCollector
from data_management.data_manager import DataManager


logger = LoggerFactory.get_general_logger()

parser = argparse.ArgumentParser(prog='main.py')
parser.add_argument('--context', '-c', nargs='?', help='Set the location context')
args = parser.parse_args()

context = 'de'
if args.context is not None:
    context = args.context.lower()

logger.info('Selected location context: ' + args.context)

now = datetime.now()
StatsCollector.date = now.strftime('%Y-%m-%d')
StatsCollector.timestamps['crawling_started'] = now.strftime('%H:%M:%S (%d. %m. %Y)')
# Runs the extraction process and writes the scraped data to data_extraction/data directory
run_extraction(context)

now = datetime.now()
StatsCollector.timestamps['crawling_ended'] = now.strftime('%H:%M:%S (%d. %m. %Y)')
StatsCollector.timestamps['enhancement_started'] = now.strftime('%H:%M:%S (%d. %m. %Y)')

for file in os.scandir(os.path.join(ROOT_DIR, f'data_extraction/data/{context}')):
    file_name = os.path.splitext(file.name)[0]

    stats = StatsCollector.get_stats_collector(file_name)

    # read scraped data for enhancement
    data = read_data_from_json(file.path)

    # Enhance data
    start = time.time()
    enhanced_data = enhance_data.Enhancer(data, file_name, context).run()
    enhance_time = '{:.2f}'.format((time.time() - start))
    stats.set_enhancement_duration(enhance_time)

    # Write enhanced data to files
    write_data_to_json(os.path.join(ROOT_DIR, f'data_enhancement/data/{context}', f'{file_name}.json'), enhanced_data)

now = datetime.now()
StatsCollector.timestamps['enhancement_ended'] = now.strftime('%H:%M:%S (%d. %m. %Y)')

DataManager.run_backup_process(context)

StatsCollector.create_summary()
