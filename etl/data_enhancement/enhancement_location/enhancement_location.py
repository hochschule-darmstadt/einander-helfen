from shared.LoggerFactory import LoggerFactory

logger = LoggerFactory.get_enhancement_logger()


def add_map_address(data):
    """ dummy function for adding map_adress """
    logger.debug("add_map_address()")

    for post in data:
        post['post_struct']['map_address'] = ''
