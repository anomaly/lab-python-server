""" Utility functions shared across the app

"""

from minio import Minio

from .config import config

minio_client = Minio(
    f"{config.S3_ENDPOINT}:{config.S3_PORT}",
    access_key=config.S3_ACCESS_KEY.get_secret_value(),
    secret_key=config.S3_SECRET_KEY.get_secret_value(),
    secure=config.S3_USE_SSL,
    region=config.S3_REGION,
)

def create_celery_app(include=None):
    """Create a Celery app
    
    If an array of packages if provided then we load the tasks
    this is used when the worker is started.

    Otherwise we return a connection to the broker to delay
    or schedule tasks.
    """
    import asyncio
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

