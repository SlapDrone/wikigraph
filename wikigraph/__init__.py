from dotenv import load_dotenv

from wikigraph.config import get_settings
from wikigraph.logger import setup_logging

load_dotenv(".env")
settings = get_settings()
setup_logging(settings=settings)