"""
 Module recording possible exceptions for the application,
 with hooks to ensure standardized logging

 For more information on application exceptions see:
  - https://salvetech.atlassian.net/wiki/spaces/CMAI/pages
  /2661023745/Image+classifier+annotation+Exceptions
"""
from abc import ABCMeta, abstractmethod
from enum import Enum, auto
from logging import getLogger
from typing import Optional

from wikigraph.log_helper import LoggingExtra


logger = getLogger(__name__)


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
    log_code = "ANNOTATE-CLASSIFY-U000"
    level = Severity.exception


class NoFilesFoundException(BaseResult):
    """No files found at specified location."""

    is_error = True
    is_full_failure = True
    is_transient = False
    log_code = "ANNOTATE-CLASSIFY-F000"
    level = Severity.exception


class DataDirectoryNotFoundException(BaseResult):
    """Specified data path doesn't exist."""

    is_error = True
    is_full_failure = True
    is_transient = False
    log_code = "ANNOTATE-CLASSIFY-F001"
    level = Severity.exception


class ExtractionFailedException(BaseResult):
    """No files found after extraction."""

    is_error = True
    is_full_failure = True
    is_transient = False
    log_code = "ANNOTATE-CLASSIFY-F002"
    level = Severity.exception


class UploadToS3Exception(BaseResult):
    """Failed to upload files to S3."""

    is_error = True
    is_full_failure = True
    is_transient = True
    log_code = "ANNOTATE-CLASSIFY-F003"
    level = Severity.exception


class InvalidWellFileException(BaseResult):
    """Invalid well file provided."""

    is_error = True
    is_full_failure = False
    is_transient = False
    log_code = "ANNOTATE-CLASSIFY-E000"
    level = Severity.exception


# Exceptions just for classification
class NoDatasetsProducedException(BaseResult):
    """Failed to produce any datasets after stacking."""

    is_error = True
    is_full_failure = True
    is_transient = False
    log_code = "CLASSIFY-F000"
    level = Severity.exception


class EmptyDatasetException(BaseResult):
    """All images have been removed."""

    is_error = True
    is_full_failure = False
    is_transient = False
    log_code = "CLASSIFY-E000"
    level = Severity.exception


class MissingMetadataException(BaseResult):
    """Incomplete embryo metadata."""

    is_error = True
    is_full_failure = False
    is_transient = False
    log_code = "CLASSIFY-E001"
    level = Severity.exception


class ImageLoadingException(BaseResult):
    """Error in loading image."""

    is_error = True
    is_full_failure = False
    is_transient = False
    log_code = "CLASSIFY-E002"
    level = Severity.exception


class AmbiguousMetadataException(BaseResult):
    """Ambiguous embryo metadata."""

    is_error = True
    is_full_failure = False
    is_transient = False
    log_code = "CLASSIFY-E003"
    level = Severity.exception
