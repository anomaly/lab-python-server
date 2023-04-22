from .config import config

# See PyPI for more information about taskiq_redis
# https://pypi.org/project/taskiq-redis/
# 
# Redis is recommended as the results backend for the tasks
from taskiq_redis import RedisAsyncResultBackend

# RabbitMQ is recommended as the broker 
from taskiq_aio_pika import AioPikaBroker

redis_result_backend = RedisAsyncResultBackend(
    config.redis_dsn
)

broker = AioPikaBroker(
    config.amqp_dsn,
    result_backend=redis_result_backend
)
