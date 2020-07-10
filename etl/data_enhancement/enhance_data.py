from importlib import import_module

def run(data, domain_name):
    
    load_enhancement_by_file(data, domain_name, 'default')
    load_enhancement_by_file(data, domain_name)

    return data


def load_enhancement_by_file(data, domain_name, file_name=None):
    try:
        if not file_name:
            file_name = domain_name 

        enhancement = import_module(f'data_enhancement.domain.{file_name}')
        enhancement.run(data)
        print(f'Enhanced data from [{domain_name}] with {file_name}.py')
    except Exception as err:
        print(err)
