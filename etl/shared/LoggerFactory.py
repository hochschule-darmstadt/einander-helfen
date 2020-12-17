import logging
import os

ROOT_DIR = os.environ['ROOT_DIR']


class LoggerFactory:

    logger_dict = dict()
    # Set levels for display / writing to logfile. Levels are in ascending order:
    # NOTSET
    # DEBUG
    # INFO
    # WARNING
    # ERROR
    # CRITICAL
    display_level = logging.INFO
    logfile_level = logging.DEBUG

    @staticmethod
    def get_logger(name):
        """Returns logger with the set name if it exists, otherwise sets up logger with the requested name.
        default: only WARNING messages or above get displayed, DEBUG-level and above is written to logfile"""

        if name in LoggerFactory.logger_dict:
            return LoggerFactory.logger_dict[name]

        if not os.path.exists(os.path.join(ROOT_DIR, 'logs')):
            os.makedirs(os.path.join(ROOT_DIR, 'logs'))

        # set up general formatting for log messages
        formatter_display = logging.Formatter('%(asctime)s [%(levelname)s]:\t %(message)s', "%Y-%m-%d %H:%M:%S")
        # prettier print and module information for logfile
        formatter_logfile = logging.Formatter('%(asctime)s [%(levelname)s]\n\t\t\t\t\t[%(module)s]:\t %(message)s',
                                              "%Y-%m-%d %H:%M:%S")

        # set up logging to logfile. all levels of messages will be logged to individual files, old contents will be
        # overwritten
        file_handler = logging.FileHandler(os.path.join(ROOT_DIR, 'logs', f'{name}.log'), 'w+')
        file_handler.setFormatter(formatter_logfile)
        file_handler.setLevel(LoggerFactory.logfile_level)

        # set up display of logging messages. only messages of that are at the level of message_level or above will be
        # logged
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter_display)
        stream_handler.setLevel(LoggerFactory.display_level)

        # set up logger and register handlers
        new_logger = logging.getLogger(name)
        # general logging level set to INFO so all messages can be passed on to the handlers
        new_logger.setLevel(logging.DEBUG)
        new_logger.addHandler(file_handler)
        new_logger.addHandler(stream_handler)
        LoggerFactory.logger_dict[name] = new_logger
        return new_logger

    @staticmethod
    def get_general_logger():
        """Returns general logger for overall logging across different modules"""
        return LoggerFactory.get_logger('general_etl')

    @staticmethod
    def get_enhancement_logger():
        """Returns general logger for enhancement modules"""
        return LoggerFactory.get_logger('enhancement')

    @staticmethod
    def get_elastic_logger():
        """Returns general logger for enhancement modules"""
        return LoggerFactory.get_logger('elastic')
