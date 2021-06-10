from datetime import datetime
from shared.LoggerFactory import LoggerFactory
import json
import os

logger = LoggerFactory.get_general_logger()


def write_data_to_json(path, data):
    """Writes the given data to the given json file."""
    logger.debug(f'write_data_to_json({path})')

    dir_name = os.path.dirname(path)
    if not os.path.exists(dir_name):
        os.makedirs(path)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def read_data_from_json(path):
    """Reads the given json file."""
    logger.debug(f'read_data_from_json({path})')

    if not os.path.exists(path):
        print(f'Enhanced data file does not exist! [{path}]')
    with open(path, 'r', encoding='utf-8') as data_file:
        json_load = json.load(data_file)
    return json_load


def append_data_to_json(path, data):
    """Appends json data to the given json file."""

    if data is not None:
        json_load = read_data_from_json(path)
        json_load.append(data)
        write_data_to_json(path, json_load)

