import logging

from sqlalchemy import event

from models import City
from tasks.task import create_weather

logger = logging.getLogger(__name__)


# @event.listens_for(City, 'after_commit')
# def create_weather_event(mapper, connection, target):
#     logger.info(f'City {target.name} created, start pars weather')
#
#     create_weather.delay()
