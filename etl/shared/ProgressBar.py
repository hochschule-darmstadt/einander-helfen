from threading import Lock
from shared.LoggerFactory import LoggerFactory


class ProgressBar:
    lock = Lock()
    progress_data = dict()
    logger = LoggerFactory.get_general_logger()

    @staticmethod
    def __add_progress_data(key, current, total):
        ProgressBar.logger.debug("__add_progress_data()")

        ProgressBar.lock.acquire()
        try:
            ProgressBar.progress_data[key] = [current, total]

        finally:
            ProgressBar.lock.release()

    @staticmethod
    def register_crawler(name):
        ProgressBar.logger.debug("register_crawler()")
        ProgressBar.lock.acquire()
        try:
            ProgressBar.progress_data[name] = [0, 0]

        finally:
            ProgressBar.lock.release()

    @staticmethod
    def __generate_progress_bar(name, current, total):
        ProgressBar.logger.debug("__generate_progress_bar()")
        description = ""
        if total == 0:
            percentage = 0
            description = "(still fetching pages)"
        else:
            percentage = int(100 * current / total)
            if percentage == 100:
                description = "(finished)"
            else:
                description = f"{percentage}% ({current}/{total})"
        bar = ''.join(['#' * int(percentage / 2)])
        size_bar_missing = 50 - len(bar)
        bar_missing = ''.join(["-" * size_bar_missing])
        bar = bar + bar_missing
        return f"{name}\t [{bar}] {description}"

    @staticmethod
    def get_progress_data(name, current, total):
        ProgressBar.logger.debug("get_progress_data()")
        ProgressBar.__add_progress_data(name, current, total)
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
                key.ljust(max_len),
                progress_data[key][0],
                progress_data[key][1]
            ))

        progress_bar = bars[0]
        for index in range(1, len(bars)):
            progress_bar = progress_bar + "\n" + bars[index]
        print("\n"+progress_bar)
