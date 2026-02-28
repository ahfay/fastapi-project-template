import logging
from logging.config import dictConfig
import json
from datetime import datetime
import os

LOG_PATH = "./app/logs/app.log"


# Custom JSON formatter
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "line": record.lineno,
            "message": record.getMessage()
        }

        # Add exception info if available
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record)

logging_conf = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": JsonFormatter
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "json",
            "stream": "ext://sys.stdout",
        },
        "rotating_file": {  # This is the handler name
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "json",
            "filename": LOG_PATH,
            "maxBytes": 10485760,  # 10 MB
            "backupCount": 5,
        },
    },
    "loggers": {
        # root logger
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
        # khusus untuk log di code kita
        "app": {
            "handlers": ["rotating_file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

def setup_logging():
    dictConfig(logging_conf)