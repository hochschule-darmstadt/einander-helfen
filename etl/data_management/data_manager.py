import os
import time
import datetime
import shutil
from shared.logger_factory import LoggerFactory
from shared.utils import read_data_from_json, write_data_to_json

ROOT_DIR = os.environ['ROOT_DIR']


class DataManager:
    """ Class that collects the enhanced data from the scraping process, manages backups and composes the data that is
     will be uploaded to elasticsearch
     - After the enhancement process, the results are stored in a backup folder named after the time of the backup
     - the upload folder contains the data that will be uploaded to elasticsearch

     For the upload data, the most recent backup data is selected. The amount of posts in the selected dataset is
     compared against older backups according to the value set in fallback_depth. A fallback_depth of 2 means that the
     data from the last 2 backups that are older than the current selected backup is compared with the upload data.
     If the current dataset for the upload contains less than X% of the posts in the backup dataset, where X is the
     defined threshold, the backup dataset is selected instead. This is done on a file by file basis, meaning the
     upload can contain a mixture of files from different backups.

     The source of all files in the upload folder at the end of the process gets logged."""

    # manages how many backups are to be kept. if the number of existing backups would exceed this threshold, the oldest
    # backup gets deleted
    max_number_of_backups = 7

    # manages how many backups into the past should be considered for the upload
    fallback_depth = 3

    # defines the percentage threshold at which data from an older backup may be used. data from an older backup may be
    # used if the current data selected for upload contains less than [threshold] * [number of posts in backup], the
    # data from the backup is selected for upload instead
    threshold = 0.75

    enhanced_data_location = os.path.join(ROOT_DIR, 'data_enhancement/data')
    backup_directory = os.path.join(ROOT_DIR, 'data_management', 'backups')
    upload_directory = os.path.join(ROOT_DIR, 'data_management', 'upload')
    file_upload_data_origin = os.path.join(ROOT_DIR, 'logs', 'upload_data_origin.log')

    mask_timestamp = '%d.%m.%Y'

    logger = LoggerFactory.get_datamanagement_logger()

    data_origin = dict()

    @staticmethod
    def timestamp_to_datestring(timestamp):
        """Converts unix timestamp into datestring"""
        DataManager.logger.debug('timestamp_to_datestring()')

        return datetime.datetime.fromtimestamp(timestamp).strftime(DataManager.mask_timestamp)

    @staticmethod
    def datestring_to_timestamp(datestring):
        """Converts datestring into unix timestamp"""
        DataManager.logger.debug('datestring_to_timestamp()')

        return time.mktime(datetime.datetime.strptime(datestring, DataManager.mask_timestamp).timetuple())

    @staticmethod
    def save_upload_data_origin(upload_data_origin):
        """Saves the information about the origin of the data inside the upload folder into a text file"""
        file = open(DataManager.file_upload_data_origin, 'w', encoding='utf-8')
        file.write(f'last upload: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
        file.write(f'Source for upload data:')
        file.write(upload_data_origin)
        file.close()

    @staticmethod
    def copy_from_backup(backup):
        """Copies all the files from a backup into the upload folder and documents the files origin"""
        DataManager.logger.debug('copy_from_backup()')

        path_backup = os.path.join(DataManager.backup_directory, backup)
        for file in os.listdir(path_backup):
            shutil.copy(os.path.join(path_backup, file), os.path.join(DataManager.upload_directory, file))
            DataManager.data_origin[file] = backup

    @staticmethod
    def backup_current_data():
        """Creates a backup for the data in einander-helfen/etl/data_enhancement/data with current date as timestamp"""
        DataManager.logger.debug('backup_current_data()')

        backup_location = os.path.join(DataManager.backup_directory, DataManager.timestamp_to_datestring(time.time()))

        if os.path.exists(backup_location):
            DataManager.logger.warning('There already exists a backup from today, deleting old backup')
            shutil.rmtree(backup_location)
        os.makedirs(backup_location)

        enhancement_files = os.listdir(DataManager.enhanced_data_location)
        for file in enhancement_files:
            enhancement_file = os.path.join(DataManager.enhanced_data_location, file)
            if os.path.isfile(enhancement_file):
                shutil.copy(enhancement_file,  backup_location)

    @staticmethod
    def get_sorted_list_of_backups():
        """ returns a list containing all the backup folders in a sorted order from old to new"""
        DataManager.logger.debug('get_sorted_list_of_backups()')

        backups = os.listdir(DataManager.backup_directory)
        backup_timestamps = list()
        for folder in backups:
            backup_timestamps.append(DataManager.datestring_to_timestamp(folder))
        backup_timestamps.sort()

        sorted_filenames = list()
        for timestamp in backup_timestamps:
            sorted_filenames.append(DataManager.timestamp_to_datestring(timestamp))
        return sorted_filenames

    @staticmethod
    def remove_old_backups():
        """Checks if the backup folder contains more than the maximum of set backups and deletes surplus"""
        DataManager.logger.debug('remove_old_backups()')

        backups = DataManager.get_sorted_list_of_backups()
        if len(backups) > DataManager.max_number_of_backups:
            DataManager.logger.info(f'More than {DataManager.max_number_of_backups} backups exist({len(backups)})'
                                    f', deleting {len(backups)- DataManager.max_number_of_backups} backup(s)')
            for file in backups[:len(backups)-DataManager.max_number_of_backups]:
                DataManager.logger.info(f'Deleting backup {file}')
                shutil.rmtree(os.path.join(DataManager.backup_directory, file))

    @staticmethod
    def clear_upload():
        """Clears the upload folder as preparation for the fresh upload data"""
        DataManager.logger.debug('clear_upload()')

        shutil.rmtree(DataManager.upload_directory)
        os.makedirs(DataManager.upload_directory)

    @staticmethod
    def get_eligible_backups():
        """Returns list of backups that are eligible as a fallback"""
        DataManager.logger.debug('get_eligible_backups()')

        if len(DataManager.get_sorted_list_of_backups()) < DataManager.fallback_depth:
            DataManager.fallback_depth = len(DataManager.get_sorted_list_of_backups())
        return DataManager.get_sorted_list_of_backups()[-DataManager.fallback_depth-1:]

    @staticmethod
    def initialise_upload_data(backups):
        """Copies files from all backups within fallback depth into upload folder, the most recent backup is the last to
        get copied. As a result, upload now contains all files from the most recent scrape and any additional files
        from older backups within fallback range."""
        DataManager.logger.debug('initialise_upload_data()')

        for backup_folder in backups[-DataManager.fallback_depth-1:]:
            DataManager.copy_from_backup(backup_folder)

    @staticmethod
    def build_string_data_origin():
        """Builds string with summary of which backup files in the upload folder are taken from"""
        DataManager.logger.debug('build_string_data_origin()')

        max_length = 0
        for entry in DataManager.data_origin:
            if len(entry) > max_length:
                max_length = len(entry)
        string_data_origin = ''
        for entry in DataManager.data_origin:
            string_data_origin = string_data_origin+"\n" + \
                                 f'{entry.rjust(max_length)} : {DataManager.data_origin[entry]}'
        return string_data_origin

    @staticmethod
    def compose_upload():
        """Composes the upload according to the general behaviour described for this class and the set parameters"""
        DataManager.logger.debug('compose_upload()')

        DataManager.clear_upload()
        eligible_backups = DataManager.get_eligible_backups()
        DataManager.initialise_upload_data(eligible_backups)
        eligible_backups = eligible_backups[:-1]  # ignore most recent backup

        for backup in eligible_backups:
            for upload_file in os.listdir(DataManager.upload_directory):
                if os.path.isfile(os.path.join(DataManager.backup_directory, backup, upload_file)):
                    data_in_upload = read_data_from_json(os.path.join(DataManager.upload_directory, upload_file))
                    data_in_backup = read_data_from_json(os.path.join(DataManager.backup_directory, backup,
                                                                      upload_file))

                    if len(data_in_upload) < DataManager.threshold*len(data_in_backup):
                        DataManager.logger.info(f'{upload_file} contains less than 75% of the posts in backup '
                                                f'\'{backup}\' ({len(data_in_upload)} posts vs {len(data_in_backup)} '
                                                f'posts). Current data for {upload_file} will be replaced with backup '
                                                f'data')
                        write_data_to_json(os.path.join(DataManager.upload_directory, upload_file), data_in_backup)
                        DataManager.data_origin[upload_file] = backup
        upload_data_origin = DataManager.build_string_data_origin()
        DataManager.save_upload_data_origin(upload_data_origin)
        DataManager.logger.info(f'Source for upload data: {upload_data_origin}')

    @staticmethod
    def init(context):
        """Sets up the required folders and corrects set parameters if needed"""
        DataManager.logger.debug('init()')

        DataManager.enhanced_data_location = DataManager.enhanced_data_location + f'/{context}'
        DataManager.backup_directory = DataManager.backup_directory + f'/{context}'
        DataManager.upload_directory = DataManager.upload_directory + f'/{context}'

        if not os.path.exists(DataManager.backup_directory):
            DataManager.logger.info('Creating backup directory')
            os.makedirs(DataManager.backup_directory)
        if not os.path.exists(DataManager.upload_directory):
            DataManager.logger.info('Creating upload directory')
            os.makedirs(DataManager.upload_directory)

        if DataManager.fallback_depth > DataManager.max_number_of_backups:
            DataManager.logger.warning(f'fallback depth exceeds maximal number of backups ('
                                       f'{DataManager.fallback_depth} > {DataManager.max_number_of_backups}), '
                                       f'fallback depth will be limited to number of backups')
            DataManager.fallback_depth = DataManager.max_number_of_backups

    @staticmethod
    def run_backup_process(context):
        """Runs the datamangement process for creating backups"""
        DataManager.logger.debug('run_backup_process()')

        DataManager.init(context)
        DataManager.backup_current_data()
        DataManager.remove_old_backups()

    @staticmethod
    def run_compose_upload_process(context):
        """Runs the datamangement process for composing the upload"""
        DataManager.logger.debug('run_compose_upload_process()')

        DataManager.init(context)
        DataManager.compose_upload()
