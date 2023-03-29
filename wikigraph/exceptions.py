"""
 Module recording possible exceptions for the application,
 with hooks to ensure standardized logging

 For more information on application exceptions see:
  - https://salvetech.atlassian.net/wiki/spaces/CMAI/pages
  /2661023745/Image+classifier+annotation+Exceptions
"""
from abc import ABCMeta, abstractmethod
from enum import Enum, auto
import logging 
from typing import Optional

from wikigraph.logger import LoggingExtra, get_logger


logger = get_logger(__name__)


class Severity(Enum):
    """Types of logging severity"""

    # pylint: disable=invalid-name
    exception = auto()
    warning = auto()
    info = auto()


class BaseResult(Exception, metaclass=ABCMeta):
    """Abstract class used to control process flow"""

    @property
    @abstractmethod
    def is_error(self):
        """Boolean flag to indicate whether the result an exception or success"""
        return NotImplementedError

    @property
    @abstractmethod
    def is_full_failure(self) -> Optional[bool]:
        """
        Boolean to indicate whether this exception causes the application to terminate.

        A missing value (uncaught exception) means this exception can either be for full
        application failure, or just for one specific file
        """
        return NotImplementedError

    @property
    @abstractmethod
    def is_transient(self):
        """Determines if an exception is transient to inform error retry"""
        return NotImplementedError

    @property
    @abstractmethod
    def log_code(self):
        """Code used for logging purposes & standardisation"""
        return NotImplementedError

    @property
    @abstractmethod
    def level(self):
        """Severity used for logging purposes"""
        return NotImplementedError

    def message(self) -> str:
        """Get the exception message inheriting
        from the docstring and initialisation message
        """
        return self.__doc__ + (f": {self}" if str(self) else "")

    def log(self, logging_extra: Optional[LoggingExtra] = None):
        """Log the result appropriately"""
        extra = {} if logging_extra is None else logging_extra.format()

        extra["logCode"] = self.log_code

        if self.level == Severity.exception:
            logger.exception(msg=self.message(), extra=extra)

        if self.level == Severity.warning:
            logger.warning(msg=self.message(), extra=extra)

        if self.level == Severity.info:
            logger.info(msg=self.message(), extra=extra)


# Exceptions common between the two applications
class UncaughtException(BaseResult):
    """Uncaught exception"""

    is_error = True
    is_full_failure = None
    is_transient = False
    log_code = "WIKIGRAPH-U000"
    level = Severity.exception


class NoFilesFoundException(BaseResult):
    """No files found at specified location."""

    is_error = True
    is_full_failure = True
    is_transient = False
    log_code = "WIKIGRAPH-F000"
    level = Severity.exception


# wikigraph/exceptions.py
class WikigraphError(Exception):
    """Base exception class for the wikigraph package."""


class DataFetchError(WikigraphError):
    """Raised when there's an error while fetching data from Wikipedia or Wikidata."""


class DataProcessingError(WikigraphError):
    """Raised when there's an issue processing the fetched data."""


class DatabaseConnectionError(WikigraphError):
    """Raised when there's an error connecting to the Neo4j database."""


class DatabaseInsertionError(WikigraphError):
    """Raised when there's an error inserting data into the Neo4j database."""
