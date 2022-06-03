"""Common Celery configuration

  Either the API or worker should be able to get a handle on the celery
  queue processor and use it to schedule or consume tasks.

"""

from celery import Celery

from . import __title__
from .config import config

app=Celery(__title__, broker=config.celery_dsn)