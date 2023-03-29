"""
config.py
"""
import logging
from functools import lru_cache
from json import dumps
from os import getenv
from pathlib import Path
from typing import Optional, Tuple
from uuid import uuid4

import pydantic
from pydantic import BaseSettings, Json, validator


# initial logger is default before config loaded
logger = logging.getLogger(__name__)

package_dir = Path(__file__).resolve().parent
repo_dir = package_dir.parent

RELATIONSHIP_TYPES = [
    "P40",   # Child
    "P22",   # Father
    "P25",   # Mother
    "P3373", # Sibling
    "P1038", # Relative
    "P1037", # Employer
    "P106",  # Occupation
    "P108",  # Employer
    "P1347", # Participant of
    "P551",  # Residence
    "P1313", # Position held
    "P1026", # Diplomatic relation
    "P1441", # Present in work
    "P1269", # Facet of
    "P451"  # Romantic partner
]


class Settings(BaseSettings):
    # Configure allowed relationship types for graph construction (Wikidata relations of format "P:XXX")
    relationship_types: list = pydantic.Field(default=RELATIONSHIP_TYPES)
    # configure parameters stable over application lifetime and associated with jobs/runs
    job_id: str = pydantic.Field(default="local_job")
    correlation_id: str = pydantic.Field(default="local_corr")
    # worker settings
    num_workers: int
    items_per_worker: int
    # Database details
    neo4j_uri: pydantic.AnyUrl
    neo4j_user: str
    neo4j_password: str
    # GCP details
    gcp_access_key_id: str = pydantic.Field(default="")
    gcp_secret_access_key: str = pydantic.Field(default="")
    # debug/testing
    log_level: Optional[str] = pydantic.Field(default="INFO")
    testing: Optional[bool] = pydantic.Field(default=False)

    # TODO: More config validation in the pydantic base classes
    @validator("gcp_access_key_id")
    def check_id_not_empty(cls, value):  # pylint: disable=E0213,R0201
        """Validate an GCP key ID has been passed"""
        if not value:
            logger.warning("Missing GCP_ACCESS_KEY_ID env var.")
        return value

    @validator("gcp_secret_access_key")
    def check_secret_not_empty(cls, value):  # pylint: disable=E0213,R0201
        """Validate a GCP secret has been passed"""
        if not value:
            logger.warning("Missing GCP_SECRET_ACCESS_KEY env var.")
        return value


@lru_cache()
def get_settings() -> Settings:
    try:
        settings = Settings()
        logger = get_logger(__name__, settings=settings)
        logger.info("Settings loaded successfully.")
    except Exception as e:
        logger = get_logger(__name__)
        logger.error("Error loading settings: %s", e)
        raise

    return settings
