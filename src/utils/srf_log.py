#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import logging.config

logger = logging.getLogger("debug")


def init_log(log_path, log_name, log_level="DEBUG"):
    log_level = log_level.upper()
    LOG_PATH_DEBUG = "%s/%s.log" % (log_path, log_name)
    LOG_PATH_ERROR = "%s/process_server_error.log" % log_path
    LOG_FILE_BACKUP_COUNT = 15

    log_conf = {
        "version": 1,
        "formatters": {
            "format1": {
                "format":
                '%(asctime)-15s [%(thread)d] - [%(filename)s %(lineno)d] %(levelname)s %(message)s',
            },
        },
        "handlers": {
            "handler1": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "level": log_level,
                "formatter": "format1",
                "when": "midnight",
                "backupCount": LOG_FILE_BACKUP_COUNT,
                "filename": LOG_PATH_DEBUG
            },
            "handler2": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "level": 'ERROR',
                "formatter": "format1",
                "when": "midnight",
                "backupCount": LOG_FILE_BACKUP_COUNT,
                "filename": LOG_PATH_ERROR
            },
        },
        "loggers": {
            "debug": {
                "handlers": ["handler1", "handler2"],
                "level": log_level
            },
        }
    }
    logging.config.dictConfig(log_conf)


def close_log():
    logging.shutdown()