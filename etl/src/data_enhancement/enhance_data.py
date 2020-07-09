import os
from importlib import import_module

SRC_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run(data, file_name):
    print('Starting Enhancement!')
    load_enhancement_by_file('default', data)
    load_enhancement_by_file(file_name, data)
    print('Enhancement finished!')
    return data


def load_enhancement_by_file(file_name: str, data):
    try:
        enhancement = import_module(f'data_enhancement.domain.{file_name}')
        enhancement.run(data)
    except Exception as err:
        print(err)
