from .config import config

# See PyPI for more information about taskiq_redis
# https://pypi.org/project/taskiq-redis/
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend

redis_async_result = RedisAsyncResultBackend(
    redis_url=config.redis_dsn,
)

# TaskIQ have two brokers with similar interfaces, but with different logic. 
# The PubSubBroker uses redis' pubsub mechanism and is very powerful, 
# but it executes every task on all workers, because PUBSUB broadcasts message 
# to all subscribers.
broker = ListQueueBroker(
    url=config.redis_dsn,
    result_backend=redis_async_result,
)
