import logging

class Color:
   
   DEBUG = '\033[94m'
   INFO = '\033[92m'
   WARNING = '\033[93m'
   ERROR = '\033[91m'
   CRITICAL = '\033[30;41m'
   
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


class Logger:

    def __init__(self, logger_name):
        self.logger = logging.getLogger(logger_name)
        if not self.logger.handlers:
            self.logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

    def debug(self, msg):
        self.logger.debug(f"{Color.DEBUG} {msg}\033[0m")

    def info(self, msg):
        self.logger.info(f"{Color.INFO} {msg}\033[0m")

    def infop(self, msg):
        self.logger.info(f"{Color.CRITICAL} {msg}\033[0m")

    def warning(self, msg):
        self.logger.warning(f"{Color.WARNING} {msg}\033[0m")

    def error(self, msg):
        self.logger.error(f"{Color.ERROR} {msg}\033[0m")

    def critical(self, msg):
        self.logger.critical(f"{Color.CRITICAL} {msg}\033[0m")
