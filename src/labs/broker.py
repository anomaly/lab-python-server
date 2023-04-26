from .config import config

# See PyPI for more information about taskiq_redis
# https://pypi.org/project/taskiq-redis/
# 
# Redis is recommended as the results backend for the tasks
from taskiq_redis import RedisAsyncResultBackend

# RabbitMQ is recommended as the broker 
from taskiq_aio_pika import AioPikaBroker

# Task Scheduler for periodic tasks
from taskiq.schedule_sources import LabelScheduleSource
from taskiq.scheduler import TaskiqScheduler

redis_result_backend = RedisAsyncResultBackend(
    config.redis_dsn
)

broker = AioPikaBroker(
    config.amqp_dsn,
    result_backend=redis_result_backend
)

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)
