from threading import Lock
from shared.LoggerFactory import LoggerFactory


class ProgressBar:
    lock = Lock()
    progress_data = dict()
    logger = LoggerFactory.get_general_logger()
    MODE_FETCHING = "fetching pages"
    MODE_CRAWLING = "crawling"
    MODE_INITIALISING = "initialising"
    PADLENGTH = 25

    @staticmethod
    def __add_progress_data(key, current, total, mode):
        """registers progress data for crawler"""

        ProgressBar.logger.debug("__add_progress_data()")

        ProgressBar.lock.acquire()
        try:
            ProgressBar.progress_data[key] = [current, total, mode]

        finally:
            ProgressBar.lock.release()

    @staticmethod
    def register_crawler(name):
        """ registers crawler without progress data """
        ProgressBar.logger.debug("register_crawler()")

        ProgressBar.lock.acquire()
        try:
            ProgressBar.progress_data[name] = ["0", "0", ProgressBar.MODE_INITIALISING]

        finally:
            ProgressBar.lock.release()

    @staticmethod
    def add_time(name, time):
        """ adds finish time of a crawler to progress data"""
        ProgressBar.logger.debug("add_time()")

        ProgressBar.lock.acquire()
        try:
            ProgressBar.progress_data[name].append(time)

        finally:
            ProgressBar.lock.release()

    @staticmethod
    def __generate_progress_bar(name, current, total, max_len):
        """ generates a progress bar for a single crawler and returns it as a string"""
        ProgressBar.logger.debug("__generate_progress_bar()")

        description = f"{''.ljust(ProgressBar.PADLENGTH)} [{ProgressBar.progress_data[name][2]}]"
        if int(total) == 0:
            percentage = 0
        else:
            percentage = int(100 * int(current) / int(total))
            if percentage == 100:
                if len(ProgressBar.progress_data[name]) == 4:
                    description = f"{ProgressBar.__pad_to_length(percentage,current,total)} [finished after " \
                                  f"{ProgressBar.progress_data[name][3]} seconds]"
                else:
                    description = f"{ProgressBar.__pad_to_length(percentage,current,total)}" \
                                  f" [{ProgressBar.progress_data[name][2]}]"
            else:
                description = f"{ProgressBar.__pad_to_length(percentage,current,total)}" \
                              f" [{ProgressBar.progress_data[name][2]}]"
        bar = ''.join(['#' * int(percentage / 2)])
        size_bar_missing = 50 - len(bar)
        bar_missing = ''.join(["-" * size_bar_missing])
        bar = bar + bar_missing
        return f"{name.ljust(max_len)}\t [{bar}] {description}"

    @staticmethod
    def __pad_to_length(percentage, current, total):
        """ builds padded string for proper mode description alignment"""
        return f"{percentage}% ({current}/{total})".ljust(ProgressBar.PADLENGTH)

    @staticmethod
    def get_progress_data(name, current, total, mode):
        """ updates progress data for crawler and prints complete progress bar"""

        ProgressBar.logger.debug("get_progress_data()")
        ProgressBar.__add_progress_data(name, current, total, mode)
        ProgressBar.lock.acquire()
        try:
            progress_data = ProgressBar.progress_data.copy()
        finally:
            ProgressBar.lock.release()
        max_len = 0
        for key in progress_data:
            if len(key) > max_len:
                max_len = len(key)

        bars = []

        for key in progress_data:
            bars.append(ProgressBar.__generate_progress_bar(
                key,
                progress_data[key][0],
                progress_data[key][1],
                max_len
            ))

        progress_bar = bars[0]
        for index in range(1, len(bars)):
            progress_bar = progress_bar + "\n" + bars[index]
        print("\n"+progress_bar)
