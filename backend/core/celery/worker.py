from celery import Celery
from celery.signals import worker_process_init, worker_process_shutdown

from core.settings import settings
from core.logger import configure_logging

from .db_connection import create_engine_for_worker, dispose_engine


@worker_process_init.connect
def init_celery_worker(**kwargs):
    configure_logging()
    create_engine_for_worker()


@worker_process_shutdown.connect
def shutdown_celery_worker(**kwargs):
    dispose_engine()


app = Celery(
    "my_tasks",
    broker=settings.get_redis_url(),
    backend=settings.get_redis_url(),
    include=["tasks.task"],
)

