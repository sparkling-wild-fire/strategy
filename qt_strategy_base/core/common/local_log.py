# -- coding: utf-8 --
import logging
import logging.config
import logging.handlers
import os

from qt_strategy_base.common.singleton import singleton


@singleton
class Logger:
    def __init__(self):
        self._logger = None
        self._logger_level_int = 0

    def init(self, logger_name, file_name, path, logger_level):
        if not os.path.exists(os.path.join(path, "log")):
            os.makedirs(os.path.join(path, "log"))
        log_path = os.path.join(path, "log", file_name)

        if logger_level == "0":
            self._logger_level_int = int(logger_level)
            logger_level = "DEBUG"

        elif logger_level == "1":
            self._logger_level_int = int(logger_level)
            logger_level = "INFO"

        elif logger_level == "2":
            self._logger_level_int = int(logger_level)
            logger_level = "WARNING"

        elif logger_level == "3":
            self._logger_level_int = int(logger_level)
            logger_level = "INFO"

        else:
            self._logger_level_int = 0
            logger_level = "INFO"

        # 创建一个logger
        self._logger = logging.getLogger(name=logger_name)
        self._logger.setLevel(logger_level)
        formatter = logging.Formatter('%(asctime)s - %(process)d - %(thread)d - %(message)s')
        file_handler = logging.handlers.RotatingFileHandler(log_path, maxBytes=104857600, backupCount=10,
                                                            encoding="utf-8")
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

    def critical(self, msg):
        if self._logger_level_int == 5:
            self._logger.critical("CRITICAL - " + str(msg))

    def error(self, msg):
        if self._logger_level_int < 5:
            self._logger.error("ERROR - " + str(msg))

    def warning(self, msg):
        if self._logger_level_int < 4:
            self._logger.warning("WARNING - " + str(msg))

    def info(self, msg):
        if self._logger_level_int < 3:
            self._logger.info("INFO - " + str(msg))

    def debug(self, msg):
        if self._logger_level_int < 2:
            self._logger.debug("DEBUG - " + str(msg))


local_logger = Logger()
