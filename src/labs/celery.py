"""Common Celery configuration

  Either the API or worker should be able to get a handle on the celery
  queue processor and use it to schedule or consume tasks.

"""

from .utils import create_celery_app

app=create_celery_app(include=["labs.tasks"])
