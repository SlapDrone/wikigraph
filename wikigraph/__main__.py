"""Main entrypoint for the wikigraph module"""
from injector import Injector

from wikigraph import classifier_settings
from wikigraph.driver import main
from wikigraph.log_helper import LogFields, setup_logging


log_fields = LogFields(
    correlation_id=classifier_settings.correlation_id,
    job_id=classifier_settings.job_id,
)

setup_logging(log_fields=log_fields)


injector = Injector()
settings = injector.get(Settings)


main()