"""Utility functions shared across the app

"""


def create_celery_app():
    """Create a Celery app

    """
    from celery import Celery

    from . import __title__
    from .config import config

    app=Celery(__title__, broker=config.redis_dsn)

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

