import os
import sys

# Root Directory (/etl)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ['ROOT_DIR'] = ROOT_DIR

# Adds path of the data extraction modules
sys.path.extend([f'{ROOT_DIR}/data_extraction', f'{ROOT_DIR}/shared'])

from data_enhancement import enhance_data as enhance_data
from data_extraction.scrape_data import run as run_extraction
from shared.utils import write_data_to_json, read_data_from_json
from shared.logger_factory import LoggerFactory
from data_management.data_manager import DataManager


logger = LoggerFactory.get_general_logger()
# Runs the extraction process and writes the scraped data to data_extraction/data directory
run_extraction()

for file in os.scandir(os.path.join(ROOT_DIR, 'data_extraction/data')):
    file_name = os.path.splitext(file.name)[0]
    # read scraped data for enhancement
    data = read_data_from_json(file.path)

    # Enhance data
    enhanced_data = enhance_data.Enhancer(data, file_name).run()

    # Write enhanced data to files
    write_data_to_json(os.path.join(ROOT_DIR, 'data_enhancement/data', f'{file_name}.json'), enhanced_data)

DataManager.run_backup_process()
