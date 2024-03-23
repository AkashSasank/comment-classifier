import os
from datetime import date
import logging

from ..configs import get_settings


class Logger:
    """
    Log handler class
    """

    def __init__(self):
        log_message_fmt = '[%(asctime)s.%(msecs).03d] [%(name)s,%(funcName)s:%(linen' \
                          'o)s] [%(levelname)s]  %(message)s  %(pathname)s %(lineno)d'
        log_date_fmt = '%d/%b/%Y %H:%M:%S'
        self.formatter = logging.Formatter(
            fmt=log_message_fmt, datefmt=log_date_fmt)
        logging.basicConfig(level=logging.DEBUG)
        log_root = get_settings().LOG_ROOT
        log_dir = os.path.join(log_root, 'logs')
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        filename = log_dir + '/logs_' + date.today(). \
            strftime("%Y%m%d") + '.log'
        self.handler = logging.FileHandler(filename=filename)
        self.logger_ = logging.getLogger(__name__)

    def get_logger(self):
        self.logger_.addHandler(self.handler)
        self.logger_.handlers[0].setFormatter(self.formatter)
        return self.logger_


logger = Logger().get_logger()
