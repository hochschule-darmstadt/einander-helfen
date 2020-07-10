import json
import os


def write_data_to_json(path, file_name, data):
    if not os.path.exists(path):
        os.makedirs(path)

    with open(os.path.join(path, file_name), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def read_data_from_json(path):
    if not os.path.exists(path):
        print(f'Enhanced data file does not exist! [{path}]')
    with open(path, 'r', encoding='utf-8') as data_file:
        json_load = json.load(data_file)
    return json_load

def get_current_timestamp():
    
    from datetime import datetime

    now = datetime.now()
    
    return now.strftime("%Y%m%dT%H%M%S")