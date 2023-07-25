""" TaskIQ broker configuration

"""

from .settings import settings

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

# Middlewares
from taskiq import SimpleRetryMiddleware

# FastAPI middleware
import taskiq_fastapi

from .settings import settings

redis_result_backend = RedisAsyncResultBackend(
    str(settings.redis.dsn)
)

broker = (
    AioPikaBroker(str(settings.amqp.dsn),)
    .with_result_backend(redis_result_backend)
)

# Override the broker to use the InMemory backend
# if FastAPI is being called via pytest
# if settings.env == "pytest":
# from taskiq import InMemoryBroker
# broker = InMemoryBroker()


# Configure the necessary middlewares here, a default retry middleware
# is configured to retry tasks 3 times before failing you can override this
# https://bit.ly/3LLyH9M
broker.add_middlewares(
    SimpleRetryMiddleware(
        default_retry_count=settings.lifetime.queue_retry_count
    )
)

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[
        LabelScheduleSource(broker)
    ],
)

# The middleware is used to inject the broker into FastAPI
# it enables broker task discovery for FastAPI applications
# as well as sharing dependencies between tasks and FastAPI
taskiq_fastapi.init(broker, "labs.api:app")
