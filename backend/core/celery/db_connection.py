import logging

from threading import local

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.settings import settings

from core.database import AsyncSessionLocal, engine

logger = logging.getLogger(__name__)
process_local = local()


def create_engine_for_worker():
    logger.info("Creating a new SQLAlchemy engine for worker process")
    process_local.engine = engine
    process_local.Session = AsyncSessionLocal
    return engine


def dispose_engine():
    if hasattr(process_local, 'engine'):
        logger.info("Disposing SQLAlchemy engine for worker process")
        process_local.engine.dispose()
        del process_local.engine
        del process_local.Session


def get_engine():
    if hasattr(process_local, 'engine'):
        return process_local.engine
    return engine
