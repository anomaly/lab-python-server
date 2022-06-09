"""Utility functions shared across the app

"""


def create_celery_app(include=None):
    """Create a Celery app
    
    If an array of packages if provided then we load the tasks
    this is used when the worker is started.

    Otherwise we return a connection to the broker to delay
    or schedule tasks.
    """
    from celery import Celery

    from . import __title__
    from .config import config

    app = Celery(__title__, broker=config.redis_dsn)
    app.autodiscover_tasks()

    if include:
        app.conf.update(include=include)

    return app


def create_fluentbit_logger():
    """ Configures a Fluentd sender that should be made available
    in the Docker-compose or K8s constructed environment.
    """
    from fluent import sender
    from . import __title__

    logger = sender.FluentSender(__title__, 
        host=config.FLUENTD_HOST, 
        port=config.FLUENTD_PORT)

    return logger

