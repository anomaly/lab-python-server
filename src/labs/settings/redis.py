""" Redis configuration for TaskIQ

TaskIQ writes the results of the task to a Redis database. This
configuration allows the application to define the Redis database
"""

from pydantic import BaseSettings, RedisDsn


class RedisSettings(BaseSettings):

    # redis is used by TaskIQ for writing results
    host: str
    port: int = 6379

    @property
    def dsn(self) -> RedisDsn:
        """Construct the DSN for the TaskIQ broker

        This is provided by a container for development, but you 
        can choose to use a hosted product in production.
        """
        redis_url=f'redis://{self.host}:{self.port}'
        return RedisDsn(
            url=redis_url, 
            scheme="redis"
        )

    class Config:
        """ Env vars are prefixed with POSTGRES_ are loaded
        into instances of this class
        """
        env_prefix = "REDIS_"
