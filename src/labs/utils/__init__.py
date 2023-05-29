""" Utility functions shared across the app

"""

from minio import Minio

from ..settings  import settings

minio_client = Minio(
    f"{settings.storage.endpoint}:{settings.storage.port}",
    access_key=settings.storage.access_key.get_secret_value(),
    secret_key=settings.storage.secret_key.get_secret_value(),
    secure=settings.storage,
    region=settings.storage.region,
)

def redis_client():
    """ Creates a redis client that can be used to connect to the
    redis server. 
    """
    import redis

    client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        decode_responses=True
    )

    return client