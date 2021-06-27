import os

from reporting.report_generator import ReportGenerator

ROOT_DIR = os.environ['ROOT_DIR']


class StatsCollector:

    ERROR_TYPE_FETCHING = 'fetching_errors'
    ERROR_TYPE_PARSING = 'parsing_errors'
    ERROR_TYPE_ENHANCEMENT = 'enhancement_errors'

    collectors = {}
    date = None
    timestamps = {
        'crawling_started': None,
        'crawling_ended': None,
        'enhancement_started': None,
        'enhancement_ended': None
    }

    @staticmethod
    def get_stats_collector(name):
        if name in StatsCollector.collectors:
            return StatsCollector.collectors[name]
        StatsCollector.collectors[name] = Stats(name)
        return StatsCollector.collectors[name]

    @staticmethod
    def create_summary():
        rg = ReportGenerator()
        rg.set_stats(StatsCollector.collectors, StatsCollector.timestamps, StatsCollector.date)
        rg.build_report()


class Stats:

    def __init__(self, name):
        self.name = name
        self.timestamps = {
            'crawling_duration': 0,
            'enhancement_duration': 0
        }
        self.crawling_successful = 0
        self.crawling_empty = 0
        self.enhancement_new_tags = 0
        self.enhancement_duplicates = 0
        self.enhancement_missing_coordinates = 0
        self.error_messages = {StatsCollector.ERROR_TYPE_FETCHING: [],
                               StatsCollector.ERROR_TYPE_PARSING: [],
                               StatsCollector.ERROR_TYPE_ENHANCEMENT: []}

    def add_error_message(self, error_type, message):
        if error_type in [StatsCollector.ERROR_TYPE_FETCHING,
                          StatsCollector.ERROR_TYPE_PARSING,
                          StatsCollector.ERROR_TYPE_ENHANCEMENT]:
            self.error_messages[error_type].append(message)

    def inc_crawling_successful(self):
        self.crawling_successful += 1

    def inc_crawling_empty_posts(self):
        self.crawling_empty += 1

    def set_enhancement_new_tags(self, new_tags):
        self.enhancement_new_tags = new_tags

    def set_enhancement_duplicates(self, duplicates):
        self.enhancement_duplicates = duplicates

    def set_crawling_duration(self, duration):
        self.timestamps['crawling_duration'] = duration

    def set_enhancement_duration(self, duration):
        self.timestamps['enhancement_duration'] = duration

    def inc_enhancement_missing_coordinates(self):
        self.enhancement_missing_coordinates += 1
