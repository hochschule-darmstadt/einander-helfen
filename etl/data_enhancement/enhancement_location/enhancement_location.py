def add_map_address(data):
    for post in data:
        post['post_struct']['map_address'] = ''
        #post['map_address'] = ''
    return data