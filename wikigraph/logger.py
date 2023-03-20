"""Module to configure logging handlers, filters and levels
in the application entrypoint
"""
import logging
import pydantic
import typing as ty
from injector import Injector

from pythonjsonlogger.jsonlogger import JsonFormatter

from wikigraph import Settings


class LogFields(pydantic.BaseModel):
    """Standard fields present with each log, passed via the record filter"""
    correlation_id: str
    job_id: str

class LoggingExtra(pydantic.BaseModel):
    """Config to pass to a logger's extra parameter"""
    limit: Optional[int] = None
    offset: Optional[int] = None



class AppFilter(Filter):
    """
    Class that can act on a log handler to filter all records passed to the handle
    and add fields that should be present in all logs
    """

    def __init__(
        self,
        correlation_id: str,
        job_id: str,
        *args,
        **kwargs
    ):
        self.correlation_id = correlation_id
        self.job_id = job_id

        super().__init__(*args, **kwargs)

    def filter(self, record) -> bool:
        """Impose relevant fields on records"""
        record.correlationId = self.correlation_id
        record.jobId = self.job_id
        record.component = "wikigraph-crawler"

        return True


def get_log_handlers(log_fields) -> List[Handler]:
    """
    Define and format logging handlers to use in the app
    Logs are read into CloudWatch via stdout/stderr (StreamHandler).
    """
    # pylint: disable=redefined-builtin
    format = (
        "[%(asctime)s] %(levelname)s <%(correlationId)s> "
        "[%(name)s.%(funcName)s:%(lineno)d] %(message)s"
    )
    datefmt = "%Y-%m-%dT%H:%M:%S"

    # TODO: I've added a filehander log for now, but we may want to remove
    simple_formatter = logging.Formatter(format, datefmt)
    log_file_path = Path("./logs/classifier.log"); log_file_path.parent.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(simple_formatter)

    json_formatter = JsonFormatter(
        format, datefmt, rename_fields={"asctime": "timestamp", "levelname": "level"}
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(json_formatter)

    app_filter = AppFilter(
        correlation_id=log_fields.correlation_id,
        job_id=log_fields.job_id,
    )
    stream_handler.addFilter(app_filter)
    file_handler.addFilter(app_filter)

    return [handler for handler in [file_handler, stream_handler] if handler]


def setup_logging(
    log_fields: LogFields,
    log_level: str
):
    """
    Configures logging with a chosen formatter.
    """
    handlers = get_log_handlers(log_fields=log_fields)

    # Pass handlers and level back to the root logger
    root.handlers = handlers
    root.setLevel(log_level)

    # pylint: disable=no-member
    for name in root.manager.loggerDict.keys():
        logger = getLogger(name)
        logger.handlers = []
        logger.propagate = True

    # Overrides for module specific loggers
    modules = {
        "tensorflow": ERROR,
        "absl": ERROR,
        "botocore": WARNING,
        "s3transfer": WARNING,
        "urllib3": WARNING,
    }
    for name, level in modules.items():
        logger = logging.getLogger(name)
        logger.handlers = []
        logger.setLevel(level)
        logger.propagate = True



# TODO: fix this.
# LOG_LEVEL = logging.getLevelName(settings.log_level)
# log_fields = LogFields(
#     correlation_id=classifier_settings.correlation_id,
#     job_id=classifier_settings.job_id,
# )

# setup_logging(log_fields=log_fields)

# injector = Injector()
# settings = injector.get(Settings)

# def get_logger(name: str):
#     return logging.getLogger(name)