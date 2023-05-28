""" Utility functions shared across the app

"""

from minio import Minio

from ..config import config

minio_client = Minio(
    f"{config.storage.endpoint}:{config.storage.port}",
    access_key=config.storage.access_key.get_secret_value(),
    secret_key=config.storage.secret_key.get_secret_value(),
    secure=config.storage,
    region=config.storage.region,
)

def redis_client():
    """ Creates a redis client that can be used to connect to the
    redis server. 
    """
    import redis

    client = redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=0,
        decode_responses=True
    )

    return client