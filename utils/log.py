import sys
import logging

try:
    from utils import config as c
except Exception, e:
    sys.path.append('../')
    from utils import config as c


class Logger():

    def __init__(self, loggerName='p-geo'):
        """
        Initialize and configure the logger. The logging level and the logger name
        are set in the general.json file stored in the config folder.
        """
        self.config = c.Config('general')
        self.level = 'INFO'
        logging.basicConfig(level=self.config.get('loggingLevel'),
                            format='%(asctime)s | %(levelname)-8s | %(message)s',
                            datefmt='%d-%m-%Y | %H:%M:%s')
        self.logger = logging.getLogger(loggerName)
        self.logger.setLevel(self.level)

    def debug(self, msg):
        """
        Log a message at debug level
        @param msg: The message to be logged.
        """
        self.logger.debug(msg)

    def info(self, msg):
        """
        Log a message at info level
        @param msg: The message to be logged.
        """
        self.logger.info(msg)

    def warn(self, msg):
        """
        Log a message at warn level
        @param msg: The message to be logged.
        """
        self.logger.warn(msg)

    def error(self, msg):
        """
        Log a message at error level
        @param msg: The message to be logged.
        """
        self.logger.error(msg)

    def critical(self, msg):
        """
        Log a message at critical level
        @param msg: The message to be logged.
        """
        self.logger.critical(msg)