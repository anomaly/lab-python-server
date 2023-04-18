""" Utility functions shared across the app

"""

from minio import Minio

from ..config import config

minio_client = Minio(
    f"{config.S3_ENDPOINT}:{config.S3_PORT}",
    access_key=config.S3_ACCESS_KEY.get_secret_value(),
    secret_key=config.S3_SECRET_KEY.get_secret_value(),
    secure=config.S3_USE_SSL,
    region=config.S3_REGION,
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