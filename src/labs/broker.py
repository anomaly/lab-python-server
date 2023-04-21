from .config import config

# See PyPI for more information about taskiq_redis
# https://pypi.org/project/taskiq-redis/
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend

from taskiq import InMemoryBroker

broker = InMemoryBroker()